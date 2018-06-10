from django.views.generic import TemplateView


# Create your views here.


class ArticleView(TemplateView):
    template_name = 'article.html'


def article_list(request):
    # user = request.user
    #
    # score = some_function(user)
    #
    # article = Article.objects.filter(labels__in=label_list)
    #
    # return
    pass
