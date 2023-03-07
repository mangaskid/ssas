from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser 

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    phone = models.CharField(max_length=255)
    reg_num = models.CharField(max_length=255, default="")
    organization = models.CharField(max_length=255, default="")
    level = models.CharField(max_length=255, default="")
    location = models.CharField(max_length=255, default="")
    is_reg = models.BooleanField(default=False)

    # USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

# class Student(User):
#     reg_num = models.CharField(max_length=255)
#     organization = models.CharField(max_length=255)
#     level = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     is_reg = models.BooleanField(default=False)

class SiwesReg(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_reg")
    date = models.DateTimeField(auto_now=True)

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
