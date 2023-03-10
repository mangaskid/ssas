from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from .models import User, Attendance, SiwesReg
from sqlite3 import IntegrityError
from datetime import date

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
                return HttpResponseRedirect(reverse("supervisordash"))
        else:
            return HttpResponseRedirect(reverse("index"))

def supervisor_dashboard(request):
    if request.method == "GET":
        siwes_students = SiwesReg.objects.filter(lecturer=request.user)
        return render(request, "main/supervisor/dashboard.html", {
            "students": siwes_students
        })

def supervisor_add_student(request):
    if request.method == "GET":
        siwes_students = User.objects.filter(is_reg=False, is_student=True)
        siwes_reg = SiwesReg.objects.all()
        # std = Student.objects.all()
        # for s in std:
        #     s.is_reg = False
        #     s.save()
        return render(request, "main/supervisor/add-student.html", {
            "students": siwes_students
        })

def supervisor_view_attendance(request, id):

    if request.method == "GET":
        student = User.objects.get(pk=id)
        attendance = Attendance.objects.filter(student=student)
        return render(request, "main/supervisor/attendance.html", {"student": student, "attendance":attendance})

def supervisor_conf_attendance(request, id, std):

    if request.method == "GET":
        attendance = Attendance.objects.get(pk=id)
        attendance.is_confirm = True
        attendance.save()

        return HttpResponseRedirect(reverse("viewattendance", args=[std,]))


def supervisor_connect_student(request, id):
    if request.method == "GET":
        lecturer = request.user
        student = User.objects.get(pk=id)
        siwes_reg = SiwesReg(
            lecturer=lecturer,
            student=student
        )
        siwes_reg.save()
        student.is_reg = True
        student.save()
        return HttpResponseRedirect(reverse("supervisordash"))

def supervisor_delete_student(request, id):
    if request.method == "GET":
        siwes_reg = SiwesReg.objects.get(pk=id)
        student = siwes_reg.student
        student.is_reg = False
        student.save()
        siwes_reg.delete()
        return HttpResponseRedirect(reverse("supervisordash"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def dashboard(request):
    spv = User.objects.filter(is_supervisor=True)
    std = User.objects.filter(is_student=True)
    return render(request, 'main/admin/admin.html', {
        "page": "dashboard",
        "spv": len(spv),
        "std": len(std)
    })

def student_dashboard(request):
    if request.method == "GET":
        data = User.objects.get(pk=request.user.id)
        # attendance = Attendance.objects.filter(student=data)

        return render(request, "main/student/dashboard.html", {
            "data": data
        })

def student_view_attendance(request, id):
    if request.method == "GET":
        student = request.user
        attendance = Attendance.objects.filter(student=student)
        return render(request, "main/student/attendance.html", {"attendance":attendance})

def student_attendance(request):
    if request.method == "POST":
        data = User.objects.get(pk=request.user.id)
        last = Attendance.objects.filter(student=data).last()
        
        today = date.today().day

        if (last.date.day == today):
            return HttpResponse("You can't take attendance twice in a day!")

        atte = Attendance(
            student=data,
            location= request.POST["url"],
            url = request.POST["gUrl"]
        )
        atte.save()
        return HttpResponse("Successfull!")

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
            student = User.objects.create_user(
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
