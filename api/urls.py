from django.urls import path, include

from core.views import login

app_name = 'core'

urlpatterns = [
    path('login/', login, name='login'),
]
