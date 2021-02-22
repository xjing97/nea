from django.urls import path, include
from .views import get_all_results, get_results_by_date, get_result_details

app_name = 'result'

urlpatterns = [
    path('get-all-results/', get_all_results, name='get_all_results'),
    path('get-result-details/', get_result_details, name='get_result_details'),
    path('get-results-by-date/', get_results_by_date, name='get_results_by_date'),
]
