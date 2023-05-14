from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField()
    photo = models.ImageField(upload_to='student_photos/')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    students = models.ManyToManyField(Student, related_name='courses')

    def __str__(self):
        return self.title


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username}'s grade in {self.course.title} for {self.assignment}"


class HealthRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    immunizations = models.TextField()
    medical_history = models.TextField()
    medications = models.TextField()
    allergies = models.TextField()

    def __str__(self):
        return f"{self.student.user.username}'s health record"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attendees = models.ManyToManyField(CustomUser, related_name='events_attending')

    def __str__(self):
        return self.title


class LearningObjective(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Standard(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title


class LibraryBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title


class LibraryBorrow(models.Model):
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username}'s borrowing of {self.book.title}"


class CalendarEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attendees = models.ManyToManyField(CustomUser, related_name='calendar_events_attending')

    def __str__(self):
        return self.title


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser)

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Section(models.Model):
    name = models.CharField(max_length=255)

class ClassRoom(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    students = models.ManyToManyField(CustomUser, related_name='classes')
