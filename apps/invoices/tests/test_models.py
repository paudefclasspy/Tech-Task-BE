import pytest
from decimal import Decimal
from django.utils import timezone
from apps.invoices.models import Invoice

@pytest.mark.django_db
class TestInvoice:
    def test_invoice_creation(self):
        # Basic smoke test - if this fails we're in deep trouble lol
        invoice = Invoice.objects.create(
            adjusted_gross_value=Decimal('1000.00'),
            haircut_percent=Decimal('20.00'),
            daily_advance_fee=Decimal('0.05'),
            advance_duration=30,
            customer_name='Test Customer',
            currency_code='USD',
            customer_id=1,
            revenue_source_id=1,
            revenue_source_name='Test Source'
        )

    def test_calculate_loan_details(self):
        # Aquí probamos que los cálculos no estén locos
        # Si esto falla, el equipo de finanzas nos mata 💀
        invoice = Invoice.objects.create(
            adjusted_gross_value=Decimal('1000.00'),
            haircut_percent=Decimal('20.00'),
            daily_advance_fee=Decimal('0.05'),
            advance_duration=30,
            customer_name='Test Customer',
            currency_code='USD',
            customer_id=1,
            revenue_source_id=1,
            revenue_source_name='Test Source'
        )
        
        loan_details = invoice.calculate_loan_details()
        assert loan_details['haircut_amount'] == Decimal('200.00')
        assert loan_details['advance_amount'] == Decimal('800.00')
        assert loan_details['daily_fee_amount'] == Decimal('0.40')
        assert loan_details['expected_fees'] == Decimal('12.00')


