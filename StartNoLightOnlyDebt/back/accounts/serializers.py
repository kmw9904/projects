# accounts/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User  # User 모델을 사용
from managebanks.models import FinancialCompany  # 올바른 모델 사용

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=True)  # 이름 필드 추가
    preferred_banks = serializers.PrimaryKeyRelatedField(
        many=True, queryset=FinancialCompany.objects.all(), required=False
    )  # 선호 은행 필드 추가

    def get_cleaned_data(self):
        # 기본 회원가입 필드 가져오기
        data = super().get_cleaned_data()
        # 추가 필드 병합
        data['name'] = self.validated_data.get('name', '')
        data['preferred_banks'] = self.validated_data.get('preferred_banks', [])
        return data

    def save(self, request):
        # 기본 사용자 생성
        user = super().save(request)
        # 추가 필드 저장
        user.name = self.cleaned_data.get('name', '')  # 이름 저장
        user.save()
        user.preferred_banks.set(self.cleaned_data.get('preferred_banks', []))  # 선호 은행 저장
        return user
