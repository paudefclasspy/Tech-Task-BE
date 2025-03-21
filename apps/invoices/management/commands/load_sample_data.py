from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.invoices.services import InvoiceIngestionService

class Command(BaseCommand):
    help = 'Loads sample invoice data'

    def handle(self, *args, **kwargs):
        # just some dummy data for testing
        # no uses esto en prod porfa 🙏
        sample_data = [
            {
                'adjusted_gross_value': Decimal('1000.00'),
                'haircut_percent': Decimal('20.00'),
                'daily_advance_fee': Decimal('0.05'),
                'customer_name': 'Sample Customer 1',
                # usd always works for testing, keep it simple
                'currency_code': 'USD',
                'customer_id': 1,
                'revenue_source_id': 1,
                'revenue_source_name': 'Online Sales'
            },
            # otro más por si acaso
            {
                'adjusted_gross_value': Decimal('2000.00'),
                'haircut_percent': Decimal('15.00'),
                'daily_advance_fee': Decimal('0.04'),
                'customer_name': 'Sample Customer 2',
                # mezclamos con eur para ver que todo funcione
                'currency_code': 'EUR',
                'customer_id': 2,
                'revenue_source_id': 2,
                'revenue_source_name': 'Retail Sales'
            }
        ]

        for data in sample_data:
            InvoiceIngestionService.ingest_invoice(data)
            self.stdout.write(
                self.style.SUCCESS(f'Created invoice for {data["customer_name"]}')
            )
