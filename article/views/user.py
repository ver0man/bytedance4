from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from article.models import BaseProfile


class UserDetailView(LoginRequiredMixin, DetailView):
    model = BaseProfile
    template_name = 'accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context

