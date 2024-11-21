from rest_framework import serializers
from .models import CreditComment, JeonseComment, MortgageComment

class CreditCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditComment
        fields = ['id', 'user', 'product', 'content', 'created_at']

class JeonseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JeonseComment
        fields = ['id', 'user', 'product', 'content', 'created_at']

class MortgageCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageComment
        fields = ['id', 'user', 'product', 'content', 'created_at']
