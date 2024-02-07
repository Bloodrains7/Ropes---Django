from rest_framework import serializers

from udigital.models import Post, User, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['user', 'comment', 'timestamp']


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'comments']


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Post
        fields = ['title', 'content', 'author_id', 'publication_date']


class CommentCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['user_id', 'post_id', 'comment']
