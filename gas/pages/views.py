from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from gas.pages.forms import CandidateForm
from gas.person.models import Person


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
        form = CandidateForm(request.POST)
        # if not request.user.in_staff_department:
        #     return no_access(request, 'Нет прав доступа для создания')

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return render(request, 'pages/form.html', locals())


@login_required
def profile(request, uid):

    if request.POST and (person := Person.objects.filter(id=uid)):
        person = person.first()
        form = CandidateForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('/')

    person = Person.objects.get(id=uid)
    return render(request, 'pages/profile.html', locals())

