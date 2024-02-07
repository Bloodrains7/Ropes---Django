from django.shortcuts import render, redirect

from udigital.forms import PostForm, CommentForm
from udigital.models import Post, Comment


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
