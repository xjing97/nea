from django.db.models import F, Value
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.models import Config
from core.models import User
from module.models import Scenario


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_config_by_macid(request):
    user_id = request.user.id
    mac_id = request.GET.get('mac_id', '')
    if not mac_id:
        user = User.objects.filter(id=user_id).first()
        mac_id = user.mac_id
        if not mac_id:
            return Response(status=400, data={'message': 'mac_id is required'})

    config = Config.objects.get_config_by_macid(user_id, mac_id)

    return Response(data={'data': list(config)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_practice_config(request):
    config = Scenario.objects.get_all_default_configs()

    return Response(data={'data': list(config)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_config_with_id(request):
    config_id = request.GET.get('config_id', '')

    config = Config.objects.filter(id=config_id).first()

    if not config:
        return Response(status=400, data={'message': 'Configuration not found'})

    scenarios = Scenario.objects.values('id', 'scenario_title')
    mac_ids = User.objects.exclude(mac_id="").values_list('mac_id', flat=True)

    return Response(data={'data': {'config': {'scenario__id': config.scenario_id,
                                              'config': config.config,
                                              'breeding_point': config.breeding_point,
                                              'is_owner_at_home': config.is_owner_at_home,
                                              'is_owner_appeal': config.is_owner_appeal,
                                              'is_refuse_entry': config.is_refuse_entry,
                                              'mac_ids': config.mac_ids},
                                   'scenarios': list(scenarios),
                                   'mac_ids': mac_ids}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_default_config_with_scenario_id(request):
    scenario_id = request.GET.get('scenario_id', '')

    scenario = Scenario.objects.filter(id=scenario_id).first()

    if not scenario:
        return Response(status=400, data={'message': 'Scenario not found'})

    scenarios = Scenario.objects.values('id', 'scenario_title')
    mac_ids = User.objects.exclude(mac_id="").values_list('mac_id', flat=True)

    return Response(data={'data': {'config': {'scenario__id': scenario.id,
                                              'config': scenario.default_config},
                                   'scenarios': list(scenarios), 'mac_ids': mac_ids}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_configs_with_scenario_id(request):
    scenario_id = request.GET.get('scenario_id', '')

    scenario = Scenario.objects.filter(id=scenario_id).first()

    if not scenario:
        return Response(status=400, data={'message': 'Scenario not found'})

    configs = Config.objects.filter(scenario_id=scenario_id).values(
        'id', 'scenario_id', 'breeding_point', 'is_owner_at_home', 'is_owner_appeal', 'config',
        'is_refuse_entry', 'mac_ids', 'dateCreated', 'dateUpdated'
    )

    return Response(data={'data': {'configs': list(configs), 'scenario_title': scenario.scenario_title}})
