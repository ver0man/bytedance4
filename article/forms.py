from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from article.models import *


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = BaseProfile
        fields = ('username', 'email', 'password1', 'password2',)


class ImageUploadForm(ModelForm):
    class Meta:
        model = Images
        fields = ['images', ]


class ArticleSaveForm(ModelForm):
    class Meta:
        model = Article
        fields = ['body', ]
