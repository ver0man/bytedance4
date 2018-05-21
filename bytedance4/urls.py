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
from django.urls import path
from article.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # For listing all the articles
    path('', IndexView.as_view(), name='index'),

    # For articles
    path('articles/', ArticleView.as_view()),
    # For User Editing
    path('articles/editor/', EditorView.as_view(), name='editor'),


]
