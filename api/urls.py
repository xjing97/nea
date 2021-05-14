from django.urls import path

from config.views import get_config_by_macid, get_practice_config
from core.views import renewToken, logout, set_completed_tutorial
from result.views import store_result, get_user_results
from .views import login, ChangePasswordView

app_name = 'api'

# FOR UNITY SIDE ONLY

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('set-completed-tutorial/', set_completed_tutorial, name='set_completed_tutorial'),
    path('renew-token/', renewToken, name='renewToken'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('store-result/', store_result, name='storeResult'),
    path('get-config-by-macid/', get_config_by_macid, name='get_config_by_macid'),
    path('get-practice-config/', get_practice_config, name='get_practice_config'),
    path('get-user-results/', get_user_results, name='get_user_results'),
]
