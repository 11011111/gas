from django.conf import settings
from django.forms import ModelForm, DateField

from gas.person.models import Person


class CandidateForm(ModelForm):
    birth_date = DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False)
    passport_date = DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = Person
        exclude = ('DTC', )