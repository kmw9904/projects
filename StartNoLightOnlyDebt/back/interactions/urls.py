from django.urls import path
from .views import LikeToggleView, CommentView

urlpatterns = [
    path("<str:option_type>/<str:option_id>/like/", LikeToggleView.as_view(), name="like-toggle"),
    path("<str:option_type>/<str:option_id>/comments/", CommentView.as_view(), name="comments"),
]
