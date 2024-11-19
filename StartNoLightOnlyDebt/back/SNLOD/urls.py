"""
URL configuration for SNLOD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import preferred_loan_list
from django.urls import path
from django.http import HttpResponse
from dj_rest_auth.views import LogoutView

def custom_email_confirmation(request, *args, **kwargs):
    return HttpResponse("Email confirmed successfully.", content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('managebanks.urls')),  # accounts 앱 URL 포함
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('accounts/logout/', LogoutView.as_view(), name='rest_logout'),
    path('accounts/profile/', preferred_loan_list, name='accounts-profile'),
    path('accounts/signup/account-confirm-email/<key>/', custom_email_confirmation, name="account_confirm_email"),
]
