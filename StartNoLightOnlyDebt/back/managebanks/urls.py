from django.urls import path
from .views import FetchFinancialData, BankListView, CalculateMonthlyPayment
from .views import CreditLoanView, JeonseLoanView, MortgageLoanView, BankListView, FinancialProductDetailView

urlpatterns = [
    path('fetch-financial-data/', FetchFinancialData.as_view(), name='fetch_financial_data'),
    path('calculate/<str:product_type>/<str:product_id>/', CalculateMonthlyPayment.as_view(), name='calculate_monthly_payment'),
    path("credit-loans/", CreditLoanView.as_view(), name="credit_loans"),
    path("jeonse-loans/", JeonseLoanView.as_view(), name="jeonse_loans"),
    path("mortgage-loans/", MortgageLoanView.as_view(), name="mortgage_loans"),
    path("banks/", BankListView.as_view(), name="bank-list"),
    path("product/<str:product_id>/", FinancialProductDetailView.as_view(), name="financial-product-detail"),
]
