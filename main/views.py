from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

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
                return HttpResponseRedirect(reverse("student"))

            if user.is_supervisor:
                return HttpResponseRedirect(reverse("supervisor"))

            #TODO: Create and return no access page
        else:
            return HttpResponseRedirect(reverse("login"))


def dashboard(request):
    return HttpResponse("Admin Dashboard")


def student(request):
    return HttpResponse("Student Dashboard")


def supervisor(request):
    return HttpResponse("Supervisor Dashboard")
