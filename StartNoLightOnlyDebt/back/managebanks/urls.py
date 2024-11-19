from django.urls import path
from .views import FetchFinancialData, BankListView, CalculateMonthlyPayment

urlpatterns = [
    path('fetch-financial-data/', FetchFinancialData.as_view(), name='fetch_financial_data'),
    path('calculate/<str:product_type>/<str:product_id>/', CalculateMonthlyPayment.as_view(), name='calculate_monthly_payment'),
    path("banks/", BankListView.as_view(), name="bank-list"),
]
