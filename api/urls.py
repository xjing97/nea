from django.urls import path

from core.views import renewToken
from result.views import store_result
from .views import login, ChangePasswordView

app_name = 'api'

# FOR UNITY SIDE ONLY

urlpatterns = [
    path('login/', login, name='login'),
    path('renew-token/', renewToken, name='renewToken'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('store-result/', store_result, name='storeResult'),
]
