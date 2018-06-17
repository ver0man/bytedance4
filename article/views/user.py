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

# def user_register(request):
#     """
#     For user login
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         # Adding 'username' field to be the same as email
#         data = request.POST.dict()
#         data['username'] = data['email']
#         # Use form and form_valid method
#         form = UserRegisterForm(data)
#         if form.is_valid():
#             form.save()
#             # log in user after creation
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return JsonResponse({'status': 1})
#         else:
#             # Construct error message in the form
#             error_msg = []
#             for key in form.errors.keys():
#                 error_msg.append('\n'.join(error_msg))
#
#             return JsonResponse({'status': 0, 'message': '\n'.join(error_msg)})
#     else:
#         # TODO: add 404 page
#         return render(request, 'GET404.html')
