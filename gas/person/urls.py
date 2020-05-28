from django.urls import path
from .views import Login, Registration, Logout, EmailConfirm, ResetPassword, LinkResetPassword

urlpatterns = [
    path('login/', Login.as_view()),
    path('registration/', Registration.as_view()),
    path('logout/', Logout.as_view()),
    path('confirm_email/', EmailConfirm.as_view()),
    path('confirm_email/<uuid:code>/', EmailConfirm.as_view()),
    path('reset_password/', ResetPassword.as_view()),
    path('reset_password/<uuid:code>/', LinkResetPassword.as_view())
]
