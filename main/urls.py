from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("student", views.student, name="student"),
    path("student-login", views.student_login_view, name="studentlog"),
    path("student-dashboard", views.student_dashboard, name="studentdash"),
    path("student_attendance", views.student_attendance, name="studentattendance"),
    path("supervisor", views.supervisor, name="supervisor"),
    path("supervisor-login", views.supervisor_login_view, name="supervisorlog"),
    path("supervisor-dashboard", views.supervisor_dashboard, name="supervisordash"),
    path("supervisor-dashboard/add-student", views.supervisor_add_student, name="addstudent"),
    # path("student_attendance/view/<int:id>", views.student_view_attendance, name="attendance"),
    path("supervisor-dashboard/add-student/connect/<int:id>", views.supervisor_connect_student, name="connect"),
    path("supervisor-dashboard/add-student/delete/<int:id>", views.supervisor_delete_student, name="delete"),
    path("supervisor/view-attendance/<int:id>", views.supervisor_view_attendance, name="viewattendance"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]