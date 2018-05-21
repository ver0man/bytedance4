from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class EditorView(TemplateView):
    template_name = 'editor.html'
