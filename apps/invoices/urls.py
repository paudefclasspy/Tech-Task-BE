from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register('invoices', views.InvoiceViewSet, basename='invoice-api')

# The API URLs are now determined automatically by the router
urlpatterns = [
    # Regular views
    path('', views.DashboardView.as_view(), name='dashboard'),  # Dashboard at root
    path('invoices/', views.InvoiceListView.as_view(), name='invoice-list-view'),
    
    # API endpoints - prefix all router URLs with 'api/'
    path('api/', include(router.urls)),
]


