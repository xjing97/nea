from django.urls import path, include
from .views import get_all_modules

app_name = 'module'

urlpatterns = [
    path('get-all-modules/', get_all_modules, name='get_all_modules'),
]
