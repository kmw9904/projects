from django.views.decorators.http import require_http_methods
from .models import CreditLike, CreditComment, JeonseLike, JeonseComment, MortgageLike, MortgageComment
from .serializers import CreditCommentSerializer, JeonseCommentSerializer, MortgageCommentSerializer
from .helpers import get_likes, toggle_like, get_comments, add_comment
from django.views.decorators.csrf import csrf_exempt

# 개인 대출

@require_http_methods(["GET"])
def get_credit_likes(request, product_id):
    return get_likes(CreditLike, product_id)

@csrf_exempt
@require_http_methods(["POST"])
def toggle_credit_like(request, product_id):
    return toggle_like(CreditLike, request.user, product_id)

@require_http_methods(["GET"])
def get_credit_comments(request, product_id):
    return get_comments(CreditComment, CreditCommentSerializer, product_id)

@csrf_exempt
@require_http_methods(["POST"])
def add_credit_comment(request, product_id):
    return add_comment(CreditComment, CreditCommentSerializer, request=request, user=request.user, product_id=product_id)

# 전세 대출

@require_http_methods(["GET"])
def get_jeonse_likes(request, product_id):
    return get_likes(JeonseLike, product_id)

@csrf_exempt
@require_http_methods(["POST"])
def toggle_jeonse_like(request, product_id):
    return toggle_like(JeonseLike, request.user, product_id)

@require_http_methods(["GET"])
def get_jeonse_comments(request, product_id):
    return get_comments(JeonseComment, JeonseCommentSerializer, product_id)

@csrf_exempt
@require_http_methods(["POST"])
def add_jeonse_comment(request, product_id):
    return add_comment(JeonseComment, JeonseCommentSerializer, request.POST, request.user, product_id)

# 담보 대출

@require_http_methods(["GET"])
def get_mortgage_likes(request, product_id):
    return get_likes(MortgageLike, product_id)

@csrf_exempt
@require_http_methods(["POST"])
def toggle_mortgage_like(request, product_id):
    return toggle_like(MortgageLike, request.user, product_id)

@require_http_methods(["GET"])
def get_mortgage_comments(request, product_id):
    return get_comments(MortgageComment, MortgageCommentSerializer, product_id)

@csrf_exempt
@require_http_methods(["POST"])
def add_mortgage_comment(request, product_id):
    return add_comment(MortgageComment, MortgageCommentSerializer, request.POST, request.user, product_id)
