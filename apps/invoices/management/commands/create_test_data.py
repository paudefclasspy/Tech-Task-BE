from django.core.management.base import BaseCommand
from apps.invoices.models import Invoice
from decimal import Decimal
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Creates test invoice data with multiple currencies'

    def handle(self, *args, **options):
        currencies = ['USD', 'EUR', 'GBP']
        customers = [
            {'id': 1, 'name': 'Customer A'},
            {'id': 2, 'name': 'Customer B'},
            {'id': 3, 'name': 'Customer C'},
        ]
        
        # Create invoices for the last 6 months
        for i in range(180):  # 6 months * 30 days
            invoice_date = date.today() - timedelta(days=i)
            
            for customer in customers:
                for currency in currencies:
                    Invoice.objects.create(
                        adjusted_gross_value=Decimal(random.uniform(1000, 10000)),
                        haircut_percent=Decimal(random.uniform(10, 30)),
                        daily_advance_fee=Decimal(random.uniform(0.01, 0.05)),
                        advance_duration=30,
                        customer_name=customer['name'],
                        currency_code=currency,
                        customer_id=customer['id'],
                        revenue_source_id=1,
                        revenue_source_name='Test Source',
                        invoice_date=invoice_date
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))