
from django.urls import path
from .import views
student=views.student_view()
urlpatterns = [


    path('', student.index, name='Home'),
    path('login/', student.login, name='Login'),
    path('register/', student.register, name='register'),
    path('dashboard/', student.dashboard, name='Dashboard'),
    path('profile/', student.profile, name='profile'),
    path('room/', student.room, name='room'),
    path('complains/', student.complains, name='complains'),
    path('fee/', student.fee_detail, name='fee'),
    path('password/', student.passwords, name='password'),
    path('logout/', student.logout, name='logout'),
    path('change_room/', student.change_room,  name='change_room'),
    path('forget_password/', student.forget_password,  name='forget_password'),
    path('book_room/', student.book_room,  name='book_room'),
    path('chat/', student.chat,  name='chat'),
    path('installment/', student.installment,  name='installment'),

]