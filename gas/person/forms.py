from django import forms
from django.contrib.auth import authenticate

from .models import User, Person
from .validators import user_password


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(min_length=2, max_length=5, required=True)
    password = forms.CharField(min_length=8, max_length=30, validators=[user_password],
                                   widget=forms.PasswordInput)

    def save(self):
        user = User.objects.create_user(self.cleaned_data['email'], self.cleaned_data['password'])
        Person.objects.create(user=user, first_name=self.cleaned_data['first_name'])
        user = authenticate(email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        # login(request, user)

        return user


class AnonymousResetPasswordForm(forms.Form):
    """
    Форма востановления пароля с эл. почтой для пользователя, который не произвел вход
    Пример: Пользователь забыл пароль и не может войти
    """
    email = forms.EmailField(required=True)


class LinkResetPasswordForm(forms.Form):
    """
    Форма изменения пароля после перехода по ссылке из письма полученого после
    выполнения AnonymousResetPasswordForm
    """
    new_password = forms.CharField(min_length=8, max_length=30, validators=[user_password],
                                   widget=forms.PasswordInput)
    conf_password = forms.CharField(min_length=8, max_length=30, validators=[user_password],
                                   widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        conf_password = cleaned_data.get("conf_password")

        if new_password and conf_password:
            if new_password != conf_password:
                raise forms.ValidationError({'new_password': 'Passwords is not equal'})
        else:
            raise forms.ValidationError({'conf_password': 'Confirm your password'})


class UserResetPasswordForm(forms.Form):
    """
    Форма восстановления пароля и непосредственного его изменения из учетной записи
    после подтвержения действующего пароля
    """
    old_password = forms.CharField(min_length=8, max_length=30, validators=[user_password],
                                   widget=forms.PasswordInput)
    new_password = forms.CharField(min_length=8, max_length=30, validators=[user_password],
                                   widget=forms.PasswordInput)




class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, max_length=30, validators=[user_password],
                                   widget=forms.PasswordInput)