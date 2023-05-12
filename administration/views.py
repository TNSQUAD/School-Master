from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CustomUser, Teacher, Parent, Student, Admin, Course, StudentPerformance


# Frontend
def index(request):
    return render(request, 'administration/index.html')

@login_required
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

class TeacherListView(ListView):
    model = Teacher
    template_name = 'teacher_list.html'

class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'teacher_detail.html'

class TeacherCreateView(CreateView):
    model = Teacher
    template_name = 'teacher_form.html'
    fields = ['user', 'subject', 'courses', 'qualifications', 'experience']

class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'teacher_form.html'
    fields = ['user', 'subject', 'courses', 'qualifications', 'experience']

class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher_list')

class ParentListView(ListView):
    model = Parent
    template_name = 'parent_list.html'

class ParentDetailView(DetailView):
    model = Parent
    template_name = 'parent_detail.html'

class ParentCreateView(CreateView):
    model = Parent
    template_name = 'parent_form.html'
    fields = ['user', 'children', 'occupation']

class ParentUpdateView(UpdateView):
    model = Parent
    template_name = 'parent_form.html'
    fields = ['user', 'children', 'occupation']

class ParentDeleteView(DeleteView):
    model = Parent
    template_name = 'parent_confirm_delete.html'
    success_url = reverse_lazy('parent_list')

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'

class StudentCreateView(CreateView):
    model = Student
    template_name = 'student_form.html'
    fields = ['user', 'courses', 'section', 'classRoom', 'parents']

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student_form.html'
    fields = ['user', 'courses', 'section', 'classRoom', 'parents']

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

class AdminListView(ListView):
    model = Admin
    template_name = 'admin_list.html'

class AdminDetailView(DetailView):
    model = Admin
    template_name = 'admin_detail.html'

class AdminCreateView(CreateView):
    model = Admin
    template_name = 'admin_form.html'
    fields = ['user']

class AdminUpdateView(UpdateView):
    model = Admin
    template_name = 'admin_form.html'
    fields = ['user']

class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'

class StudentPerformanceListView(ListView):
    model = StudentPerformance
    template_name = 'performance_list.html'

class StudentPerformanceDetailView(DetailView):
    model = StudentPerformance
    template_name = 'performance_detail.html'

class StudentPerformanceCreateView(CreateView):
    model = StudentPerformance
    template_name = 'performance_form.html'
    fields = ['user', 'exam_name', 'exam_date', 'subject', 'score', 'attendance_report', 'grade']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class StudentPerformanceUpdateView(UpdateView):
    model = StudentPerformance
    template_name = 'performance_form.html'
    fields = ['user', 'exam_name', 'exam_date', 'subject', 'score', 'attendance_report', 'grade']

class StudentPerformanceDeleteView(DeleteView):
    model = StudentPerformance
    template_name = 'performance_confirm_delete.html'
    success_url = reverse_lazy('performance_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Student performance record deleted successfully.')
        return super().delete(request, *args, **kwargs)
