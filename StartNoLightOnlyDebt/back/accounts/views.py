from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def preferred_loan_list(request):
    user = request.user  # 현재 로그인된 사용자
    if user.is_authenticated:
        # 선호 은행 데이터 가져오기
        preferred_banks = user.preferred_banks.all()  # ManyToMany 관계 데이터
        preferred_banks_data = list(preferred_banks.values('company_id', 'company_name'))  # 필드 수정

        response = {
            "profile_user": {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "password": "********",  # 실제 비밀번호는 반환하지 않음
                "preferred_banks": preferred_banks_data,  # 선호 은행 데이터
            }
        }
    else:
        response = {
            "error": "User is not authenticated."
        }
        return JsonResponse(response, status=401)

    return JsonResponse(response)
