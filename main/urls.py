from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("student", views.student, name="student"),
    path("supervisor", views.supervisor, name="supervisor"),
    path("login", views.login_view, name="login"),
]