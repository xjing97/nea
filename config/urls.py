from django.urls import path
from .views import get_config_with_id, get_default_config_with_scenario_id

app_name = 'config'

urlpatterns = [
    path('get-config-with-id/', get_config_with_id, name='get_config_with_id'),
    path('get-default-config-with-scenario-id/', get_default_config_with_scenario_id,
         name='get_default_config_with_scenario_id'),
]
