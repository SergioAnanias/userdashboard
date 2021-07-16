from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/new', views.newuser),
    path('users/create', views.createuser),
    path('users/<int:id>', views.showuser),
    path('users/newmessage', views.newmessage),
    path('users/newcomment', views.newcomment),
    path('users/edit', views.editself),
    path('users/edit/<int:id>', views.editadmin),
    path('users/editinfo', views.editinfo),
    path('users/editpass', views.editpass),
]
