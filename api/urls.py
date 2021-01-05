from django.urls import path

from config.views import get_config_by_macid
from core.views import renewToken, logout
from result.views import store_result
from .views import login, ChangePasswordView

app_name = 'api'

# FOR UNITY SIDE ONLY

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('renew-token/', renewToken, name='renewToken'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('store-result/', store_result, name='storeResult'),
    path('get-config-by-macid/', get_config_by_macid, name='get_config_by_macid'),
]
