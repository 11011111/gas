from datetime import datetime

from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from gas.pages.forms import NewCandidate, StationForm
from gas.person.models import Person, User, Station, WorkTime
from datetime import timedelta 


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
    page_name = '+ Кандидат '
    if request.POST:
        form = NewCandidate(request.POST)
        user = User.objects.get(id=request.user.id)
        if user.in_group_staff_department:
            if not user.is_superuser:
                return no_access(request, 'Нет прав доступа для создания')

        if form.is_valid():
            person = form.save()
            person.status = Person.CANDIDATE
            person.save()
        else:
            print(form.errors)

    return render(request, 'pages/form.html', locals())


@login_required
def profile(request, uid):
    page_name = 'Профиль сотрудника'
    if Group.objects.get(name='Служба Безопасности') in request.user.groups.all():
        if person := Person.objects.filter(id=uid):
            person = person.first()
            return render(request, 'pages/profile.html', locals())
        if request.POST:
            pass
    return render(request, 'pages/no_access.html', locals())


@login_required
def stations_view(request):
    page_name = 'Станции'
    stations = Station.objects.all()
    return render(request, 'pages/stations.html', locals())


@login_required
def stations_view_detail(request, uid=None):
    page_name = 'Редактирование данных станции'
    station = None
    
    if uid and (station := Station.objects.filter(id=uid)):
        station = station.first()
    
    if request.POST:
        form = StationForm(request.POST, instance=station) if station else StationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/stations/')
        
    return render(request, 'pages/station_detail.html', locals())


@login_required
def work_time_view(request):
    page_name = 'График работы'
    today = datetime.now()
    dates = [today + timedelta(days=d) for d in range(14)]
    stations = Station.objects.all()
    work_times = WorkTime.objects.all()
    return render(request, 'pages/work_time.html', locals())


@login_required
def work_time_view_detail(request, uid=None):
    page_name = 'Редактирование графика'
    station = None

    if uid and (station := Station.objects.filter(id=uid)):
        station = station.first()

    if request.POST:
        form = WorkTime(request.POST, instance=station) if station else StationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/stations/')

    return render(request, 'pages/station_detail.html', locals())


