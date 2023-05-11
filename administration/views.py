from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from .models import User
from django.utils import timezone
from django.http import JsonResponse

from .models import User, Parent, Teacher, TeacherAttendance, Student, StudentPerformance,  Attendance, Course, Payment, Grade, HealthRecord, Event, Curriculum, LearningObjective, Standard, Assessment, LibraryBook, LibraryBorrow, CalendarEvent, ChatRoom, ChatMessage, Notification, Section, Class


Parent, Teacher, Student, Subject, Grade, Notice, CustomUser, Course,StudentProfile, TeacherProfile, AdminProfile, Event, Attendance,  Subject, Class, Section, Payment

from .forms import UserForm, ParentForm, ParentUpdateForm, TeacherForm, TeacherAttendanceForm, StudentForm, StudentPerformanceForm, AttendanceForm, CourseForm, PaymentForm, GradeForm, HealthRecordForm, EventForm, CurriculumForm, LearningObjectiveForm, StandardForm, AssessmentForm, LibraryBookForm, LibraryBorrowForm, CalendarEventForm, ChatRoomForm, ChatMessageForm, StudentProfileForm, NotificationForm, SectionForm, ClassForm



 SubjectForm, NoticeForm, ClassForm, SectionForm, UserCreationForm, UserChangeForm, CustomUserCreationForm, CustomUserChangeForm,  AdminProfileForm



# View for displaying the details of a single CustomUser object
class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'administration/user_detail.html'
    context_object_name = 'user'

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'administration/user_list.html'
    context_object_name = 'users'
    ordering = ['last_name', 'first_name']
    paginate_by = 10
    search_fields = ['first_name', 'last_name', 'email']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

class UserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'administration/user_form.html'
    success_url = reverse_lazy('administration:user_list')
    success_message = "User was created successfully."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'administration/user_form.html'
    success_url = reverse_lazy('administration:user_list')
    success_message = "User was updated successfully."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'administration/user_confirm_delete.html'
    success_url = reverse_lazy('administration:user_list')
    success_message = "User was deleted successfully!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(UserDeleteView, self).delete(request, *args, **kwargs)


# Parent views
class ParentListView(LoginRequiredMixin, ListView):
    model = Parent
    template_name = 'administration/parent_list.html'
    context_object_name = 'parents'


class ParentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Parent
    form_class = ParentForm
    template_name = 'administration/parent_form.html'
    success_url = reverse_lazy('admin:parent_list')
    success_message = "Parent was created successfully!"


class ParentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Parent
    form_class = ParentForm
    template_name = 'administration/parent_form.html'
    success_url = reverse_lazy('admin:parent_list')
    success_message = "Parent was updated successfully!"


class ParentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Parent
    template_name = 'administration/parent_confirm_delete.html'
    success_url = reverse_lazy('admin:parent_list')
    success_message = "Parent was deleted successfully!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ParentDeleteView, self).delete(request, *args, **kwargs)


# View for creating new TeacherProfile objects
@login_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New teacher profile created successfully.')
            return redirect('administration:index')
    else:
        form = TeacherProfileForm()
    return render(request, 'administration/create_teacher.html', {'form': form})
# Teacher views
class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'administration/teacher_list.html'
    context_object_name = 'teachers'


class TeacherCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'administration/teacher_form.html'
    success_url = reverse_lazy('admin:teacher_list')
    success_message = "Teacher was created successfully!"


class TeacherUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'administration/teacher_form.html'
    success_url = reverse_lazy('admin:teacher_list')
    success_message = "Teacher was successfully updated!"

@login_required
def teacher_attendance(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        form = TeacherAttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance has been saved.')
            return redirect('teacher_attendance')
        else:
            messages.error(request, 'There was an error saving the attendance.')
    else:
        form = TeacherAttendanceForm()
    return render(request, 'administration/teacher_attendance.html', {'teachers': teachers, 'form': form})

@login_required
def teacher_attendance_list(request):
    attendances = TeacherAttendance.objects.all()
    return render(request, 'administration/teacher_attendance_list.html', {'attendances': attendances})


# View for creating new CustomUser objects
@login_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('admin_index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'administration/user_form.html', {'form': form, 'title': 'Create User'})

# View for updating existing CustomUser objects
@login_required
def update_user(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('admin_index')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'administration/user_form.html', {'form': form, 'title': 'Update User'})


@method_decorator(login_required, name='dispatch')
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'administration/student_list.html'
    context_object_name = 'students'


@method_decorator(login_required, name='dispatch')
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'administration/student_detail.html'
    context_object_name = 'student'


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('administration.add_student'), name='dispatch')
class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'administration/student_form.html'
    success_url = reverse_lazy('administration:student_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('administration.change_student'), name='dispatch')
class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'administration/student_form.html'
    success_url = reverse_lazy('administration:student_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('administration.delete_student'), name='dispatch')
class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Student
    template_name = 'administration/student_confirm_delete.html'
    success_url = reverse_lazy('administration:student_list')


@method_decorator(login_required, name='dispatch')
class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'administration/attendance_list.html'
    context_object_name = 'attendance'


@method_decorator(login_required, name='dispatch')
class AttendanceDetailView(LoginRequiredMixin, DetailView):
    model = Attendance
    template_name = 'administration/attendance_detail.html'
    context_object_name = 'attendance'


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('administration.add_attendance'), name='dispatch')
class AttendanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'administration/attendance_form.html'
    success_url = reverse_lazy('administration:attendance_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('administration.change_attendance'), name='dispatch')
class AttendanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'administration/attendance_form.html'
    success_url = reverse_lazy('administration:attendance_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('administration.delete_attendance'), name='dispatch')
class AttendanceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Attendance
    template_name = 'administration/attendance_confirm_delete.html'
    success_url = reverse_lazy('administration:attendance_list')

class StudentProfileView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentProfileForm
    template_name = 'administration/student_profile.html'
    success_url = reverse_lazy('administration:index')
    login_url = reverse_lazy('account_login')

    def get_object(self, queryset=None):
        return self.request.user.student


# View for displaying a list of Course objects
class CourseListView(ListView):
    model = Course
    template_name = 'administration/course_list.html'
    context_object_name = 'courses'

# View for displaying the details of a single Course object
class CourseDetailView(DetailView):
    model = Course
    template_name = 'administration/course_detail.html'
    context_object_name = 'course'

# View for creating new Course objects
@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully.')
            return redirect('course-list')
    else:
        form = CourseForm()

    return render(request, 'administration/course_form.html', {'form': form})

    from .models import StudentPerformance
from .forms import StudentPerformanceForm

class StudentPerformanceListView(ListView):
    model = StudentPerformance
    template_name = 'administration/studentperformance_list.html'
    context_object_name = 'performances'

class StudentPerformanceCreateView(CreateView):
    model = StudentPerformance
    form_class = StudentPerformanceForm
    template_name = 'administration/studentperformance_form.html'
    success_url = reverse_lazy('studentperformance_list')


@method_decorator(login_required, name='dispatch')
class PaymentListView(ListView):
    model = Payment
    template_name = 'administration/payment_list.html'
    context_object_name = 'payments'

@method_decorator(login_required, name='dispatch')
class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'administration/payment_form.html'
    success_url = reverse_lazy('payment_list')

@method_decorator(login_required, name='dispatch')
class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'administration/payment_form.html'
    success_url = reverse_lazy('payment_list')

@method_decorator(login_required, name='dispatch')
class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'administration/payment_confirm_delete.html'
    success_url = reverse_lazy('payment_list')

# View for displaying a list of all Grade objects
class GradeListView(ListView):
    model = Grade
    template_name = 'administration/grade_list.html'
    context_object_name = 'grades'


# View for displaying the details of a single Grade object
class GradeDetailView(DetailView):
    model = Grade
    template_name = 'administration/grade_detail.html'
    context_object_name = 'grade'


# View for creating new Grade objects
@method_decorator(login_required, name='dispatch')
class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'administration/grade_form.html'
    success_url = reverse_lazy('administration:grade_list')


# View for updating existing Grade objects
@method_decorator(login_required, name='dispatch')
class GradeUpdateView(UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'administration/grade_form.html'
    success_url = reverse_lazy('administration:grade_list')


# View for deleting existing Grade objects
@method_decorator(login_required, name='dispatch')
class GradeDeleteView(DeleteView):
    model = Grade
    template_name = 'administration/grade_confirm_delete.html'
    success_url = reverse_lazy('administration:grade_list')

class HealthRecordListView(ListView):
    model = HealthRecord
    template_name = 'administration/healthrecord_list.html'
    context_object_name = 'healthrecords'


class HealthRecordCreateView(LoginRequiredMixin, CreateView):
    model = HealthRecord
    form_class = HealthRecordForm
    template_name = 'administration/healthrecord_form.html'
    success_url = reverse_lazy('administration:healthrecord-list')


class HealthRecordDetailView(DetailView):
    model = HealthRecord
    template_name = 'administration/healthrecord_detail.html'
    context_object_name = 'healthrecord'


class HealthRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = HealthRecord
    form_class = HealthRecordForm
    template_name = 'administration/healthrecord_form.html'
    context_object_name = 'healthrecord'
    success_url = reverse_lazy('administration:healthrecord-list')


class HealthRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = HealthRecord
    template_name = 'administration/healthrecord_confirm_delete.html'
    context_object_name = 'healthrecord'
    success_url = reverse_lazy('administration:healthrecord-list')

# View for displaying a list of Event objects
class EventListView(ListView):
    model = Event
    template_name = 'administration/event_list.html'
    context_object_name = 'events'

# View for creating new Event objects
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'administration/event_form.html', {'form': form})

# View for updating existing Event objects
@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'administration/event_form.html', {'form': form, 'event': event})

# View for deleting existing Event objects
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'administration/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

# View for displaying the details of a single Event object
class EventDetailView(DetailView):
    model = Event
    template_name = 'administration/event_detail.html'
    context_object_name = 'event'


# View for displaying a list of all Curriculum objects
class CurriculumListView(ListView):
    model = Curriculum
    template_name = 'administration/curriculum_list.html'
    context_object_name = 'curriculums'

# View for displaying the details of a single Curriculum object
class CurriculumDetailView(DetailView):
    model = Curriculum
    template_name = 'administration/curriculum_detail.html'
    context_object_name = 'curriculum'

# View for creating new Curriculum objects
class CurriculumCreateView(CreateView):
    model = Curriculum
    template_name = 'administration/curriculum_form.html'
    fields = ['name', 'description']

# View for updating existing Curriculum objects
class CurriculumUpdateView(UpdateView):
    model = Curriculum
    template_name = 'administration/curriculum_form.html'
    fields = ['name', 'description']

# View for deleting existing Curriculum objects
class CurriculumDeleteView(DeleteView):
    model = Curriculum
    template_name = 'administration/curriculum_confirm_delete.html'
    success_url = reverse_lazy('administration:curriculum_list')

# View for displaying a list of all LearningObjective objects
class LearningObjectiveListView(ListView):
    model = LearningObjective
    template_name = 'administration/learningobjective_list.html'
    context_object_name = 'learningobjectives'

# View for displaying the details of a single LearningObjective object
class LearningObjectiveDetailView(DetailView):
    model = LearningObjective
    template_name = 'administration/learningobjective_detail.html'
    context_object_name = 'learningobjective'

# View for creating new LearningObjective objects
class LearningObjectiveCreateView(CreateView):
    model = LearningObjective
    template_name = 'administration/learningobjective_form.html'
    fields = ['curriculum', 'description']

# View for updating existing LearningObjective objects
class LearningObjectiveUpdateView(UpdateView):
    model = LearningObjective
    template_name = 'administration/learningobjective_form.html'
    fields = ['curriculum', 'description']

# View for deleting existing LearningObjective objects
class LearningObjectiveDeleteView(DeleteView):
    model = LearningObjective
    template_name = 'administration/learningobjective_confirm_delete.html'
    success_url = reverse_lazy('administration:learningobjective_list')

# View for displaying a list of all Standard objects
class StandardListView(ListView):
    model = Standard
    template_name = 'administration/standard_list.html'
    context_object_name = 'standards'

# View for displaying the details of a single Standard object
class StandardDetailView(DetailView):
    model = Standard
    template_name = 'administration/standard_detail.html'
    context_object_name = 'standard'

# View for creating new Standard objects
class StandardCreateView(CreateView):
    model = Standard
    template_name = 'administration/standard_form.html'
    fields = ['curriculum', 'description']

# View for updating existing Standard objects
class StandardUpdateView(UpdateView):
    model = Standard
    template_name = 'administration/standard_form.html'
    fields = ['curriculum', 'description']

# View for deleting existing Standard objects
class StandardDeleteView(DeleteView):
    model = Standard
    template_name = 'administration/standard_confirm_delete.html'
    success_url = reverse_lazy('administration:standard_list')

# View for Assessment objects
class AssessmentCreateView(CreateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = 'administration/assessment_create.html'
    success_url = reverse_lazy('administration:assessment_list')


class AssessmentUpdateView(UpdateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = 'administration/update.html'
    success_url = reverse_lazy('administration:assessment_list')


class AssessmentDeleteView(DeleteView):
    model = Assessment
    template_name = 'administration/delete.html'
    success_url = reverse_lazy('administration:assessment_list')


class AssessmentListView(ListView):
    model = Assessment
    template_name = 'administration/assessment_list'
    paginate_by = 10


# View for LibraryBook objects
@method_decorator(login_required, name='dispatch')
class LibraryBookList(LoginRequiredMixin, ListView):
    model = LibraryBook
    template_name = 'administration/librarybook_list.html'
    context_object_name = 'books'

@method_decorator(login_required, name='dispatch')
class LibraryBookCreate(LoginRequiredMixin, CreateView):
    model = LibraryBook
    form_class = LibraryBookForm
    template_name = 'administration/librarybook_form.html'
    success_url = reverse_lazy('administration:librarybook_list')

@method_decorator(login_required, name='dispatch')
class LibraryBookUpdate(LoginRequiredMixin, UpdateView):
    model = LibraryBook
    form_class = LibraryBookForm
    template_name = 'administration/librarybook_form.html'
    success_url = reverse_lazy('administration:librarybook_list')

@method_decorator(login_required, name='dispatch')
class LibraryBookDelete(LoginRequiredMixin, DeleteView):
    model = LibraryBook
    template_name = 'administration/librarybook_confirm_delete.html'
    success_url = reverse_lazy('administration:librarybook_list')

@method_decorator(login_required, name='dispatch')
class LibraryBorrowList(LoginRequiredMixin, ListView):
    model = LibraryBorrow
    template_name = 'administration/libraryborrow_list.html'
    context_object_name = 'borrows'

@method_decorator(login_required, name='dispatch')
class LibraryBorrowCreate(LoginRequiredMixin, CreateView):
    model = LibraryBorrow
    form_class = LibraryBorrowForm
    template_name = 'administration/libraryborrow_form.html'
    success_url = reverse_lazy('administration:libraryborrow_list')

    def form_valid(self, form):
        book = form.cleaned_data['book']
        if book.quantity == 0:
            messages.error(self.request, f'The book "{book.title}" is not available for borrowing.')
            return redirect('administration:libraryborrow_create')
        else:
            book.quantity -= 1
            book.save()
            return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class LibraryBorrowUpdate(LoginRequiredMixin, UpdateView):
    model = LibraryBorrow
    form_class = LibraryBorrowForm
    template_name = 'administration/libraryborrow_form.html'
    success_url = reverse_lazy('administration:libraryborrow_list')

    def form_valid(self, form):
        book = form.cleaned_data['book']
        if book.quantity == 0:
            messages.error(self.request, f'The book "{book.title}" is not available for borrowing.')
            return redirect('administration:libraryborrow_update', pk=self.kwargs['pk'])
        else:
            book.quantity -= 1
            book.save()
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, f'The form contains errors.')
        return super().form_invalid(form)

@method_decorator(login_required, name='dispatch')
class LibraryBorrowDelete(LoginRequiredMixin, DeleteView):
    model = LibraryBorrow
    template_name = 'administration/libraryborrow_confirm_delete.html'
    success_url = reverse_lazy('administration:libraryborrow_list')

    def delete(self, request, *args, **kwargs):
        borrow = self.get_object()
        book = borrow.book
        book.quantity += 1
        book.save()
        return super().delete(request, *args, **kwargs)

# Views for CalendarEvent Objects
class CalendarEventListView(ListView):
    model = CalendarEvent
    template_name = 'administration/calendar_event_list.html'
    context_object_name = 'events'
    ordering = ['-start_time']


class CalendarEventCreateView(CreateView):
    model = CalendarEvent
    template_name = 'administration/calendar_event_form.html'
    fields = ['title', 'description', 'start_time', 'end_time']
    success_url = reverse_lazy('administration:event_list')


class CalendarEventUpdateView(UpdateView):
    model = CalendarEvent
    template_name = 'administration/calendar_event_form.html'
    fields = ['title', 'description', 'start_time', 'end_time']
    success_url = reverse_lazy('administration:event_list')


class CalendarEventDeleteView(DeleteView):
    model = CalendarEvent
    template_name = 'administration/calendar_event_confirm_delete.html'
    success_url = reverse_lazy('administration:event_list')

# Views for Chat_rooms Objects
@login_required
def chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'administration/chat_rooms.html', {'chat_rooms': chat_rooms})

@login_required
def create_chat_room(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chat_room = form.save()
            messages.success(request, 'Chat room created successfully!')
            return redirect('chat_rooms')
    else:
        form = ChatRoomForm()
    return render(request, 'administration/create_chat_room.html', {'form': form})

@login_required
def edit_chat_room(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, pk=chat_room_id)
    if request.method == 'POST':
        form = ChatRoomForm(request.POST, instance=chat_room)
        if form.is_valid():
            chat_room = form.save()
            messages.success(request, 'Chat room updated successfully!')
            return redirect('chat_rooms')
    else:
        form = ChatRoomForm(instance=chat_room)
    return render(request, 'administration/edit_chat_room.html', {'form': form})

@login_required
def delete_chat_room(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, pk=chat_room_id)
    chat_room.delete()
    messages.success(request, 'Chat room deleted successfully!')
    return redirect('chat_rooms')

@login_required
def chat_messages(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, pk=chat_room_id)
    chat_messages = ChatMessage.objects.filter(chat_room=chat_room).order_by('timestamp')
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.chat_room = chat_room
            chat_message.timestamp = timezone.now()
            chat_message.save()
            return redirect('chat_messages', chat_room_id=chat_room.id)
    else:
        form = ChatMessageForm()
    return render(request, 'administration/chat_messages.html', {'chat_room': chat_room, 'chat_messages': chat_messages, 'form': form})

@login_required
def delete_chat_message(request, chat_room_id, chat_message_id):
    chat_message = get_object_or_404(ChatMessage, pk=chat_message_id, chat_room__pk=chat_room_id)
    chat_message.delete()
    messages.success(request, 'Chat message deleted successfully!')
    return redirect('chat_messages', chat_room_id=chat_room_id)

@login_required
def get_chat_messages(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, pk=chat_room_id)
    chat_messages = ChatMessage.objects.filter(chat_room=chat_room).order_by('timestamp')
    data = []
    for message in chat_messages:
        data.append({'id': message.id, 'user': message.user.username, 'message': message.message, 'timestamp': str(message.timestamp)})
    return JsonResponse({'chat_messages': data})

# Notification list view
class NotificationListView(ListView):
    model = Notification
    context_object_name = 'notifications'
    ordering = ['-created_at']
    template_name = 'administration/notification_list.html'


# Notification create view
@staff_member_required(login_url='login')
def create_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification created successfully.')
            return redirect('admin_dashboard')
    else:
        form = NotificationForm()
    context = {'form': form}
    return render(request, 'administration/notification_form.html', context)


# Notification update view
@staff_member_required(login_url='login')
def update_notification(request, pk):
    notification = Notification.objects.get(id=pk)
    form = NotificationForm(instance=notification)
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification updated successfully.')
            return redirect('admin_dashboard')
    context = {'form': form}
    return render(request, 'administration/notification_form.html', context)


# Notification delete view
class NotificationDeleteView(DeleteView):
    model = Notification
    context_object_name = 'notification'
    template_name = 'administration/notification_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')


class SectionListView(ListView):
    model = Section
    template_name = 'administration/section_list.html'
    context_object_name = 'sections'

class SectionCreateView(CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'administration/section_form.html'
    success_url = reverse_lazy('section_list')

class SectionUpdateView(UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'administration/section_form.html'
    success_url = reverse_lazy('section_list')

class SectionDeleteView(DeleteView):
    model = Section
    template_name = 'administration/section_confirm_delete.html'
    success_url = reverse_lazy('section_list')


class ClassListView(ListView):
    model = Class
    template_name = 'administration/class_list.html'
    context_object_name = 'classes'

class ClassCreateView(CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'administration/class_form.html'
    success_url = reverse_lazy('class_list')

class ClassUpdateView(UpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'administration/class_form.html'
    success_url = reverse_lazy('class_list')

class ClassDeleteView(DeleteView):
    model = Class
    template_name = 'administration/class_confirm_delete.html'
    success_url = reverse_lazy('class_list')


class SubjectListView(ListView):
    model = Subject
    template_name = 'administration/subject_list.html'
    context_object_name = 'subjects'

class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'administration/subject_form.html'
    success_url = reverse_lazy('subject_list')

class SubjectUpdateView(UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'administration/subject_form.html'
    success_url = reverse_lazy('subject_list')

class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'administration/subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')
