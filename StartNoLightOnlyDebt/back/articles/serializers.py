from rest_framework import serializers
from .models import Article, Comment
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    preferred_banks = serializers.StringRelatedField(many=True)  # 선호 은행 문자열로 직렬화

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'preferred_banks']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 댓글 작성자 정보를 포함

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 게시글 작성자 정보를 포함
    comments = CommentSerializer(many=True, read_only=True)  # 댓글 목록 포함
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'user', 'title', 'content', 'likes_count', 'is_liked', 'created_at', 'updated_at', 'comments']
        
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False