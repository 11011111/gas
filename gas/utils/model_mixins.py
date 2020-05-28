from django.db.models import UUIDField, Model, DateTimeField
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


class BaseMixin(Model):
    """Базовые действия для объектов класса и модели"""

    def clean(self, *args, **kwargs):
        # add custom validation here
        super(BaseMixin, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(BaseMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class UidMixin(BaseMixin):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampMixin(BaseMixin):
    DTC = DateTimeField(verbose_name=_('Дата создания'), null=True, blank=True, auto_now_add=True, editable=False)
    DTU = DateTimeField(verbose_name=_('Дата обновления'), null=True, blank=True, auto_now=True, editable=False)

    class Meta:
        abstract = True


class BaseModelMixin(TimeStampMixin, UidMixin):
    class Meta:
        abstract = True
