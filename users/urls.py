from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, custom_logout, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(
        template_name="login.html"), name="login"),
    path("logout/", custom_logout, name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
]
