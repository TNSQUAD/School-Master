from django.db import models

class Parent(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    occupation = models.CharField(max_length=255)
    children = models.ManyToManyField('Student')

class Student(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female')])
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    enrolled_courses = models.ManyToManyField('Course')

class StudentPerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=200)
    exam_date = models.DateField()
    subject = models.CharField(max_length=200)
    score = models.FloatField()

    class Meta:
        verbose_name_plural = "Student Performances"

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    students = models.ManyToManyField('Student')

class Teacher(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female')])
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    courses = models.ManyToManyField('Course')
    date_joined = models.DateTimeField(auto_now_add=True)
    qualifications = models.TextField()
    experience = models.TextField()


class Payment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)

class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    date_graded = models.DateField(auto_now_add=True)

class HealthRecord(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    attendees = models.ManyToManyField('Student')

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
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)

class TeacherAttendance(models.Model):
    date = models.DateField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=255)
    cls = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cls} - {self.name}"

class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
