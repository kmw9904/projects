from rest_framework import serializers
from .models import Like, Comment

class LikeSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()  # 좋아요 수 추가
    
    class Meta:
        model = Like
        fields = ["id", "user", "jeonse_option", "credit_loan_option", "mortgage_option", "created_at"]

    def get_likes_count(self, obj):
        if obj.jeonse_option:
            return obj.jeonse_option.jeonse_likes.count()
        elif obj.credit_loan_option:
            return obj.credit_loan_option.credit_likes.count()
        elif obj.mortgage_option:
            return obj.mortgage_option.mortgage_likes.count()
        return 0

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "content", "jeonse_option", "credit_loan_option", "mortgage_option", "created_at"]
