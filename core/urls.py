from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # the usual django stuff
    path('admin/', admin.site.urls),
    
    # main app urls
    path('', include('apps.invoices.urls')),
    
    # accounts urls - include the full accounts urls
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    
    # Remove these since they're now handled by accounts.urls
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]




