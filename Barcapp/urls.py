from django.urls import path
from . import views

urlpatterns = [
    path('add_user', views.add_user, name='add_user'),
    path('add_email', views.add_email, name='add_email'),
    path('add_password', views.add_password, name='add_password')
]