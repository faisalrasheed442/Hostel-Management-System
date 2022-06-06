from django.urls import path
from .import views
admin=views.admin_view()
urlpatterns = [
    path('admin-basic/', admin.admin_basic, name='admin-basic'),
    path('admin-dashboard', admin.admin_dashboard, name='admin-dashboard'),

    path('student-registration', admin.student_registration, name='student-registration'),
    path('manage-student', admin.manage_student, name='manage-student'),

    path('add-room', admin.add_room, name='add-room'),
    path('manage-room', admin.manage_room, name='manage-room'),

    path('admin-profile', admin.admin_profile, name='admin-profile'),
    path('admin-update-password', admin.admin_update_password, name='admin-update-password'),

    path('admin-login', admin.admin_login, name='admin-login'),
    path('admin-registration', admin.admin_registration, name='admin-registration'),
    path('admin-message', admin.admin_message, name='admin-message'),
]