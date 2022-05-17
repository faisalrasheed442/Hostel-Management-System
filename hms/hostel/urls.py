
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
    path('fee/', student.fee, name='fee'),
    path('password/', student.passwords, name='password'),
    path('logout/', student.logout, name='logout'),
    path('change_room/', student.change_room,  name='change_roon'),

]