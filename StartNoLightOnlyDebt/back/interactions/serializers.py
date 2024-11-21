from rest_framework import serializers
from .models import Like, Comment

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "jeonse_option", "credit_loan_option", "mortgage_option", "created_at"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "content", "jeonse_option", "credit_loan_option", "mortgage_option", "created_at"]
