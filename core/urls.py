from django.urls import path, include
from .views import sign_up, login, editUser, deleteUser

app_name = 'core'

urlpatterns = [
    path('create-acc/', sign_up, name='create-acc'),
    path('login/', login, name='login'),
    path('edit-user/', editUser, name='editUser'),
    path('delete-user/', deleteUser, name='deleteUser'),
]
