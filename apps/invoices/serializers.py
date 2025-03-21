from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    # adding some extra spicy data for the frontend peeps
    # they always want more fields lol
    loan_details = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'adjusted_gross_value', 'haircut_percent', 'daily_advance_fee',
            'advance_duration', 'customer_name', 'currency_code', 'customer_id',
            'revenue_source_id', 'revenue_source_name', 'invoice_date',
            'created_at', 'loan_details'  # this last one is the magic sauce ✨
        ]

    def get_loan_details(self, obj):
        # aquí calculamos todo lo importante
        # si la math está mal nos matan los de finanzas 💀
        return obj.calculate_loan_details()

