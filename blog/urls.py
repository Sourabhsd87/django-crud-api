from django.urls import path
from .views import (
    PostListAPIView,
    PostUpdateAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostCreateAPIView,
    CategoryCreateAPIView,
    CategoryListAPIView,
    CommentListAPIView,
    CommentCreateAPIView,
)

urlpatterns = [
    path("posts/", PostListAPIView.as_view(), name="post-list"),
    path("post/create/", PostCreateAPIView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailAPIView.as_view(), name="post-detail"),
    path("posts/update/<int:pk>/", PostUpdateAPIView.as_view(), name="post-update"),
    path("posts/delete/<int:pk>/", PostDeleteAPIView.as_view(), name="post-delete"),
    path("posts/comments/<int:post_id>/",CommentListAPIView.as_view(),name='comment-list'),
    path("posts/comment/create/<int:post_id>/",CommentCreateAPIView.as_view(),name='comment-create'),
    path("category/", CategoryListAPIView.as_view(), name="category-list"),
    path("category/create/", CategoryCreateAPIView.as_view(), name="category-create"),
]