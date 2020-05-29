from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

# Create your views here.
from gas.pages.forms import NewCandidate
from gas.person.models import Person


def main_page(request):
    persons = Person.objects.filter(status=Person.CANDIDATE)

    if request.GET and (q := request.GET.get('search', '')):
        persons = persons.filter(last_name__icontains=q)

    return render(request, 'pages/main.html', locals())
    # return redirect('/auth/login/')


def form_page(request):
    if request.POST:
        form = NewCandidate(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return render(request, 'pages/form.html', locals())


def profile(request, uid):
    if Group.objects.get(name='Служба Безопасности') in request.user.groups.all():
        if person := Person.objects.filter(id=uid):
            person = person.first()
            return render(request, 'pages/profile.html', locals())
        if request.POST:
            pass
    return render(request, 'pages/no_access.html', locals())

