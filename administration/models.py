from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_set'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_permissions',
        help_text=_('The permissions this user has')
    )

    def __str__(self):
        return self.username


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    subject = models.CharField(max_length=255)
    courses = models.ManyToManyField('Course', related_name='teachers')
    qualifications = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)


class Parent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    children = models.ManyToManyField('Student')
    occupation = models.CharField(max_length=255)


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    courses = models.ManyToManyField('Course')
    section = models.CharField(max_length=255)
    classRoom = models.CharField(max_length=255)
    parents = models.ManyToManyField(Parent)


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField('Student', blank=True)

    def __str__(self):
        return self.name

class StudentPerformance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='performances')
    exam_name = models.CharField(max_length=200)
    exam_date = models.DateField()
    subject = models.CharField(max_length=200)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    attendance_report = models.CharField(max_length=200, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ])
    grade = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.exam_name} - {self.user.username}"
