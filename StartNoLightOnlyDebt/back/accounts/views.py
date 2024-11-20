from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from managebanks.models import FinancialCompany


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def preferred_loan_list(request):
    user = request.user  # 현재 로그인된 사용자
    if user.is_authenticated:
        # 선호 은행 데이터 가져오기
        preferred_banks = user.preferred_banks.all()  # ManyToMany 관계 데이터
        preferred_banks_data = list(preferred_banks.values('company_id', 'company_name'))  # 필요한 필드만 반환

        response = {
            "profile_user": {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "password": "********",  # 비밀번호는 반환하지 않음
                "preferred_banks": preferred_banks_data,  # 선호 은행 데이터
            }
        }
    else:
        response = {
            "error": "User is not authenticated."
        }
        return JsonResponse(response, status=401)

    return JsonResponse(response)

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from managebanks.models import FinancialCompany

class PreferredBanksUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # 전체 은행 목록 가져오기
        all_banks = FinancialCompany.objects.all()
        # 사용자의 선호 은행 가져오기
        preferred_banks = user.preferred_banks.all()

        # 전체 은행 목록에 is_preferred 추가
        bank_data = []
        for bank in all_banks:
            bank_data.append({
                "company_id": bank.company_id,
                "company_name": bank.company_name,
                "is_preferred": bank in preferred_banks
            })

        return Response({"banks": bank_data})

    def put(self, request):
        user = request.user
        bank_ids = request.data.get('preferred_banks', [])
        valid_banks = FinancialCompany.objects.filter(company_id__in=bank_ids)

        if len(valid_banks) != len(bank_ids):
            return Response({
                "error": "유효하지 않은 bank_ids가 포함되어 있습니다.",
                "invalid_bank_ids": list(set(bank_ids) - set(valid_banks.values_list('company_id', flat=True))),
            }, status=400)

        # 선호 은행 업데이트
        user.preferred_banks.set(valid_banks)
        return Response({
            "message": "선호 은행이 성공적으로 업데이트되었습니다.",
            "preferred_banks": [
                {"company_id": bank.company_id, "company_name": bank.company_name}
                for bank in user.preferred_banks.all()
            ]
        })




