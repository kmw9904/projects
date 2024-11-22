from django.urls import path
from .views import LikeToggleView, CommentView, TopLikedProductsView

urlpatterns = [
    path("<str:option_type>/<str:option_id>/like/", LikeToggleView.as_view(), name="like-toggle"),
    path("<str:option_type>/top-liked/", TopLikedProductsView.as_view(), name="top-liked-products"),
    path("<str:option_type>/<str:option_id>/comments/", CommentView.as_view(), name="comments"),
    path('<str:option_type>/<str:option_id>/comments/<int:comment_id>/delete/', CommentView.as_view()),
]
