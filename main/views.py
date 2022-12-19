from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .models import User, Student
from sqlite3 import IntegrityError

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def login_view(request):

    if request.method == "GET":
        return render(request, "main/dashbardlog.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect(reverse("dashboard"))

            if user.is_student:
                return HttpResponse("You have no accesss to admin portal")

            if user.is_supervisor:
                return HttpResponse("You have no accesss to admin portal")

            #TODO: Create and return no access page
        else:
            return HttpResponseRedirect(reverse("login"))


def student_login_view(request):

    if request.method == "GET":
        return render(request, "main/studentlog.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return HttpResponse("You have no accesss to student portal")
            
            if user.is_student:
                return HttpResponseRedirect(reverse("studentdash"))

            if user.is_supervisor:
                return HttpResponse("You have no accesss to student portal")
        else:
            return HttpResponseRedirect(reverse("index"))


def supervisor_login_view(request):

    if request.method == "GET":
        return render(request, "main/supervisorlog.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return HttpResponse("You have no accesss to supervisor portal")
            
            if user.is_student:
                return HttpResponse("You have no accesss to supervisor portal")

            if user.is_supervisor:
                return HttpResponse("Success")
        else:
            return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def dashboard(request):
    return render(request, 'main/admin/admin.html', {
        "page": "dashboard"
    })

def student_dashboard(request):
    if request.method == "GET":
        data = Student.objects.get(pk=request.user.id)
        return render(request, "main/student/dashboard.html", {
            "page": "students",
            "data": data
        })

def student_attendance(request):
    if request.method == "GET":
        data = Student.objects.get(pk=request.user.id)
        pass


def student(request):
    if request.method == "GET":
        return render(request, "main/admin/students.html", {
            "page": "students"
        })

    if request.method == "POST":

        name = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        level = request.POST["level"]
        organization = request.POST["org"]
        reg_num = request.POST["reg"]

        try:
            student = Student.objects.create_user(
                first_name = name,
                last_name = last,
                email = email,
                password = password,
                phone = phone,
                username = email,
                is_supervisor = False,
                is_student = True,
                reg_num = reg_num,
                organization = organization,
                location = organization,
                level = level
            )

            student.save()

        except IntegrityError:
            print("error")
            return HttpResponse("Error")

        return HttpResponse("Success")


def supervisor(request):
    if request.method == "GET":
        return render(request, "main/admin/supervisors.html", {
            "page": "supervisor"
        })

    if request.method == "POST":

        name = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]

        try:
            supervisor = User.objects.create_user(
                first_name = name,
                last_name = last,
                email = email,
                password = password,
                phone = phone,
                username = email,
                is_supervisor = True,
                is_student = False
            )

            supervisor.save()

        except IntegrityError:
            print("error")
            return HttpResponse("Error")

        return HttpResponse("Success")
