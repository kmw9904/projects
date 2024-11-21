from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from managebanks.models import CreditLoanOption

def get_likes(model, product_id):
    """
    특정 상품에 대한 좋아요 수를 반환
    """
    try:
        # ForeignKey를 통해 product__id로 참조
        like_count = model.objects.filter(product=product_id).count()
        return JsonResponse({"likes": like_count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def toggle_like(model, user, product_id):
    """
    특정 상품에 대한 좋아요 토글
    """
    if not user.is_authenticated:
        return JsonResponse({"error": "사용자가 로그인되지 않았습니다."}, status=401)

    try:
        # product_id로 CreditLoanOption 인스턴스 가져오기
        product = get_object_or_404(CreditLoanOption, option_id=product_id)

        # 좋아요 토글 처리
        like, created = model.objects.get_or_create(user=user, product=product)
        if not created:
            like.delete()
            message = "좋아요 취소"
        else:
            message = "좋아요 추가"
        
        like_count = model.objects.filter(product=product).count()
        return JsonResponse({"message": message, "likes": like_count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_comments(model, serializer, product_id):
    """
    특정 상품에 대한 댓글 목록 반환
    """
    try:
        # ForeignKey를 통해 product__id로 참조
        comments = model.objects.filter(product=product_id)
        serialized_data = serializer(comments, many=True).data
        return JsonResponse(serialized_data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


import json
from django.http import JsonResponse

def add_comment(model, serializer, request, user, product_id):
    try:
        # request.body에서 JSON 데이터 파싱
        data = json.loads(request.body.decode("utf-8"))
        print("요청 데이터:", data)  # 디버깅용 출력

        # 사용자 및 상품 정보 추가
        data['user'] = user.id
        data['product'] = product_id

        # 직렬화 및 저장
        serialized_data = serializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return JsonResponse(serialized_data.data, status=201)
        else:
            print("유효성 검증 실패:", serialized_data.errors)  # 디버깅용 출력
            return JsonResponse(serialized_data.errors, status=400)
    except Exception as e:
        print("예외 발생:", e)  # 예외 출력
        return JsonResponse({"error": str(e)}, status=400)



