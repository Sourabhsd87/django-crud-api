from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import (
    PostListSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PostDetailSerializer,
)

# class PostListCreateAPIView(APIView):
#     """
#     API to list all Posts and create a new Post
#     """
#     def get(self,request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self,request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class PostGetUpdateDeleteAPIView(APIView):
#     """
#     API to get, update and delete a Post
#     """
#     def get(self,request,pk):
#         post = get_object_or_404(Post, pk=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self,request,pk):
#         post = get_object_or_404(Post,pk=pk)
#         serializer = PostSerializer(post,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self,request,pk):
#         post = get_object_or_404(Post,pk=pk)
#         post.delete()
#         return Response({"message":"Post deleted successfully"},status=status.HTTP_204_NO_CONTENT)

# GET all posts
class PostListAPIView(APIView):
    """
    API to list all Posts
    """
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    
class PostCreateAPIView(APIView):
    """
    API to create a new Post
    """
    def post(self,request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetailAPIView(APIView):
    """
    API to get details of a Post
    """
    def get(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class PostUpdateAPIView(APIView):
    """
    API to update a Post
    """
    def put(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        serializer = PostUpdateSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(seralizer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDeleteAPIView(APIView):
    """
    API to delete a Post
    """
    def delete(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        post.delete()
        return Response({"message":"Post deleted successfullly"},status=status.HTTP_204_NO_CONTENT)
        