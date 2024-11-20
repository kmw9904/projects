from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 요청한 사용자로 게시글 작성
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=200)

    elif request.method == 'PUT':
        if article.user != request.user:  # 작성자 확인
            return Response({'message': '권한이 없습니다.'}, status=403)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if article.user != request.user:
            return Response({'message': '권한이 없습니다.'}, status=403)
        article.delete()
        return Response({'message': '게시글이 삭제되었습니다.'}, status=204)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = Comment.objects.filter(article=article).order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, article_id=article_pk)

    if comment.user != request.user:  # 작성자 확인
        return Response({'message': '권한이 없습니다.'}, status=403)
    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'}, status=204)
