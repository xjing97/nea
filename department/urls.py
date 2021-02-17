from django.urls import path, include

from department.views import get_all_user_department, get_user_department, get_grc_by_department, get_division_by_grc, \
    get_all_division, add_user_department, edit_user_department, get_grc, add_grc, edit_grc

app_name = 'department'

urlpatterns = [
    path('get-all-user-department/', get_all_user_department, name='get_all_user_department'),
    path('get-user-department/', get_user_department, name='get_user_department'),
    path('add-user-department/', add_user_department, name='get_user_department'),
    path('edit-user-department/', edit_user_department, name='get_user_department'),
    path('get-all-division/', get_all_division, name='get_all_division'),
    path('get-grc-by-department/', get_grc_by_department, name='get_grc_by_department'),
    path('get-grc/', get_grc, name='get_grc'),
    path('add-grc/', add_grc, name='add_grc'),
    path('edit-grc/', edit_grc, name='edit_grc'),
    path('get-division-by-grc/', get_division_by_grc, name='get_division_by_grc'),
]
