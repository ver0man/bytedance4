import mimetypes
import pdb
from wsgiref.util import FileWrapper

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from article.models import Images, Article


# Create your views here.


class EditorView(LoginRequiredMixin, TemplateView):
    template_name = 'editor.html'


# @method_decorator(login_required, name='dispatch')
class ImageUploadView(LoginRequiredMixin, CreateView):
    model = Images
    fields = []  # did not attach name in the wangEditor.. so leave it blank here
    template_name = 'article.html'

    def form_valid(self, form):
        # Attach the user to the form
        # form.instance.user = self.request.user
        form.save(commit=False)
        if self.request.FILES:
            # Multiple images uploaded
            image_urls = []
            for name, image_file in self.request.FILES.items():
                image = Images.objects.create(image=image_file, profile=self.request.user)
                image.save()
                image_urls.append('/images/' + image.slug)
            #
            return JsonResponse({'errno': 0, 'data': image_urls})

    def form_invalid(self, form):
        pdb.set_trace()
        return JsonResponse({'errno': 1, 'data': ['']})


@login_required
def image_detail(request, slug):
    """
    Return images url to be rendered in the editor area
    :param request:
    :param slug:
    :return:
    """
    if request.method == 'GET':
        # Get image object
        image = get_object_or_404(Images, slug=slug)
        # ImageField is File object, can be open
        wrapper = FileWrapper(image.image.open())
        # Use mimetypes to get file type
        content_type = mimetypes.guess_type(str(image))[0]
        # Return image response
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = image.image.size
        response['Content-Disposition'] = "attachment; filename={}".format(str(image))
        return response


class ArticleSaveView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'body', ]

    def form_valid(self, form):
        # Attach the user to the form
        form.instance.author = self.request.user
        form.save()
        # Return Json Response, overwrite the createview redirect return
        return JsonResponse({'message': '保存成功!'})

    def form_invalid(self, form):
        pdb.set_trace()
        return JsonResponse({'message': '保存成功!'})
