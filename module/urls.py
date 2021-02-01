from django.urls import path
from .views import get_all_modules, count_modules_by_difficulty, edit_quiz_attempt

app_name = 'module'

urlpatterns = [
    path('get-all-modules/', get_all_modules, name='get_all_modules'),
    path('get-modules-for-dashboard/', count_modules_by_difficulty, name='count_modules_by_difficulty'),
    path('edit-quiz-attempt/', edit_quiz_attempt, name='edit_quiz_attempt'),
]
