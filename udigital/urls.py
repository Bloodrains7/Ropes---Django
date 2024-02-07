"""
URL configuration for udigital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework import permissions

from udigital.views import list_posts, create_post, edit_post, create_comment, PostListView, PostDetailView, \
    PostCreateView, CommentCreateView

schema_view = swagger_get_schema_view(
    openapi.Info(
        title='u.Digital API',
        default_version='1.1.0',
        description='API documentation of App'
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('posts/', list_posts, name='list_posts'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/<int:pk>/edit/', edit_post, name='edit_post'),
    path('posts/<int:pk>/addComment/', create_comment, name='create_comment'),
    path('api/', include([
        path('posts', PostListView.as_view()),
        path('post', include([
            path('', PostCreateView.as_view()),
            path('/', include([
                path('<int:pk>', PostDetailView.as_view()),
                path('create/comment', CommentCreateView.as_view())
            ]))
        ]))
    ])),
    path('api/v1/swagger', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path('admin/', admin.site.urls)
]
