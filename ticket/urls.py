from django.urls import path
from . import views

urlpatterns = [
    path("login", views.logn, name = "login"),
    path("", views.index, name = "index"),
    path("add", views.add, name ='add'),
    path("logout", views.logt, name = 'logout'),
    path("newForm", views.newForm, name = "newForm"),
    path("editForm", views.editForm, name = 'editForm'),
    path("extraTickets", views.extraTicket, name = 'extrat'),
    path("paswordreset", views.new_password, name = "new_password"),
    path("edit", views.edit, name = 'edit')
]