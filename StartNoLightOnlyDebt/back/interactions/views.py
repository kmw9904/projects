from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
import json

from .models import CreditLike, CreditComment, JeonseLike, JeonseComment, MortgageLike, MortgageComment
from .serializers import CreditCommentSerializer, JeonseCommentSerializer, MortgageCommentSerializer
from managebanks.models import CreditLoanOption, JeonseOption, MortgageOption

# 개인 대출

@api_view(['GET'])
def get_credit_likes(request, product_id):
    try:
        like_count = CreditLike.objects.filter(product=product_id).count()
        return JsonResponse({"likes": like_count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def toggle_credit_like(request, product_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "사용자가 로그인되지 않았습니다."}, status=401)

    try:
        product = get_object_or_404(CreditLoanOption, option_id=product_id)
        like, created = CreditLike.objects.get_or_create(user=user, product=product)
        if not created:
            like.delete()
            message = "좋아요 취소"
        else:
            message = "좋아요 추가"

        like_count = CreditLike.objects.filter(product=product).count()
        return JsonResponse({"message": message, "likes": like_count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['GET'])
def get_credit_comments(request, product_id):
    try:
        comments = CreditComment.objects.filter(product=product_id)
        serialized_data = CreditCommentSerializer(comments, many=True).data
        return JsonResponse(serialized_data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def add_credit_comment(request, product_id):
    try:
        user = request.user
        data = json.loads(request.body.decode("utf-8"))
        data['user'] = user.id
        data['product'] = product_id

        serialized_data = CreditCommentSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return JsonResponse(serialized_data.data, status=201)
        else:
            return JsonResponse(serialized_data.errors, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['DELETE'])
def delete_credit_comment(request, product_id, comment_id):
    try:
        comment = get_object_or_404(CreditComment, id=comment_id, product__option_id=product_id)
        if comment.user != request.user:
            return JsonResponse({"error": "삭제 권한이 없습니다."}, status=403)
        comment.delete()
        return JsonResponse({"message": "댓글이 삭제되었습니다."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# 전세 대출

@api_view(['GET'])
def get_jeonse_likes(request, product_id):
    try:
        like_count = JeonseLike.objects.filter(product=product_id).count()
        return JsonResponse({"likes": like_count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def toggle_jeonse_like(request, product_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "사용자가 로그인되지 않았습니다."}, status=401)

    try:
        product = get_object_or_404(JeonseOption, option_id=product_id)
        like, created = JeonseLike.objects.get_or_create(user=user, product=product)
        if not created:
            like.delete()
            message = "좋아요 취소"
        else:
            message = "좋아요 추가"

        like_count = JeonseLike.objects.filter(product=product).count()
        return JsonResponse({"message": message, "likes": like_count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['GET'])
def get_jeonse_comments(request, product_id):
    try:
        comments = JeonseComment.objects.filter(product=product_id)
        serialized_data = JeonseCommentSerializer(comments, many=True).data
        return JsonResponse(serialized_data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def add_jeonse_comment(request, product_id):
    try:
        user = request.user
        data = json.loads(request.body.decode("utf-8"))
        data['user'] = user.id
        data['product'] = product_id

        serialized_data = JeonseCommentSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return JsonResponse(serialized_data.data, status=201)
        else:
            return JsonResponse(serialized_data.errors, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['DELETE'])
def delete_jeonse_comment(request, product_id, comment_id):
    try:
        comment = get_object_or_404(JeonseComment, id=comment_id, product__option_id=product_id)
        if comment.user != request.user:
            return JsonResponse({"error": "삭제 권한이 없습니다."}, status=403)
        comment.delete()
        return JsonResponse({"message": "댓글이 삭제되었습니다."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# 담보 대출

@api_view(['GET'])
def get_mortgage_likes(request, product_id):
    try:
        like_count = MortgageLike.objects.filter(product=product_id).count()
        return JsonResponse({"likes": like_count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def toggle_mortgage_like(request, product_id):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "사용자가 로그인되지 않았습니다."}, status=401)

    try:
        product = get_object_or_404(MortgageOption, option_id=product_id)
        like, created = MortgageLike.objects.get_or_create(user=user, product=product)
        if not created:
            like.delete()
            message = "좋아요 취소"
        else:
            message = "좋아요 추가"

        like_count = MortgageLike.objects.filter(product=product).count()
        return JsonResponse({"message": message, "likes": like_count}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['GET'])
def get_mortgage_comments(request, product_id):
    try:
        comments = MortgageComment.objects.filter(product=product_id)
        serialized_data = MortgageCommentSerializer(comments, many=True).data
        return JsonResponse(serialized_data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def add_mortgage_comment(request, product_id):
    try:
        user = request.user
        data = json.loads(request.body.decode("utf-8"))
        data['user'] = user.id
        data['product'] = product_id

        serialized_data = MortgageCommentSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return JsonResponse(serialized_data.data, status=201)
        else:
            return JsonResponse(serialized_data.errors, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['DELETE'])
def delete_mortgage_comment(request, product_id, comment_id):
    try:
        comment = get_object_or_404(MortgageComment, id=comment_id, product__option_id=product_id)
        if comment.user != request.user:
            return JsonResponse({"error": "삭제 권한이 없습니다."}, status=403)
        comment.delete()
        return JsonResponse({"message": "댓글이 삭제되었습니다."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
