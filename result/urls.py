from django.urls import path, include
from .views import get_all_results

app_name = 'result'

urlpatterns = [
    path('get-all-results/', get_all_results, name='get_all_results'),
]
