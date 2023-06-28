from django.urls import path
from . import views

urlpatterns = [
    #path('hello/',views.say_hello)
    path('add_user', views.add_user, name='add_user')
]