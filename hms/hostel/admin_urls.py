
from django.urls import path
from .import views
admin=views.admin_view()
urlpatterns = [
    path('', admin.index, name='Home'),

]