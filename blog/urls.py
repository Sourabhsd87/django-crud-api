from django.urls import path
from .views import (
    PostListAPIView,
    PostUpdateAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostCreateAPIView
)

urlpatterns = [
    path('posts/',PostListAPIView.as_view(),name='post-list'),
    path('post/create/',PostCreateAPIView.as_view(),name='post-create'),
    path('posts/<int:pk>/',PostDetailAPIView.as_view(),name='post-detail'),
    path('posts/<int:pk>/update/',PostUpdateAPIView.as_view(),name='post-update'),
    path('posts/<int:pk>/delete/',PostDeleteAPIView.as_view(),name='post-delete'),
]