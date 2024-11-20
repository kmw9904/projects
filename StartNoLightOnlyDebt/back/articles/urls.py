from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),  # 게시글 목록 조회 및 생성
    path('<int:article_pk>/', views.article_detail, name='article_detail'),  # 게시글 상세 조회, 수정, 삭제
    path('<int:article_pk>/comments/', views.comment_list, name='comment_list'),  # 댓글 목록 조회 및 생성
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),  # 댓글 삭제
]
