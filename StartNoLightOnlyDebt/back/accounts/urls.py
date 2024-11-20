from django.urls import path
from .views import CustomRegisterView, PreferredBanksUpdateView, preferred_loan_list
from dj_rest_auth.views import LogoutView
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('preferred-banks/', PreferredBanksUpdateView.as_view(), name='preferred_banks_update'),
    path('signup/', CustomRegisterView.as_view(), name='custom_signup'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('profile/', preferred_loan_list, name='accounts-profile'),
    path('account-confirm-email/<str:key>/', VerifyEmailView.as_view(), name='account_confirm_email'),
]
