from django.forms import ModelForm

from gas.person.models import Person


class NewCandidate(ModelForm):

    class Meta:
        model = Person
        exclude = ('id', )