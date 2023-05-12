from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import CustomUser, Teacher, Parent, Student, Admin, Course


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type')


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('subject', 'courses', 'qualifications', 'experience')


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ('children', 'occupation')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('courses', 'section', 'classRoom', 'parents')


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ()


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'description', 'teacher', 'students')


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'user_type', 'groups', 'user_permissions')


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')
