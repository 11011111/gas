from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, AnonymousResetPasswordForm, UserResetPasswordForm, LoginForm, LinkResetPasswordForm
from uuid import uuid4
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail
from .models import User
from collections import namedtuple


def send_confirm_email(user):
    """
    Метод отправки эл.письма с сылкой подтверждения эл.адреса
    :param user: экземпляр пользователя
    """
    code = uuid4()  # Создаем уникальный uuid4-код
    # Записываем код в кэш (Redis) в качестве ключа, а в качестве значения id пользователя
    # с периодом действия указанным в настройках
    cache.set(f'conf_{code}', user.id, settings.EMAIL_CODE_PERIOD)
    # Генерируем ссылку по которой должен перейти пользователь для подтверждения эл.адреса
    url = f'{settings.HOST_URL}auth/confirm_email/{code}/'
    link = f'<a href="{url}">Confirm</a>'
    # Отправка письма с ссылкой на подтверждение эл.адреса
    send_mail('Confirm your email', url, settings.EMAIL_HOST_USER, [user.email])


def send_resetpass_email(user):
    """
    Метод отправки эл.письма с сылкой сброс пароля
    :param user: экземпляр пользователя
    """
    code = uuid4()  # Создаем уникальный uuid4-код
    # Записываем код в кэш (Redis) в качестве ключа, а в качестве значения id пользователя
    # с периодом действия указанным в настройках
    cache.set(f'rpass_{code}', user.id, settings.EMAIL_CODE_PERIOD)
    # Генерируем ссылку по которой должен перейти пользователь для подтверждения эл.адреса
    url = f'{settings.HOST_URL}auth/reset_password/{code}/'
    link = f'<a href="{url}">Reset Password</a>'
    # Отправка письма с ссылкой на сброс пароля
    send_mail('Reset your password', url, settings.EMAIL_HOST_USER, [user.email])


class to_obj(object):
    def init(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [to_obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, to_obj(b) if isinstance(b, dict) else b)


class Registration(View):
    """
    View регистрации нового пользователя
    get: метод рендеринга шаблона для регистрации
    post: метод создания нового пользователя
    """

    def get(self, request, **kwargs):
        # Если пользователь уже произвел вход перадресовываем его на главную страницу
        if user := request.user:
            if user.is_authenticated:
                return redirect('/')
        form = RegistrationForm()  # Создание экземпляра формы для последующего рендеринга
        return render(request, 'person/registration.html', locals())

    def post(self, request):
        # Если пользователь уже произвел вход перадресовываем его на главную страницу
        if user := request.user:
            if user.is_authenticated:
                return redirect('/')
        form = RegistrationForm(request.POST)  # Заполняем форму данными пользователя
        other_error = []
        if form.is_valid():  # Проверка на валидность полученных данных от пользователя
            if not User.objects.filter(email=form.cleaned_data['email']):
                user = form.save()  # Создаем пользователя
                login(request, user)  # Выполняем автоматический вход
                send_confirm_email(user)  # Отсылаем письмо с подтверждением эл.почты
                return redirect('/')
            else:
                other_error.append('A user with this email has already been created.')
        else:
            # В случаем невалидной формы рендерим новую форму, но с данными, которые он ввел прежде
            other_error.append('Email, name or password is not correct.')
        errors = to_obj()
        form.errors['other'] = other_error
        errors.init(form.errors)
        return render(request, 'person/registration.html', locals())


class Login(View):

    def get(self, request):
        # Отображение страницы входа
        form = LoginForm()
        if user := request.user:
            if user.is_authenticated:
                return redirect('/')
        return render(request, 'person/login.html', locals())

    def post(self, request):

        form = LoginForm(request.POST)
        other_error = []
        wc = 0
        if form.is_valid():
            w = f'wrong_{form.cleaned_data["email"]}'
            wc = cache.get(w) or 0
            if wc > settings.BAD_PASSWORD_MAX_COUNT:
                # other_error.append('Password is not correct. Try again later.')
                return redirect('/auth/reset_password/')
            if user := authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password']):
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    other_error.append('User is not active.')
            else:
                cache.set(w, wc + 1, settings.BAD_PASSWORD_TIMEOUT)
                other_error.append('Email or password is not correct.')

        errors = to_obj()
        form.errors['other'] = other_error
        errors.init(form.errors)
        if wc < 5:
            return render(request, 'person/login.html', locals())
        else:
            return render(request, 'person/reset_password.html', locals())


class Logout(View):
    # Выход пользователя из учетной записи
    def get(self, request):
        logout(request)
        return redirect(to='/')


class EmailConfirm(View):
    """
    View обработки подтверждения эл.адреса
    get: пользователь переходит по ссылке из письма и производится проверка кода подтверждения
    post: метод для повтороной отправки письма, если по каким-либо причинам он его не получил
    """

    def get(self, request, code=None):
        print('Hello')
        if user_id := cache.delete(f'conf_{code}'):  # Ищем по ключу id пользователя
            user = User.objects.get(id=user_id)  # Ищем пользователя по id
            user.is_email_verify = True  # Выставлем флаг, что эл.адрес подтвержден
            user.save()  # Сохраняем пользователя
        return redirect(to='/')

    def post(self, request, code=None):
        # Повторная отправка
        send_confirm_email(request.user)
        return redirect('/')


class ResetPassword(View):

    def get(self, request):
        form = UserResetPasswordForm() if request.user.is_authenticated else AnonymousResetPasswordForm()
        return render(request, 'person/reset_password.html', locals())

    def post(self, request):
        data = request.POST
        form = UserResetPasswordForm(data) if 'old_password' in data.keys() else AnonymousResetPasswordForm(data)
        if isinstance(form, UserResetPasswordForm):
            # Проверяем старый пароль, если он верный - меняем его на новый
            user = request.user
            if form.is_valid():
                u = authenticate(email=user.email, password=form.cleaned_data['old_password'])
                if u:
                    u.set_password(form.cleaned_data['new_password'])
                    u.save()
                    return redirect('/')
                else:
                    return render(request, 'person/reset_password.html', locals())
            else:
                return render(request, 'person/reset_password.html', locals())
        elif isinstance(form, AnonymousResetPasswordForm):
            if form.is_valid():
                user = User.objects.get(email=form.data['email'])
                if user:
                    send_resetpass_email(user)
                    return redirect('/')
                else:
                    return render(request, 'person/reset_password.html', locals())
            else:
                return render(request, 'person/reset_password.html', locals())
        else:
            return render(request, 'person/reset_password.html', locals())


class LinkResetPassword(View):

    def get(self, request, code=None):
        user_id = cache.get(f'rpass_{code}')  # Ищем по ключу id пользователя и удаляем его из кэша
        user = User.objects.get(id=user_id)  # Ищем пользователя по id
        if user:
            form = LinkResetPasswordForm()
            return render(request, 'person/reset_password.html', locals())
        else:
            return redirect('/')

    def post(self, request, code=None):
        form = LinkResetPasswordForm(request.POST)
        if form.is_valid():
            user_id = cache.get(f'rpass_{code}')  # Ищем по ключу id пользователя
            user = User.objects.get(id=user_id)  # Ищем пользователя по id
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            cache.delete(f'rpass_{code}')
            return redirect('/auth/login/')
        else:
            return render(request, 'person/reset_password.html', locals())
