from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class ArticleView(TemplateView):
    template_name = 'article.html'
