from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page),
    path('form/', form_page),
    path('profile/<str:uid>/', profile),
    path('stations/', stations_view),
    path('stations/new/', stations_view_detail),
    path('stations/<str:uid>/', stations_view_detail),
    path('work_time/', work_time_view),
    path('work_time/new/', work_time_view_detail),
    path('work_time/<str:uid>/', work_time_view_detail),
]
