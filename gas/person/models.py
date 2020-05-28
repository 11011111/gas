from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db.models import CharField, OneToOneField, PROTECT, BooleanField, EmailField, ForeignKey, FileField
from django.utils.translation import gettext_lazy as _

from gas.utils.model_mixins import BaseModelMixin


class CustomUserManager(UserManager):
    """
    Переписанные методы для создания пользователя без использование поля username
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Эл.почта должна быть указана обязательно')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_email_verify', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModelMixin):
    # Переназначение контекстного менеджера
    objects = CustomUserManager()
    REQUIRED_FIELDS = []  # Обязательные поля для пользователя
    USERNAME_FIELD = 'email'  # В качестве логина используется эл.почта пользователя
    email = EmailField(_('email address'), unique=True)
    is_email_verify = BooleanField('Email подтвержден', default=False)
    # Поля имя и фамилии переносятся в модель Person
    first_name = None
    last_name = None
    # username пока не используется
    username = CharField(_('username'), max_length=30, blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Person(BaseModelMixin):
    first_name = CharField('Имя', max_length=50)
    last_name = CharField('Фамилия', max_length=50)
    middle_name = CharField('Отчество', max_length=50, default='', blank=True)
    user = OneToOneField(User, verbose_name='Пользователь', on_delete=PROTECT, related_name='person')

    passport_number = CharField('Паспорт', max_length=10, null=True, blank=True)

    WORKED = 'Работает'
    FIRED = 'Уволен'
    CANDIDATE = 'Кандидат'
    REFUSED = 'Отклонен'

    STATUSES = (
        (WORKED, 'Работает'),
        (FIRED, 'Уволен'),
        (CANDIDATE, 'Кандидат'),
        (REFUSED, 'Отклонен'),
    )

    status = CharField('Статус', max_length=10, null=True, blank=True)

    station = ForeignKey('Station', verbose_name='Станция', on_delete=PROTECT, related_name='persons', null=True,
                         blank=True)

    def save_to_path(self, filename):
        valid_extensions = ['pdf', ]
        ext = filename.rsplit('.', 1)[1]
        if ext.lower() in valid_extensions:
            raise ValidationError('Unsupported file extension.')
        return f'documents/{self.user.email.split("@")[0].lower()}.{ext}'

    document_file = FileField(upload_to=save_to_path, verbose_name='Файл документа', null=True, blank=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'.strip()

    @property
    def short_name(self):
        return f'{self.first_name} {self.last_name[0]}. {self.middle_name[0]}.'

    class Meta:
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')


class Station(BaseModelMixin):
    address = CharField('Адрес', max_length=150)
    phone = CharField('Телефон', max_length=15)


    class Meta:
        verbose_name = _('Станция')
        verbose_name_plural = _('Станции')
