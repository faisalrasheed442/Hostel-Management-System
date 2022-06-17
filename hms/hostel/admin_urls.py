from django.urls import path
from .import views
admin=views.admin_view()
urlpatterns = [
    path('admin-basic/', admin.admin_basic, name='admin-basic'),
    path('admin-dashboard', admin.admin_dashboard, name='admin-dashboard'),

    path('student-registration', admin.student_registration, name='student-registration'),
    path('manage-student', admin.manage_student, name='manage-student'),
    path('update-student', admin.update_student, name='update-student'),

    path('add-room', admin.add_room, name='add-room'),
    path('manage-room', admin.manage_room, name='manage-room'),

    path('admin-profile', admin.admin_profile, name='admin-profile'),
    path('admin-update-password', admin.admin_update_password, name='admin-update-password'),

    path('admin-login', admin.admin_login, name='admin-login'),
    path('admin-message', admin.admin_message, name='admin-message'),
    path('admin-complain', admin.admin_complain, name='admin-complain'),
    path('update-room', admin.update_room, name='update-room'),

    path('chat-now', admin.chat_now, name='chat-now'),
    path('fee-detail', admin.fee_detail, name='fee-detail'),
    path('admin-logout', admin.admin_logout, name='admin-logout'),
]