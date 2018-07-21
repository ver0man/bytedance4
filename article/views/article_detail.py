import pdb

from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.views.generic import DetailView, CreateView

from article.models import Article, Comments


# TODO: Add comment pagination
# # For listing cover images ajax view
# @page_template('comments.html')  # just add this decorator
# def article_comments_view(request, template='comments.html', extra_context=None, **kwargs):
#     if 'slug' in kwargs.keys():
#         article = Article.objects.get(slug=kwargs['slug'])
#     else:
#         return render(request, 'GET404.html')
#
#     # Build context
#     context = {
#         'comments': article.comments_set.all().order_by('-comment_time', ),
#     }
#     pdb.set_trace()
#     if extra_context is not None:
#         context.update(extra_context)
#     return render(request, template, context)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # All comments
        article = self.get_object()
        comments = article.comments_set.all().order_by('-comment_time')

        context['comments'] = comments
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
        comment.article = Article.objects.get(slug=url_string[url_string.index('post_comments') - 1])

        # Find parent comment if exist
        if 'parent' in self.request.POST.keys():
            comment.parent_comment = Comments.objects.get(pk=int(self.request.POST['parent']))

        # Save instance
        comment.save()

        # Return response
        results = {'comments': comment.article.comments_set.all().order_by('-comment_time')}

        return render_to_response(self.template_name, results)

    def form_invalid(self, form):
        # TODO: Edit error message
        pdb.set_trace()
        return JsonResponse({'errno': 1, 'data': ['']})
