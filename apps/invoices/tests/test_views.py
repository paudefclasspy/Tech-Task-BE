import pytest
from decimal import Decimal
from django.urls import reverse
from django.test import Client
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.invoices.models import Invoice

@pytest.mark.django_db
class TestViews:
    def setup_method(self):
        # gotta create a test user first, otherwise nothing works lol
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            is_active=True
        )
        
        # need both clients cuz we're testing different stuff
        # regular django client for the normal views
        self.client = Client()
        self.client.force_login(self.user)
        
        # api client for the fancy rest endpoints
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)
        
        # create a dummy invoice for testing
        # estos números son inventados pero sirven para probar 🤷‍♂️
        self.invoice = Invoice.objects.create(
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

    def test_invoice_api_list(self):
        # Use the correct URL pattern for API endpoints
        response = self.api_client.get('/api/invoices/')
        assert response.status_code == 200
        data = response.json()
        assert 'results' in data
        assert len(data['results']) == 1

    def test_invoice_api_detail(self):
        # Use the correct URL pattern for API detail endpoint
        response = self.api_client.get(f'/api/invoices/{self.invoice.id}/')
        assert response.status_code == 200
        assert response.json()['customer_name'] == 'Test Customer'










