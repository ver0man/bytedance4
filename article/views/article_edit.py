import mimetypes
from wsgiref.util import FileWrapper

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView

from article.forms import ArticleForm
from article.models import Images, Article


# Create your views here.
class EditorView(LoginRequiredMixin, ListView):
    model = Images
    template_name = 'editor.html'

    # TODO: Adding Ajax pagination
    paginate_by = 8
    ordering = ['-last_modified_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context


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

            return JsonResponse({'errno': 0, 'data': image_urls})

    def form_invalid(self, form):
        return JsonResponse({'errno': 1, 'data': ['']})


class CoverImageUploadView(LoginRequiredMixin, CreateView):
    model = Images
    fields = []  # did not attach name in the wangEditor.. so leave it blank here
    template_name = 'editor.html'

    def form_valid(self, form):
        # Attach the user to the form
        # form.instance.user = self.request.user
        form.save(commit=False)
        if self.request.FILES:
            # Multiple images uploaded
            image_files = self.request.FILES.getlist('cover_image')
            for image_file in image_files:
                image = Images.objects.create(image=image_file, profile=self.request.user)
                image.save()
            # TODO: After Ajax for the pagination is fixed, can redirect to that response
            return redirect('editor')

    def form_invalid(self, form):
        return redirect('editor')


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


class ArticleCRUDView(LoginRequiredMixin, FormView):
    form_class = ArticleForm
    template_name = 'editor.html'

    def form_valid(self, form):
        # Cover is needed
        if not self.request.POST['cover']:
            return JsonResponse({'message': '请先设置封面!'})

        article = form.instance
        # Attach the user to the form
        article.author = self.request.user

        # Update or create the article
        article_new, created = Article.objects.update_or_create(title=article.title, author=self.request.user,
                                                                defaults={'body': article.body, 'cover': article.cover})
        if created:
            # Return Json Response, overwrite the createview redirect return
            return JsonResponse({'message': '新文章保存成功!'})
        else:
            return JsonResponse({'message': '文章成功更新!'})

    def form_invalid(self, form):
        # TODO: Add form error messages
        return JsonResponse({'message': '保存失败!'})
