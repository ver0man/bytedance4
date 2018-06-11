from django.views.generic import DetailView

from article.models import Article


# Create your views here.


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context


def article_list(request):
    # user = request.user
    #
    # score = some_function(user)
    #
    # article = Article.objects.filter(labels__in=label_list)
    #
    # return
    pass
