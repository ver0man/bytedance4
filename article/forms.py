from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from article.models import *


def validate_unique_email(email):
    obj = BaseProfile.objects.filter(email=email)
    if obj:
        raise ValidationError(
            _('Email already exists.'),
        )


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = BaseProfile
        fields = ('username', 'email', 'password1', 'password2',)

    username = forms.CharField(validators=[MinLengthValidator(2, 'Username must have more than 2 characters'),
                                           MaxLengthValidator(16, 'Username must have less than 16 characters')])
    email = forms.EmailField(validators=[EmailValidator, validate_unique_email])


class UserUpdateForm(UserCreationForm):
    class Meta:
        model = BaseProfile
        fields = ('username', 'email', 'password1', 'password2',)

    username = forms.CharField(validators=[MinLengthValidator(2, 'Username must have more than 2 characters'),
                                           MaxLengthValidator(16, 'Username must have less than 16 characters')])
    email = forms.EmailField(validators=[EmailValidator, ])


class ImageUploadForm(ModelForm):
    class Meta:
        model = Images
        fields = ['image', ]


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'cover', ]
