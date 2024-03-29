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
from graphene_django.views import GraphQLView
from rest_framework import permissions

from udigital.schema import schema
from udigital.views import list_posts, post_create, comment_create, PostListView, PostDetailView, \
    PostCreateView, CommentCreateView, post_detail

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
    path('', list_posts, name='list_posts'),
    path('post/', include([
        path('create/', post_create, name='post_create'),
        path('<int:pk>', include([
            path('', post_detail, name='post_detail'),
            path('addComment/', comment_create, name='comment_create'),
        ]))
    ])),
    path('api/', include([
        path('posts', PostListView.as_view(), name='list_posts_view'),
        path('post', include([
            path('', PostCreateView.as_view(), name='post_create_view'),
            path('/', include([
                path('<int:pk>', PostDetailView.as_view(), name='post_detail_view'),
                path('create/comment', CommentCreateView.as_view(), name='comment_create_view')
            ]))
        ]))
    ])),
    path('api/v1/swagger', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
    path('admin/', admin.site.urls)
]
