from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from catalog.forms import StyleFormMixin


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введите ваш email'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Введите пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Подтвердите пароль'
        })
