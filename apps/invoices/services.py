from datetime import datetime
from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Invoice

class InvoiceIngestionService:
    @staticmethod
    def ingest_invoice(data):
        # This is where the magic happens - creates new invoices from raw data
        # Super important to get this right or accounting will kill us! 😅
        return Invoice.objects.create(
            adjusted_gross_value=data['adjusted_gross_value'],
            haircut_percent=data['haircut_percent'],
            daily_advance_fee=data['daily_advance_fee'],
            # Si no hay advance_duration, usamos 30 días por default
            advance_duration=data.get('advance_duration', 30),
            customer_name=data['customer_name'],
            currency_code=data['currency_code'],
            customer_id=data['customer_id'],
            revenue_source_id=data['revenue_source_id'],
            revenue_source_name=data['revenue_source_name'],
            invoice_date=data.get('invoice_date', datetime.now().date())
        )

    @staticmethod
    def get_monthly_totals(customer_id=None, sort_by='-month', month_filter=None):
        """
        Get monthly totals for all customers or a specific customer.
        """
        queryset = Invoice.objects.all()
        
        # Convert customer_id to integer if it's not None
        if customer_id:
            try:
                customer_id = int(customer_id)
                queryset = queryset.filter(customer_id=customer_id)
            except (ValueError, TypeError):
                print(f"Invalid customer_id: {customer_id}")
        
        # Filter by month if provided
        if month_filter:
            try:
                month_filter = int(month_filter)
                queryset = queryset.filter(invoice_date__month=month_filter)
            except (ValueError, TypeError):
                print(f"Invalid month_filter: {month_filter}")

        order_by = [sort_by, 'customer_id'] if sort_by in ['month', '-month'] else ['-month', 'customer_id']

        monthly_data = queryset.annotate(
            month=TruncMonth('invoice_date')
        ).values(
            'month', 'customer_id', 'customer_name', 'currency_code'
        ).annotate(
            total_value=Sum('adjusted_gross_value')
        ).order_by(*order_by)

        results = []
        for data in monthly_data:
            sample_invoice = queryset.filter(
                customer_id=data['customer_id'],
                invoice_date__month=data['month'].month,
                currency_code=data['currency_code']
            ).first()

            if sample_invoice:
                loan_details = sample_invoice.calculate_loan_details()
                data.update(loan_details)
                data['currency_code'] = sample_invoice.currency_code
                results.append(data)

        return results

    @staticmethod
    def calculate_portfolio_metrics(invoices):
        """Calculate portfolio-wide metrics."""
        total_advance_amount = Decimal('0')
        total_fees = Decimal('0')
        
        for invoice in invoices:
            loan_details = invoice.calculate_loan_details()
            total_advance_amount += loan_details['advance_amount']
            total_fees += loan_details['total_fee']
        
        return {
            'total_advance_amount': round(total_advance_amount, 2),
            'total_fees': round(total_fees, 2),
            'average_apr': round(total_fees / total_advance_amount * 365 / 30 * 100, 2) if total_advance_amount else 0
        }







