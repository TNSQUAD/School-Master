from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


from .models import Parent, Student, Course, StudentPerformance, Payment, Teacher, Grade, HealthRecord, Event,Curriculum, LearningObjective, Standard, Assessment, LibraryBook, LibraryBorrow, CalendarEvent, ChatRoom, ChatMessage, Attendance, TeacherAttendance, Notification, Section, Class

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['name', 'email', 'phone_number', 'address', 'occupation', 'children']

class ParentUpdateForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['name', 'email', 'phone_number', 'address', 'occupation', 'children']

    def __init__(self, *args, **kwargs):
        super(ParentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['children'].widget.attrs['class'] = 'select2 form-control'
        self.fields['children'].widget.attrs['data-placeholder'] = 'Select Children'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'date_of_birth', 'gender', 'address', 'phone_number', 'email', 'enrolled_courses']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect(),
            'enrolled_courses': forms.CheckboxSelectMultiple(),
        }

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'date_of_birth', 'address', 'parent')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Parent.objects.all()


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'qualifications', 'experience')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # Customize labels and placeholders for form fields
        self.fields['first_name'].label = 'First name'
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter first name'})
        self.fields['last_name'].label = 'Last name'
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter last name'})
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter email address'})
        self.fields['phone_number'].label = 'Phone number'
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Enter phone number'})
        self.fields['address'].label = 'Address'
        self.fields['address'].widget.attrs.update({'placeholder': 'Enter address'})
        self.fields['qualifications'].label = 'Qualifications'
        self.fields['qualifications'].widget.attrs.update({'placeholder': 'Enter qualifications'})
        self.fields['experience'].label = 'Experience'
        self.fields['experience'].widget.attrs.update({'placeholder': 'Enter experience'})

class TeacherProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = Teacher
        fields = ['profile_pic', 'address', 'phone_number', 'date_of_birth', 'gender', 'qualifications', 'experience']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TeacherProfileForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=self.user.username).exists():
            raise ValidationError("This email address is already in use. Please use a different email address.")
        return email


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'teacher', 'students']
        widgets = {
            'students': forms.CheckboxSelectMultiple
        }


class StudentPerformanceForm(forms.ModelForm):
    class Meta:
        model = StudentPerformance
        fields = ('student', 'exam_name', 'exam_date', 'subject', 'score')

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'amount']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'grade']


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['student', 'height', 'weight']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'date', 'attendees')
        widgets = {
            'attendees': forms.CheckboxSelectMultiple()
        }


class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class LearningObjectiveForm(forms.ModelForm):
    class Meta:
        model = LearningObjective
        fields = ['curriculum', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class StandardForm(forms.ModelForm):
    class Meta:
        model = Standard
        fields = ['curriculum', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['name', 'course', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class LibraryBookForm(forms.ModelForm):
    class Meta:
        model = LibraryBook
        fields = ['title', 'author', 'description', 'quantity']
        labels = {
            'title': 'Title',
            'author': 'Author',
            'description': 'Description',
            'quantity': 'Quantity',
        }

class LibraryBorrowForm(forms.ModelForm):
    class Meta:
        model = LibraryBorrow
        fields = ['student', 'book', 'date_returned']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_returned'].widget.attrs.update({'class': 'datepicker'})

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ('title', 'description', 'start_time', 'end_time')
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
     

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ('name',)

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ('user', 'chat_room', 'message')
        widgets = {
            'user': forms.HiddenInput(),
            'chat_room': forms.HiddenInput()
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'course', 'students_present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'students_present': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '10'})
        }

class TeacherAttendanceForm(forms.ModelForm):
    class Meta:
        model = TeacherAttendance
        fields = ('teacher', 'date', 'is_present')
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    # forms.py for Subject model
from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description']

# for Class model 
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'section']

# for Section model
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'classroom']

# for Notification model
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'description', 'classroom', 'section']
