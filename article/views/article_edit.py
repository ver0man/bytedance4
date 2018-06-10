import pdb

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from article.models import Images


# Create your views here.


class EditorView(TemplateView):
    template_name = 'editor.html'


# @method_decorator(login_required, name='dispatch')
class ImageUploadView(CreateView):
    model = Images
    fields = []
    template_name = 'article.html'

    def form_valid(self, form):
        # Attach the user to the form
        # form.instance.user = self.request.user
        image = form.save(commit=False)
        if self.request.FILES and 'image' in self.request.FILES.keys():
            # the name 'image' is set by wangEditor API
            image.images = self.request.FILES['image']

            form.save()

        return JsonResponse({'status': 1})

    def form_invalid(self, form):
        image = form
        pdb.set_trace()


#
# class ArticleSaveView(CreateView):
#     model = Article
#     fields = ['body', ]
#
#     def form_valid(self, form):
#         article = form.save(commit=False)
#
#         pdb.set_trace()
#         pass
#
#
#     def form_invalid(self, form):
#         pdb.set_trace()
#         pass


def article_save(request):
    if request.method == 'POST':
        pdb.set_trace()
        pass
