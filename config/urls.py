from django.urls import path
from .views import get_config_with_id, get_default_config_with_scenario_id, get_all_configs_with_scenario_id, \
    create_config, edit_config, duplicate_config, delete_config

app_name = 'config'

urlpatterns = [
    path('get-config-with-id/', get_config_with_id, name='get_config_with_id'),
    path('get-default-config-with-scenario-id/', get_default_config_with_scenario_id,
         name='get_default_config_with_scenario_id'),
    path('get-all-configs-with-scenario-id/', get_all_configs_with_scenario_id,
         name='get_all_configs_with_scenario_id'),
    path('create-config/', create_config, name='create_config'),
    path('edit-config/', edit_config, name='edit_config'),
    path('duplicate-config/', duplicate_config, name='duplicate_config'),
    path('delete-config/', delete_config, name='delete_config'),
]
