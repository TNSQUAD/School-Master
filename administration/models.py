from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    TEACHER = 'teacher'
    PARENT = 'parent'
    STUDENT = 'student'
    ADMIN = 'admin'
    USER_TYPE_CHOICES = [
        (TEACHER, 'Teacher'),
        (PARENT, 'Parent'),
        (STUDENT, 'Student'),
        (ADMIN, 'Admin'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
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
    roll_no = models.CharField(max_length=10, null=True, blank=True)
    courses = models.ManyToManyField('Course')
    section = models.CharField(max_length=255)
    class_room = models.CharField(max_length=255)
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

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)

class Grade(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    date_graded = models.DateField(auto_now_add=True)

class HealthRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='health_records')
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    attendees = models.ManyToManyField(CustomUser)

class Curriculum(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class LearningObjective(models.Model):
    curriculum = models.ForeignKey('Curriculum', on_delete=models.CASCADE)
    description = models.TextField()

class Standard(models.Model):
    curriculum = models.ForeignKey('Curriculum', on_delete=models.CASCADE)
    description = models.TextField()

class Assessment(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    description = models.TextField()

class LibraryBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField()

class LibraryBorrow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey('LibraryBook', on_delete=models.CASCADE)
    date_borrowed = models.DateField(auto_now_add=True)
    date_returned = models.DateField(null=True, blank=True)

class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Calendar Events"


class ChatRoom(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)
    
class StudentAttendance(models.Model):
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'USER_TYPE_CHOICES':CustomUser.STUDENT})
    is_present = models.BooleanField(default=True)

class TeacherAttendance(models.Model):
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'USER_TYPE_CHOICES': CustomUser.TEACHER})
    is_present = models.BooleanField(default=True)

class AttendanceReport(models.Model):
    date = models.DateField()
    student_attendance = models.ManyToManyField(StudentAttendance)
    teacher_attendance = models.ManyToManyField(TeacherAttendance)
    
    def get_total_student_present(self):
        return self.student_attendance.filter(is_present=True).count()
    
    def get_total_student_absent(self):
        return self.student_attendance.filter(is_present=False).count()
    
    def get_total_teacher_present(self):
        return self.teacher_attendance.filter(is_present=True).count()
    
    def get_total_teacher_absent(self):
        return self.teacher_attendance.filter(is_present=False).count()
    
    def __str__(self):
        return f"Attendance Report for {self.date}"

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=255)
    cls = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cls} - {self.name}"

class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
