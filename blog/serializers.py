from rest_framework import serializers
from .models import Post, Category, Comment


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "text", "created_date"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "author", "text"]


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "text", "created_date"]


# ---------------------------------------------------------------------------


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "published_date"]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "text", "author"]


class PostDetailSerializer(serializers.ModelSerializer):

    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["author", "title", "text", "category", "created_date", "comments"]


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


# -------------------------------------------------------------------------------------------------------
