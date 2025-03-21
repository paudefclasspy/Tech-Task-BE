from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from decimal import Decimal
import re

class Command(BaseCommand):
    help = 'Loads data from SQL file'

    def add_arguments(self, parser):
        parser.add_argument('sql_file', type=str, help='Path to the SQL file')

    def extract_values(self, line):
        # Esta función es un poco complicada pero hace la magia de convertir
        # los datos del SQL a algo que Django puede usar
        values = line.split('\t')
        formatted_values = []
        
        for value in values:
            # Null values - gotta handle these carefully!
            if value == '\\N' or value == '':
                formatted_values.append('NULL')
            # Dates need special formatting - don't mess this up or everything breaks 😅
            elif re.match(r'\d{4}-\d{2}-\d{2}', value):
                formatted_values.append(f"'{value}'")
            # Numbers are tricky - better use Decimal to avoid floating point mess
            elif re.match(r'^-?\d+\.?\d*$', value):
                decimal_val = str(Decimal(value))
                formatted_values.append(decimal_val)
            else:
                formatted_values.append(f"'{value}'")
                
        return formatted_values

    def handle(self, *args, **options):
        sql_file_path = options['sql_file']
        
        try:
            # first try to read the file
            # si el archivo no existe nos ahorramos todo el lío
            with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
                content = sql_file.read()
            
            # look for the good stuff between COPY and \.
            # esta regex es un poco hardcore pero funciona 🤘
            copy_pattern = r"COPY public\.invoices \((.*?)\) FROM stdin;\n(.*?)\\."
            match = re.search(copy_pattern, content, re.DOTALL)
            
            if not match:
                # something went wrong, better tell everyone
                # probably karen changed the file format again 🙄
                raise Exception("could not find data in the expected format")
            
            # now the fun part - processing all that data
            # get ready for some serious data crunching 🤓
            columns = match.group(1).split(', ')
            data_lines = match.group(2).strip().split('\n')
            
            # Map PostgreSQL columns to Django model fields
            column_mapping = {
                'id': 'id',
                'adjusted_gross_value': 'adjusted_gross_value',
                'haircut_percent': 'haircut_percent',
                'daily_advance_fee': 'daily_advance_fee',
                'advance_duration': 'advance_duration',
                'customer_name': 'customer_name',
                'customer_id': 'customer_id',
                'revenue_source_id': 'revenue_source_id',
                'revenue_source_name': 'revenue_source_name',
                'currency_code': 'currency_code',
                'invoice_date': 'invoice_date'
            }
            
            current_timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with connection.cursor() as cursor:
                # Delete existing data
                cursor.execute("DELETE FROM invoices_invoice")
                
                # Reset the SQLite sequence
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='invoices_invoice'")
                
                # Insert data
                for line in data_lines:
                    if line.strip():
                        values = self.extract_values(line)
                        
                        # Map columns and values
                        mapped_columns = ['created_at']  # Add created_at column
                        mapped_values = [f"'{current_timestamp}'"]  # Add created_at value
                        
                        for col, val in zip(columns, values):
                            django_col = column_mapping.get(col)
                            if django_col:
                                mapped_columns.append(django_col)
                                mapped_values.append(val)
                        
                        sql = f"""
                            INSERT INTO invoices_invoice 
                            ({', '.join(mapped_columns)})
                            VALUES ({', '.join(mapped_values)})
                        """
                        cursor.execute(sql)
                        
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded all data')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading data: {str(e)}')
            )








