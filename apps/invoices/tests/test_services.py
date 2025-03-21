import pytest
from decimal import Decimal
from django.utils import timezone
from apps.invoices.models import Invoice
from apps.invoices.services import InvoiceIngestionService

@pytest.mark.django_db
class TestInvoiceIngestionService:
    def test_ingest_invoice(self):
        # testing the main ingestion logic
        # si esto falla todo se va al traste 😱
        data = {
            'adjusted_gross_value': Decimal('1000.00'),
            'haircut_percent': Decimal('20.00'),
            'daily_advance_fee': Decimal('0.05'),
            'advance_duration': 30,
            'customer_name': 'Test Customer',
            'currency_code': 'USD',  # always start with usd, keep it simple
            'customer_id': 1,
            'revenue_source_id': 1,
            'revenue_source_name': 'Test Source'
        }
        
        invoice = InvoiceIngestionService.ingest_invoice(data)
        assert invoice.adjusted_gross_value == Decimal('1000.00')
        assert invoice.haircut_percent == Decimal('20.00')

        # Test loan calculations
        loan_details = invoice.calculate_loan_details()
        assert loan_details['haircut_amount'] == Decimal('200.00')
        assert loan_details['advance_amount'] == Decimal('800.00')
        assert loan_details['daily_fee_amount'] == Decimal('0.40')
        assert loan_details['expected_fees'] == Decimal('12.00')

    def test_get_monthly_totals(self):
        # necesitamos esto para los reportes mensuales
        # el equipo de finanzas vive de estos números
        data = {
            'adjusted_gross_value': Decimal('1000.00'),
            'haircut_percent': Decimal('20.00'),
            'daily_advance_fee': Decimal('0.05'),
            'advance_duration': 30,
            'customer_name': 'Test Customer',
            'currency_code': 'USD',
            'customer_id': 1,
            'revenue_source_id': 1,
            'revenue_source_name': 'Test Source'
        }
        
        InvoiceIngestionService.ingest_invoice(data)
        
        totals = InvoiceIngestionService.get_monthly_totals(customer_id=1)
        assert len(totals) == 1
        assert totals[0]['total_value'] == Decimal('1000.00')


