from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    # Parent URLs
    path('parents/', views.ParentListView.as_view(), name='parent_list'),
    path('parents/create/', views.create_parent, name='create_parent'),
    path('parents/<int:pk>/', views.ParentDetailView.as_view(), name='parent_detail'),
    path('parents/<int:pk>/update/', views.update_parent, name='update_parent'),
    
    # Student URLs
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/create/', views.create_student, name='create_student'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/update/', views.update_student, name='update_student'),
    
    # Course URLs
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/update/', views.update_course, name='update_course'),
    
    # Parent-Student URLs
    path('parent-student/', views.ParentStudentListView.as_view(), name='parent_student_list'),
    path('parent-student/create/', views.create_parent_student, name='create_parent_student'),
    path('parent-student/<int:pk>/', views.ParentStudentDetailView.as_view(), name='parent_student_detail'),
    path('parent-student/<int:pk>/update/', views.update_parent_student, name='update_parent_student'),
    
    # Calendar Event URLs
    path('events/', views.CalendarEventListView.as_view(), name='calendar_event_list'),
    path('events/create/', views.create_calendar_event, name='create_calendar_event'),
    path('events/<int:pk>/', views.CalendarEventDetailView.as_view(), name='calendar_event_detail'),
    path('events/<int:pk>/update/', views.update_calendar_event, name='update_calendar_event'),
    
    # Performance Analytics URLs
    path('analytics/', views.PerformanceAnalyticsView.as_view(), name='performance_analytics'),
    
    # Student Information Management URLs
    path('student-info/', views.StudentInformationManagementView.as_view(), name='student_info_management'),
    
    # Real-time Chatting Forum URLs
    path('chat/', views.ChatView.as_view(), name='chat'),
]
