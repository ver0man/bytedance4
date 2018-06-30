import pdb

from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.views.generic import DetailView, CreateView

from article.models import Article, Comments


# Create your views here.


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_object().comments_set.all()
        return context


# default, the quill JS store image as base 64 format. This is ok for comments.
# If later we want to upload the image to server, refer to the following post:
# https://github.com/quilljs/quill/issues/1400
# https://github.com/quilljs/quill/issues/1089
class CommentPostView(CreateView):
    model = Comments
    fields = ['comment', ]
    template_name = 'comments.html'

    def form_valid(self, form):
        # Attach the user to the form
        # form.instance.user = self.request.user
        comment = form.save(commit=False)
        comment.profile = self.request.user

        # Find articles using unique slug in the url
        url_string = self.request.path.split('/')
        comment.article = Article.objects.get(slug=url_string[url_string.index('comments') - 1])

        comment.save()

        # Return response
        return render_to_response(self.template_name, {'comments': comment.article.comments_set.all()})

    def form_invalid(self, form):
        pdb.set_trace()
        return JsonResponse({'errno': 1, 'data': ['']})
