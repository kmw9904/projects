from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Like, Comment
from .serializers import LikeSerializer, CommentSerializer
from managebanks.models import JeonseOption, CreditLoanOption, MortgageOption
from django.db.models import Count

class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, option_type, option_id):
        user = request.user

        # 각 옵션 유형에 따른 좋아요 데이터 조회
        if option_type == "jeonse":
            option = JeonseOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Jeonse option not found"}, status=status.HTTP_404_NOT_FOUND)
            is_liked = Like.objects.filter(user=user, jeonse_option=option).exists()
            likes_count = Like.objects.filter(jeonse_option=option).count()
        elif option_type == "credit":
            option = CreditLoanOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Credit loan option not found"}, status=status.HTTP_404_NOT_FOUND)
            is_liked = Like.objects.filter(user=user, credit_loan_option=option).exists()
            likes_count = Like.objects.filter(credit_loan_option=option).count()
        elif option_type == "mortgage":
            option = MortgageOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Mortgage option not found"}, status=status.HTTP_404_NOT_FOUND)
            is_liked = Like.objects.filter(user=user, mortgage_option=option).exists()
            likes_count = Like.objects.filter(mortgage_option=option).count()
        else:
            return Response({"error": "Invalid option type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"is_liked": is_liked, "likes": likes_count}, status=status.HTTP_200_OK)

    def post(self, request, option_type, option_id):
        user = request.user

        # 각 옵션 유형에 따른 필터링
        if option_type == "jeonse":
            option = JeonseOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Jeonse option not found"}, status=status.HTTP_404_NOT_FOUND)
            like, created = Like.objects.get_or_create(user=user, jeonse_option=option)
            likes_count = Like.objects.filter(jeonse_option=option).count()
        elif option_type == "credit":
            option = CreditLoanOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Credit loan option not found"}, status=status.HTTP_404_NOT_FOUND)
            like, created = Like.objects.get_or_create(user=user, credit_loan_option=option)
            likes_count = Like.objects.filter(credit_loan_option=option).count()
        elif option_type == "mortgage":
            option = MortgageOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Mortgage option not found"}, status=status.HTTP_404_NOT_FOUND)
            like, created = Like.objects.get_or_create(user=user, mortgage_option=option)
            likes_count = Like.objects.filter(mortgage_option=option).count()
        else:
            return Response({"error": "Invalid option type"}, status=status.HTTP_400_BAD_REQUEST)

        # 좋아요 생성 또는 제거
        is_liked = created
        if not created:
            like.delete()
            is_liked = False
            likes_count -= 1

        return Response({
            "message": "Like toggled",
            "likes": likes_count,
            "is_liked": is_liked
        }, status=status.HTTP_200_OK)



class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, option_type, option_id):
        user = request.user
        content = request.data.get("content")

        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 각 옵션 유형에 따른 필터링 및 댓글 생성
        if option_type == "jeonse":
            option = JeonseOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Jeonse option not found"}, status=status.HTTP_404_NOT_FOUND)
            comment = Comment.objects.create(user=user, jeonse_option=option, content=content)
        elif option_type == "credit":
            option = CreditLoanOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Credit loan option not found"}, status=status.HTTP_404_NOT_FOUND)
            comment = Comment.objects.create(user=user, credit_loan_option=option, content=content)
        elif option_type == "mortgage":
            option = MortgageOption.objects.filter(option_id=option_id).first()
            if not option:
                return Response({"error": "Mortgage option not found"}, status=status.HTTP_404_NOT_FOUND)
            comment = Comment.objects.create(user=user, mortgage_option=option, content=content)
        else:
            return Response({"error": "Invalid option type"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, option_type, option_id):
        # 각 옵션 유형에 따른 필터링 및 댓글 조회
        if option_type == "jeonse":
            comments = Comment.objects.filter(jeonse_option__option_id=option_id)
        elif option_type == "credit":
            comments = Comment.objects.filter(credit_loan_option__option_id=option_id)
        elif option_type == "mortgage":
            comments = Comment.objects.filter(mortgage_option__option_id=option_id)
        else:
            return Response({"error": "Invalid option type"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 삭제
    def delete(self, request, option_type, option_id, comment_id):
        user = request.user

        try:
            # 각 옵션 유형에 따른 댓글 삭제 처리
            if option_type == "jeonse":
                comment = Comment.objects.get(id=comment_id, jeonse_option__option_id=option_id, user=user)
            elif option_type == "credit":
                comment = Comment.objects.get(id=comment_id, credit_loan_option__option_id=option_id, user=user)
            elif option_type == "mortgage":
                comment = Comment.objects.get(id=comment_id, mortgage_option__option_id=option_id, user=user)
            else:
                return Response({"error": "Invalid option type"}, status=status.HTTP_400_BAD_REQUEST)

            comment.delete()
            return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_200_OK)

        except Comment.DoesNotExist:
            return Response({"error": "댓글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        

class TopLikedProductsView(APIView):
    """
    각 상품 유형에서 좋아요가 가장 많은 상품을 반환합니다.
    """
    def get(self, request, option_type):
        try:
            if option_type == "credit":
                top_product = CreditLoanOption.objects.annotate(
                    likes_count=Count('credit_likes')
                ).order_by('-likes_count').first()
            elif option_type == "jeonse":
                top_product = JeonseOption.objects.annotate(
                    likes_count=Count('jeonse_likes')
                ).order_by('-likes_count').first()
            elif option_type == "mortgage":
                top_product = MortgageOption.objects.annotate(
                    likes_count=Count('mortgage_likes')
                ).order_by('-likes_count').first()
            else:
                return Response({"error": "Invalid option type"}, status=status.HTTP_400_BAD_REQUEST)

            if top_product:
                return Response({
                    "product_id": top_product.option_id,
                    "product_type": option_type,
                    # "product_name": top_product.product_name,  # 확인 필요: 실제 상품 이름 필드명
                    "company_name": top_product.company.name if hasattr(top_product, 'company') else "N/A",
                    "likes": top_product.likes_count,
                }, status=status.HTTP_200_OK)
            return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # 에러 반환
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
