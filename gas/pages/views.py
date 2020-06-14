from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from gas.pages.forms import NewCandidate
from gas.person.models import Person, User


def no_access(request, error):
    return render(request, 'pages/no_access.html', locals())

@login_required
def main_page(request):
    persons = Person.objects.filter(status=Person.CANDIDATE)

    if request.GET and (q := request.GET.get('search', '')):
        persons = persons.filter(last_name__icontains=q)

    return render(request, 'pages/main.html', locals())


@login_required
def form_page(request):
    if request.POST:
        form = NewCandidate(request.POST)
        user = User.objects.get(id=request.user.id)
        if not user.in_group_staff_department:
            return no_access(request, 'Нет прав доступа для создания')

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return render(request, 'pages/form.html', locals())


@login_required
def profile(request, uid):
    if Group.objects.get(name='Служба Безопасности') in request.user.groups.all():
        if person := Person.objects.filter(id=uid):
            person = person.first()
            return render(request, 'pages/profile.html', locals())
        if request.POST:
            pass
    return render(request, 'pages/no_access.html', locals())

