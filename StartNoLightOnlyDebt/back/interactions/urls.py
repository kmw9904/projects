from django.urls import path
from . import views

urlpatterns = [
    # 개인대출 좋아요와 댓글
    path('credit/<str:product_id>/likes/', views.get_credit_likes, name='get_credit_likes'),
    path('credit/<str:product_id>/likes/toggle/', views.toggle_credit_like, name='toggle_credit_like'),
    path('credit/<str:product_id>/comments/', views.get_credit_comments, name='get_credit_comments'),
    path('credit/<str:product_id>/comments/add/', views.add_credit_comment, name='add_credit_comment'),

    # 전세대출 좋아요와 댓글
    path('jeonse/<str:product_id>/likes/', views.get_jeonse_likes, name='get_jeonse_likes'),
    path('jeonse/<str:product_id>/likes/toggle/', views.toggle_jeonse_like, name='toggle_jeonse_like'),
    path('jeonse/<str:product_id>/comments/', views.get_jeonse_comments, name='get_jeonse_comments'),
    path('jeonse/<str:product_id>/comments/add/', views.add_jeonse_comment, name='add_jeonse_comment'),

    # 담보대출 좋아요와 댓글
    path('mortgage/<str:product_id>/likes/', views.get_mortgage_likes, name='get_mortgage_likes'),
    path('mortgage/<str:product_id>/likes/toggle/', views.toggle_mortgage_like, name='toggle_mortgage_like'),
    path('mortgage/<str:product_id>/comments/', views.get_mortgage_comments, name='get_mortgage_comments'),
    path('mortgage/<str:product_id>/comments/add/', views.add_mortgage_comment, name='add_mortgage_comment'),
]
