from django.urls import path, include

from result.views import store_result
from .views import login

app_name = 'core'

# FOR UNITY SIDE ONLY

urlpatterns = [
    path('login/', login, name='login'),
    path('store-result/', store_result, name='storeResult'),
]
