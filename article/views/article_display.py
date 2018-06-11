from django.views.generic import ListView

from article.models import Article


# Create your views here.


class ArticleListView(ListView):
    model = Article
    template_name = 'article.html'

    # paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context
