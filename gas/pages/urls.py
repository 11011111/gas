from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page),
    path('form/', form_page),
    path('profile/<str:uid>/', profile),
]
