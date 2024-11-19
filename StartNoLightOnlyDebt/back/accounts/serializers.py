# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from managebanks.models import FinancialCompany

User = get_user_model()

class CustomRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    preferred_banks = serializers.PrimaryKeyRelatedField(queryset=FinancialCompany.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'name', 'preferred_banks']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # preferred_banks 처리: ManyToMany 관계 설정
        if 'preferred_banks' in validated_data:
            preferred_banks = validated_data['preferred_banks']
            print(f"Assigning preferred_banks: {preferred_banks}")  # 디버깅 로그
            user.preferred_banks.set(preferred_banks)
            user.save()

        return user

    
