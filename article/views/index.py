import mimetypes
import os
import re
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.files.images import ImageFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from article.forms import UserRegisterForm
from article.models import BaseProfile, Images


def user_register(request):
    """
    For user login
    :param request:
    :return:
    """
    if request.method == 'POST':
        # Adding 'username' field to be the same as email
        data = request.POST.dict()
        # Use form and form_valid method
        form = UserRegisterForm(data)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.headshot = ImageFile(open(os.path.join(settings.MEDIA_ROOT, 'headshot-default.jpg'), "rb"))

            user_obj.save()
            # log in user after creation
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return JsonResponse({'status': 1})
        else:
            return JsonResponse(form.errors.as_json(), safe=False)

    else:
        return render(request, 'GET404.html')


def user_login(request):
    if request.method == 'POST':
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if BaseProfile.objects.filter(email=request.POST['email']).exists():
            if re.match(email_regex, request.POST['email']):
                base_user = BaseProfile.objects.get(email=request.POST['email'])
            else:
                base_user = BaseProfile.objects.get(username=request.POST['email'])

            # Authenticate the user
            user = authenticate(username=base_user.username, password=request.POST['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': 0})

    return render(request, 'GET404.html')


def user_logout(request):
    pass


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


class TermsView(TemplateView):
    template_name = 'terms.html'
