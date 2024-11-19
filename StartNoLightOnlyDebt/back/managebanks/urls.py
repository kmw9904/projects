from django.urls import path
from .views import FetchFinancialData, BankListView

urlpatterns = [
    path('fetch-financial-data/', FetchFinancialData.as_view(), name='fetch_financial_data'),
    path("banks/", BankListView.as_view(), name="bank-list"),
]
