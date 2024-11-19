# accounts/admin.py
from django.contrib import admin
from .models import User
from managebanks.models import FinancialCompany

admin.site.register(User)
admin.site.register(FinancialCompany)