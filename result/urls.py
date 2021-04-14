from django.urls import path
from .views import get_all_results, get_results_by_date, get_result_details, get_critical_failure, \
    update_result_breakdown, get_event_analysis, play_audio_file

app_name = 'result'

urlpatterns = [
    path('get-all-results/', get_all_results, name='get_all_results'),
    path('get-result-details/', get_result_details, name='get_result_details'),
    path('get-results-by-date/', get_results_by_date, name='get_results_by_date'),
    path('get-critical-failure/', get_critical_failure, name='get_critical_failure'),
    path('get-event-analysis/', get_event_analysis, name='get_event_analysis'),
    path('update-result-breakdown/', update_result_breakdown, name='update_result_breakdown'),
    path('play-audio-file/upload/audio/<str:path>/', play_audio_file, name='play_audio_file'),
]
