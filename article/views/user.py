from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView, ListView

from article.forms import UserUpdateForm
from article.models import BaseProfile, Article


# class UserDetailView(LoginRequiredMixin, DetailView):
#     model = BaseProfile
#     template_name = 'accounts.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['now'] = timezone.now()
#         return context


class UserDetailView(LoginRequiredMixin, TemplateView):
    model = BaseProfile
    template_name = 'accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context


class UserArticlesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'account_article.html'

    paginate_by = 8  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class UserUpdateView(LoginRequiredMixin, FormView):
    form_class = UserUpdateForm
    template_name = 'accounts.html'

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
        return JsonResponse({'message': '保存失败!'})
