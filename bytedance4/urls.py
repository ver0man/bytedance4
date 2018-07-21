"""bytedance4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path

from article.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # For user authentication
    path('accounts/', UserDetailView.as_view(), name='user_detail'),
    path('accounts/login/', user_login, name='user_login'),
    path('accounts/register/', user_register, name='user_register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='user_logout'),

    # For listing all the articles
    path('', ArticleListView.as_view(), name='index'),

    # For articles
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    # path('articles/<slug:slug>/', article_comments_view, name='article-detail'),
    # path('articles/<slug:slug>/load_comments/', article_comments_view, name='article_load_comment'),

    path('articles/<slug:slug>/post_comments/', CommentPostView.as_view(), name='article_post_comment'),

    # For User Editing
    # path('editor/', EditorView.as_view(), name='editor'),
    path('editor/', images_list, name='editor'),
    path('editor/image_upload/', ImageUploadView.as_view(), name='editor_image_upload'),
    path('editor/cover_image_upload/', CoverImageUploadView.as_view(), name='cover_image_upload'),
    path('editor/save/', ArticleCRUDView.as_view(), name='article_save'),

    # For images,
    path('images/<slug:slug>/', image_detail, name='image'),


]
