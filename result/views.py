from datetime import datetime, timedelta
from decimal import Decimal

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import User
from module.models import Scenario, Module
from nea.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Result


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_result(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id).first()
    data = request.data
    scenario_id = data['scenario_id']
    result = data['result']
    # is_pass = True if data['is_pass'] == 'true' else False
    time_spend_str = data['time_spend']  # format should be HH:mm:ss
    mac_id = data['mac_id']

    try:
        dt = datetime.strptime(time_spend_str, '%H:%M:%S')
        time_spend = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)

    except Exception as e:
        return Response(status=400, data={'message': 'Invalid time_spend. Format should be HH:mm:ss'})

    scenario = Scenario.objects.filter(id=scenario_id).first()
    passing_score = scenario.module.passing_score
    is_pass = True if float(result) > passing_score else False
    if scenario:
        result = Result.objects.create(user=user, scenario=scenario, results=Decimal(result), is_pass=is_pass,
                                       time_spend=time_spend)
        return Response(status=200, data={'result_id': result.id, 'message': 'Stored result successfully'})
    else:
        return Response(status=400, data={'message': 'Scenario ID is invalid'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_results(request):
    result = Result.objects.values(
        'user__username', 'user__department', 'user__soeId', 'time_spend', 'results', 'is_pass', 'scenario_id',
        'scenario__module__module_name', 'scenario__high_rise', 'dateCreated')
    return Response(status=200, data={'data': list(result), 'message': 'Get all results successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_results_by_date(request):
    months = None
    result = None
    if request.GET.get('dataType', 'Month') == 'Year':
        result, months = Result.objects.get_results_by_month(group_by_department=True)
    elif request.GET.get('dataType', 'Month') == 'Month':
        result = Result.objects.get_results_by_date(group_by_department=True)
    return Response(status=200, data={'data': result, 'months': months, 'message': 'Success'})
