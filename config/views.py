import json
from datetime import datetime

from django.db.models import F, Value
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.models import Config
from core.models import User
from module.models import Scenario
from nea.validator import ValidateIsAdmin


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
    if 'config_id' not in request.GET:
        return Response(status=400, data={'message': 'Required argument config_id is missing'})

    config_id = request.GET.get('config_id', '')

    config = Config.objects.filter(id=config_id, date_deleted__isnull=True).first()

    if not config:
        return Response(status=400, data={'message': 'Configuration not found'})

    scenarios = Scenario.objects.values('id', 'scenario_title')
    mac_ids = User.objects.exclude(mac_id="").values_list('mac_id', flat=True)

    return Response(data={'data': {'config': {'scenario__id': config.scenario_id,
                                              'config': config.config,
                                              'breeding_point': config.breeding_point,
                                              'passing_score': config.passing_score,
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

    configs = Config.objects.filter(scenario_id=scenario_id, date_deleted__isnull=True).values(
        'id', 'scenario_id', 'breeding_point', 'config', 'mac_ids', 'passing_score', 'dateCreated', 'dateUpdated'
    )

    return Response(data={'data': {'configs': list(configs), 'scenario_title': scenario.scenario_title}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_config(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    data = request.data
    scenario_id = data['scenario_id']
    config = data['config']
    breeding_points = data['breeding_points']
    mac_ids = data['mac_ids']
    passing_score = data['passing_score']

    scenario = Scenario.objects.filter(id=int(scenario_id)).first()

    if not scenario:
        return Response(status=400, data={'message': 'Scenario not found'})

    Config.objects.create(scenario=scenario, config=json.dumps(config, ensure_ascii=False), passing_score=passing_score,
                          breeding_point=json.dumps(breeding_points), mac_ids=json.dumps(mac_ids))

    return Response(data={'message': 'Success'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_config(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    data = request.data
    config_id = data['config_id']
    scenario_id = data['scenario_id']
    config = data['config']
    breeding_points = data['breeding_points']
    mac_ids = data['mac_ids']
    passing_score = data['passing_score']

    scenario = Scenario.objects.filter(id=int(scenario_id)).first()

    if not scenario:
        return Response(status=400, data={'message': 'Scenario ' + str(scenario_id) + ' not found'})

    config_obj = Config.objects.filter(id=int(config_id), date_deleted__isnull=True).first()

    if not config:
        return Response(status=400, data={'message': 'Configuration ' + str(config_id) + ' not found'})

    config_obj.scenario = scenario
    config_obj.mac_ids = json.dumps(mac_ids)
    config_obj.config = json.dumps(config, ensure_ascii=False)
    config_obj.breeding_point = json.dumps(breeding_points)
    config_obj.passing_score = passing_score
    config_obj.save()

    return Response(data={'message': 'Success'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_config(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    data = request.data
    config_id = data['config_id']

    config = Config.objects.filter(id=config_id).first()

    if not config:
        return Response(status=400, data={'message': 'Invalid Config ID: %s' % config_id})

    config.date_deleted = datetime.now()
    config.save()

    return Response(data={'message': 'Config %s is deleted' % config_id})
