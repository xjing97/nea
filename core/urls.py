from django.urls import path, include
from .views import create_acc, mass_create_acc, login, renewToken, editUser, deleteUser, getUser, getAllUsers, \
    userDashboard, changeUserPassword

app_name = 'core'

urlpatterns = [
    path('login/', login, name='login'),
    path('renew-token/', renewToken, name='renewToken'),
    path('create-acc/', create_acc, name='create_acc'),
    path('mass-create-acc/', mass_create_acc, name='mass_create_acc'),
    path('get-all-users/', getAllUsers, name='getAllUsers'),
    path('get-user/', getUser, name='getUser'),
    path('edit-user/', editUser, name='editUser'),
    path('delete-user/', deleteUser, name='deleteUser'),
    path('get-user-dashboard/', userDashboard, name='userDashboard'),
    path('change-user-password/', changeUserPassword, name='changeUserPassword'),
]
