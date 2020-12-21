from django.urls import path, include
from .views import create_acc, mass_create_acc, login, editUser, deleteUser, getUser, getAllUsers

app_name = 'core'

urlpatterns = [
    path('create-acc/', create_acc, name='create_acc'),
    path('mass-create-acc/', mass_create_acc, name='mass_create_acc'),
    path('login/', login, name='login'),
    path('get-all-users/', getAllUsers, name='getAllUsers'),
    path('get-user/', getUser, name='getUser'),
    path('edit-user/', editUser, name='editUser'),
    path('delete-user/', deleteUser, name='deleteUser'),
]
