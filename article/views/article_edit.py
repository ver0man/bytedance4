from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, FormView
from el_pagination.decorators import page_template

from article.forms import ArticleForm
from article.models import Images, Article


# For listing cover images ajax view
@page_template('images_list.html')  # just add this decorator
def images_list(request, template='editor.html', extra_context=None):
    context = {
        'images_list': Images.objects.all().order_by('-last_modified_time', ),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


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
