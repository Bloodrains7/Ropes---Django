from django.shortcuts import render, redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from udigital.forms import PostForm, CommentForm
from udigital.models import Post, Comment
from udigital.serializer import PostListSerializer, PostDetailSerializer, PostCreateSerializer, CommentCreateSerializer
from udigital.swagger import accept_language, posts_response, success_response, post_response, id_param, \
    create_post_request, create_comment_request


def list_posts(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/list.html', context)


def detail_post(request, post_id):
    post = Post.objects.all()
    context = {'post': post}
    return render(request, 'posts/details.html', context)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_posts')
        else:
            form = PostForm()
        context = {'form': form}
        return render(request, 'posts/add.html', context)


def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('list_posts')
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'posts/edit.html', context)


def create_comment(request):
    if request.method == 'POST':
        form = CommentForm(request)
        if form.is_valid():
            form.save()
            return redirect('post')
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'posts/details.html', context)


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    @swagger_auto_schema(tags=['Posts'], operation_description='Get Posts',
                         manual_parameters=[accept_language],
                         responses={200: posts_response})
    def get(self, request, *args, **kwargs):
        return super(PostListView, self).get(request, *args, **kwargs)


class PostDetailView(APIView):

    @swagger_auto_schema(tags=['Post'], operation_description='Get Post',
                         manual_parameters=[accept_language, id_param],
                         responses={200: post_response})
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)


class PostCreateView(APIView):

    @swagger_auto_schema(tags=['Post'], operation_description='Create Post',
                         manual_parameters=[accept_language],
                         request_body=create_post_request,
                         responses={201: success_response})
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentCreateView(APIView):

    @swagger_auto_schema(tags=['Post'], operation_description='Create Comment to Post',
                         manual_parameters=[accept_language],
                         request_body=create_comment_request,
                         responses={201: success_response})
    def post(self, request):
        print(request)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
