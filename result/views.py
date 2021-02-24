from datetime import datetime, timedelta
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.models import Config
from core.models import User
from module.models import Scenario, Module
from nea.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from nea.validator import ValidateIsAdmin
from .models import Result


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_result(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id).first()
    data = request.data

    required_params_list = ('result', 'inspection_start', 'inspection_end', 'time_spend', 'mac_id', 'config_id',
                            'result_breakdown', 'teleport_path', 'audio_file')
    for param_name in required_params_list:
        if param_name not in data:
            return Response(status=400, data={'message': 'Required argument %s is missing' % param_name})

    result = data['result']
    # is_pass = True if data['is_pass'] == 'true' else False
    start_time_str = data['inspection_start']
    end_time_str = data['inspection_end']
    time_spend_str = data['time_spend']  # format should be HH:mm:ss
    mac_id = data['mac_id']
    config_id = data['config_id']
    breeding_points_found = data.get('breeding_points_found', '')
    breeding_points_not_found = data.get('breeding_points_not_found', '')
    critical_failure = data.get('critical_failure', '')
    result_breakdown = data['result_breakdown']
    teleport_path = data['teleport_path']
    audio_file = data['audio_file']

    try:
        dt = datetime.strptime(time_spend_str, '%H:%M:%S')
        time_spend = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
        start_time = datetime.strptime(start_time_str, '%d/%m/%Y %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%d/%m/%Y %H:%M:%S')

    except Exception as e:
        return Response(status=400, data={'message': str(e)})

    config_obj = Config.objects.filter(id=config_id).first()

    if not config_obj:
        return Response(status=400, data={'message': 'Config ID is invalid'})

    scenario = config_obj.scenario
    passing_score = config_obj.passing_score
    is_pass = True if float(result) > passing_score and not critical_failure else False

    breeding_points = config_obj.breeding_point

    if scenario:
        result = Result.objects.create(user=user, scenario=scenario, results=Decimal(result), is_pass=is_pass,
                                       start_time=start_time, end_time=end_time, breeding_points=breeding_points,
                                       breeding_points_found=breeding_points_found,
                                       breeding_points_not_found=breeding_points_not_found,
                                       time_spend=time_spend, mac_id=mac_id, config=config_obj.config,
                                       result_breakdown=result_breakdown, teleport_path=teleport_path,
                                       critical_failure=critical_failure,
                                       audio=audio_file)
        return Response(status=200, data={'result_id': result.id, 'message': 'Stored result successfully'})
    else:
        return Response(status=400, data={'message': 'Scenario ID is invalid'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_results(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    result = Result.objects.filter(
        user__is_active=True
    ).values(
        'id', 'user__username', 'user__soeId', 'user__division__grc__grc_name',
        'user__division__division_name', 'user__division__grc__user_department__department_name',
        'time_spend', 'results', 'is_pass', 'scenario_id', 'scenario__module_id', 'scenario__scenario_title',
        'scenario__module__module_name', 'scenario__inspection_site', 'dateCreated', 'audio', 'start_time', 'end_time',
        'breeding_points', 'breeding_points_not_found', 'breeding_points_found', 'critical_failure'
    ).order_by('-dateCreated')

    all_modules_scenarios = Module.objects.values('id', 'module_name', 'scenario__id', 'scenario__scenario_title')

    return Response(status=200, data={'data': {'results': list(result),
                                               'modules_scenarios': list(all_modules_scenarios)},
                                      'message': 'Get all results successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result_details(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    result_id = request.GET.get('result_id', '')
    if not result_id:
        return Response(status=400, data={'message': 'Required argument result_id is missing'})

    result = Result.objects.filter(
        user__is_active=True, id=result_id
    ).values(
        'id', 'user__username', 'user__soeId', 'user__division__grc__grc_name', 'config', 'critical_failure',
        'user__division__grc__id', 'user__division__id', 'user__division__grc__user_department__id',
        'user__division__division_name', 'user__division__grc__user_department__department_name',
        'time_spend', 'results', 'is_pass', 'scenario_id', 'scenario__module_id', 'scenario__scenario_title',
        'scenario__module__module_name', 'scenario__inspection_site', 'dateCreated', 'audio', 'start_time', 'end_time',
        'breeding_points', 'breeding_points_not_found', 'breeding_points_found', 'result_breakdown', 'teleport_path'
    )
    if not result:
        return Response(status=400, data={'message': 'Result not found'})

    return Response(status=200, data={'data': {'result': list(result)},
                                      'message': 'Get result details successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_results_by_date(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    data_type = request.GET.get('dataType', 'Day')
    from_date_str = request.GET.get('fromDate', '')
    to_date_str = request.GET.get('toDate', '')
    from_month_str = request.GET.get('fromMonth', '')
    to_month_str = request.GET.get('toMonth', '')

    if data_type == 'Day':
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d') if from_date_str else \
            datetime(datetime.now().year, datetime.now().month, 1)
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d') + relativedelta(days=1) if to_date_str else datetime.now()

        result, x_axis = Result.objects.get_results_with_date_range(from_date=from_date, to_date=to_date,
                                                                    group_by_department=True)
    else:
        from_month = datetime.strptime(from_month_str, '%Y-%m') if from_month_str else \
            datetime(datetime.now().year, datetime.now().month, 1) - relativedelta(months=11)
        to_month = datetime.strptime(to_month_str, '%Y-%m') + relativedelta(months=1) if to_month_str else datetime(
            datetime.now().year, datetime.now().month, 1) + relativedelta(months=1)

        result, x_axis = Result.objects.get_results_with_month_range(from_date=from_month, to_date=to_month,
                                                                     group_by_department=True)

    return Response(status=200, data={'data': result, 'x_axis': x_axis, 'message': 'Success'})
