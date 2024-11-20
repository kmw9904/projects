from rest_framework import serializers
from .models import FinancialCompany, FinancialProduct, MortgageOption, JeonseOption, CreditLoanOption

# FinancialCompany Serializer
class FinancialCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCompany
        fields = ['company_id', 'company_name']


# FinancialProduct Serializer
class FinancialProductSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='fin_co_no.company_name', read_only=True)

    class Meta:
        model = FinancialProduct
        fields = [
            'product_id', 'product_name', 'company_name', 'join_way', 'loan_inci_expn',
            'erly_rpay_fee', 'dly_rate', 'loan_lmt', 'prdt_div'
        ]


# JeonseOption Serializer
class JeonseOptionSerializer(serializers.ModelSerializer):
    product = FinancialProductSerializer(source='fin_prdt_cd', read_only=True)

    class Meta:
        model = JeonseOption
        fields = [
            'option_id', 'rpay_type', 'rpay_type_nm', 
            'lend_rate_type', 'lend_rate_type_nm', 'lend_rate_min', 
            'lend_rate_max', 'lend_rate_avg', 'product',  # FinancialProduct 포함
        ]


# MortgageOption Serializer
class MortgageOptionSerializer(serializers.ModelSerializer):
    product = FinancialProductSerializer(source='fin_prdt_cd', read_only=True)

    class Meta:
        model = MortgageOption
        fields = [
            'option_id', 'mrtg_type', 'mrtg_type_nm', 'rpay_type', 'rpay_type_nm', 
            'lend_rate_type', 'lend_rate_type_nm', 'lend_rate_min', 
            'lend_rate_max', 'lend_rate_avg', 'product',  # FinancialProduct 포함
        ]


# CreditLoanOption Serializer
class CreditLoanOptionSerializer(serializers.ModelSerializer):
    # FinancialProduct 데이터 포함
    product = FinancialProductSerializer(source='fin_prdt_cd', read_only=True)

    class Meta:
        model = CreditLoanOption
        fields = [
            'option_id', 'crdt_prdt_type', 'crdt_lend_rate_type', 'crdt_lend_rate_type_nm',
            'crdt_grad_1', 'crdt_grad_4', 'crdt_grad_5', 'crdt_grad_6', 'crdt_grad_avg',
            'product',  # 포함된 FinancialProduct 데이터
        ]
