from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.shortcuts import render

from article.forms import UserRegisterForm
from article.models import BaseProfile


def user_register(request):
    """
    For user login
    :param request:
    :return:
    """
    if request.method == 'POST':
        # Adding 'username' field to be the same as email
        data = request.POST.dict()
        data['username'] = data['email']
        # Use form and form_valid method
        form = UserRegisterForm(data)
        if form.is_valid():
            form.save()
            # log in user after creation
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return JsonResponse({'status': 1})
        else:
            # Construct error message in the form
            error_msg = []
            for key in form.errors.keys():
                error_msg.append('\n'.join(error_msg))

            return JsonResponse({'status': 0, 'message': '\n'.join(error_msg)})
    else:
        # TODO: add 404 page
        return render(request, 'GET404.html')


def user_login(request):
    if request.method == 'POST':

        if BaseProfile.objects.filter(email=request.POST['email']).exists():
            base_user = BaseProfile.objects.get(email=request.POST['email'])
            user = authenticate(username=base_user.username, password=request.POST['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': 0})

    # TODO: add 404 page
    return render(request, 'GET404.html')


def user_logout(request):
    pass
