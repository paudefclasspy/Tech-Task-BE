
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from calendar import month_name
from .models import Invoice
from .services import InvoiceIngestionService
from .serializers import InvoiceSerializer
from django.http import HttpResponse
import csv
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
import decimal

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'invoices/dashboard.html'

    def get(self, request, *args, **kwargs):
        if 'export' in request.GET:
            return self.export_csv()
        return super().get(request, *args, **kwargs)

    def export_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="invoice_report_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Month', 'Customer', 'Total Value', 'Haircut Amount', 'Advance Amount', 
                        'Daily Fee', 'Expected Fees', 'APR'])
        
        monthly_totals = self.get_context_data()['monthly_totals']
        for total in monthly_totals:
            writer.writerow([
                total['month'].strftime("%B %Y"),
                total['customer_name'],
                total['total_value'],
                total['haircut_amount'],
                total['advance_amount'],
                total['daily_fee_amount'],
                total['expected_fees'],
                f"{total['apr']}%"
            ])
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter parameters
        customer_id = self.request.GET.get('customer_id')
        current_sort = self.request.GET.get('sort', '-month')  # Default to newest first
        current_month = self.request.GET.get('month')
        
        # Get monthly totals using the service
        monthly_totals = InvoiceIngestionService.get_monthly_totals(
            customer_id=customer_id,
            sort_by=current_sort,
            month_filter=current_month
        )
        
        # Debug print
        print("Filter params:", {
            'customer_id': customer_id,
            'sort': current_sort,
            'month': current_month
        })
        print("Monthly Totals:", monthly_totals)
        
        # Convert Decimal objects to float for JSON serialization
        monthly_totals_json = []
        for total in monthly_totals:
            json_total = {
                'month': total['month'].strftime('%Y-%m-%d') if total['month'] else None,
                'customer_name': total['customer_name'],
                'customer_id': total['customer_id'],
                'currency_code': total.get('currency_code', 'USD'),
                'total_value': float(total['total_value']) if total['total_value'] else 0,
                'advance_amount': float(total.get('advance_amount', 0)),
                'expected_fees': float(total.get('expected_fees', 0)),
                'apr': float(total.get('apr', 0))
            }
            monthly_totals_json.append(json_total)
        
        # Get all customers for the filter dropdown
        customers = Invoice.objects.values(
            'customer_id', 'customer_name'
        ).distinct().order_by('customer_name')
        
        # Get all months for the filter dropdown
        months = Invoice.objects.dates('invoice_date', 'month', order='DESC')
        months = [{'number': m.month, 'name': m.strftime('%B %Y')} for m in months]
        
        # Get all unique currencies
        currencies = Invoice.objects.values_list(
            'currency_code', flat=True
        ).distinct().order_by('currency_code')
        
        context.update({
            'monthly_totals': monthly_totals,
            'monthly_totals_json': json.dumps(monthly_totals_json, cls=DjangoJSONEncoder),
            'currencies': currencies,
            'customers': customers,
            'months': months,
            'current_sort': current_sort,
            'current_month': int(current_month) if current_month else None,
        })
        
        return context

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_id = self.request.GET.get('customer_id')
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        return queryset.order_by('-created_at')

class InvoiceViewSet(viewsets.ModelViewSet):
    # api stuff - keep it restful!
    # frontend devs will hunt you down if you break this 🔪
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    # estos filtros son súper útiles
    # pero cuidado con filtrar demasiado o la db llora 😢
    filterset_fields = ['customer_id', 'currency_code', 'revenue_source_id']













