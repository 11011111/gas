from django.forms import ModelForm

from gas.person.models import Person, Station


class NewCandidate(ModelForm):

    class Meta:
        model = Person
        exclude = ('id', )


class StationForm(ModelForm):

    class Meta:
        model = Station
        exclude = ('id', )