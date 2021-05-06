import json
import os
from datetime import datetime, timedelta
from decimal import Decimal
from distutils.util import strtobool

from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator
from django.db.models import Q, DateTimeField, CharField, TimeField, F, Case, When, Value, ExpressionWrapper, \
    DurationField
from django.db.models.functions import Lower, Cast, TruncSecond, Extract
from django.shortcuts import render

# Create your views here.
from django.views.static import serve
from pytz import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.models import Config
from core.models import User
from module.models import Scenario, Module
from nea.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from nea.settings import BASE_DIR
from nea.validator import ValidateIsAdmin
from .models import Result, ResultBreakdown


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_result(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id).first()
    data = request.data

    required_params_list = ('user_scores', 'total_scores', 'inspection_start', 'inspection_end', 'time_spend',
                            'mac_id', 'config_id', 'result_breakdown', 'teleport_path', 'audio_file')
    for param_name in required_params_list:
        if param_name not in data:
            return Response(status=400, data={'message': 'Required argument %s is missing' % param_name})

    # result = data['result']
    user_scores = Decimal(data['user_scores'])
    total_scores = Decimal(data['total_scores'])
    # is_pass = True if data['is_pass'] == 'true' else False
    start_time_str = data['inspection_start']
    end_time_str = data['inspection_end']
    time_spend_str = data['time_spend']
    mac_id = data['mac_id']
    config_id = data['config_id']
    breeding_points_found = data.get('breeding_points_found', '')
    breeding_points_not_found = data.get('breeding_points_not_found', '')
    critical_failure = data.get('critical_failure', None)
    result_breakdown = data['result_breakdown']
    teleport_path = data['teleport_path']
    audio_file = data['audio_file']
    is_completed_str = data.get('is_completed', 'true')

    if not critical_failure:
        critical_failure = None

    try:
        start_time = timezone('Asia/Singapore').localize(datetime.strptime(start_time_str, '%d/%m/%Y %H:%M:%S'))
        end_time = timezone('Asia/Singapore').localize(datetime.strptime(end_time_str, '%d/%m/%Y %H:%M:%S'))

        time_spend_timedelta = timedelta(seconds=float(time_spend_str))
        time_spend = (datetime(year=1990, month=1, day=1, hour=0, minute=0,
                               second=0) + time_spend_timedelta).strftime('%H:%M:%S')

        is_completed = strtobool(is_completed_str)

    except Exception as e:
        print(str(e))
        return Response(status=400, data={'message': str(e)})

    config_obj = Config.objects.filter(id=config_id).first()

    if not config_obj:
        print('Config ID %s is invalid' % config_id)
        return Response(status=400, data={'message': 'Config ID is invalid'})

    scenario = config_obj.scenario
    passing_score = config_obj.passing_score
    result_percentage = user_scores / total_scores * 100

    # Shouldn't do in this way, it should be fixed from unity side
    if result_percentage > 100:
        result_percentage = 100

    is_pass = True if float(result_percentage) > passing_score and not critical_failure else False

    breeding_points = config_obj.breeding_point

    if scenario:
        result = Result.objects.create(user=user, scenario=scenario, results=Decimal(result_percentage),
                                       user_scores=user_scores, total_scores=total_scores, is_pass=is_pass,
                                       start_time=start_time, end_time=end_time, breeding_points=breeding_points,
                                       breeding_points_found=breeding_points_found,
                                       breeding_points_not_found=breeding_points_not_found,
                                       time_spend=time_spend, mac_id=mac_id, config=config_obj.config,
                                       passing_score=passing_score,
                                       result_breakdown=result_breakdown, teleport_path=teleport_path,
                                       critical_failure=critical_failure, is_completed=is_completed,
                                       audio=audio_file)
        result.create_result_breakdown()
        return Response(status=200, data={'result_id': result.uid, 'message': 'Stored result successfully'})
    else:
        print('Scenario is invalid')
        return Response(status=400, data={'message': 'Scenario ID is invalid'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_results(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    page = int(request.GET.get('page', 1))
    items = int(request.GET.get('items', 10))
    sorter_value = json.loads(request.GET.get('sorterValue', '{}'))
    column_filter_value = json.loads(request.GET.get('columnFilterValue', '{}'))
    universal_filter_value = request.GET.get('filter', '')

    retrieve_values = ['id', 'uid', 'user__username', 'user__soeId', 'user__division__grc__grc_name',
                       'user__division__division_name', 'user__division__grc__user_department__department_name',
                       'user__division__grc__id', 'user__division__id', 'user__division__grc__user_department__id',
                       'time_spend', 'results', 'is_pass', 'scenario_id', 'scenario__module_id',
                       'date_created', 'start_time_str', 'end_time_str', 'is_pass_str', 'is_completed_str',
                       'scenario__scenario_title', 'scenario__module__module_name', 'scenario__inspection_site',
                       'dateCreated', 'audio', 'start_time', 'end_time', 'breeding_points', 'breeding_points_not_found',
                       'user_scores', 'total_scores', 'mac_id', 'passing_score', 'teleport_path',
                       'breeding_points_found', 'critical_failure', 'config', 'result_breakdown']

    if 'column' in sorter_value and sorter_value['column']:
        sort_column = sorter_value['column']
        if sort_column not in ['results', 'critical_failure']:
            sort_column = Lower(sort_column)
        if not sorter_value['asc']:
            sort_column = sort_column.desc()

    else:
        sort_column = '-date_created'

    q = Q(user__is_active=True)

    if universal_filter_value:
        universal_q = Q()
        for v in retrieve_values:
            if v not in ['id', 'config', 'result_breakdown', 'audio', 'scenario_id', 'scenario__module_id','is_pass',
                         'user__division__grc__id', 'user__division__id', 'user__division__grc__user_department__id',
                         'start_time', 'end_time',
                         'breeding_points', 'breeding_points_not_found', 'breeding_points_found']:
                universal_q.add(Q(**{'{}__icontains'.format(v): universal_filter_value}), Q.OR)
        q &= universal_q

    if column_filter_value:
        for key in column_filter_value:
            if column_filter_value[key]:
                q.add(Q(**{'{}__icontains'.format(key): column_filter_value[key]}), Q.AND)

    total_items = Result.objects.annotate(
        date_created=Cast(
            TruncSecond('dateCreated', DateTimeField()), CharField()
        ),
        start_time_str=Cast(
            TruncSecond('start_time', DateTimeField()), CharField()
        ),
        end_time_str=Cast(
            TruncSecond('end_time', DateTimeField()), CharField()
        ),
        is_pass_str=Case(When(is_pass=True, then=Value("Passed")), default=Value("Failed"), output_field=CharField()),
        is_completed_str=Case(When(is_completed=True, then=Value("Completed")), default=Value("Incomplete"),
                              output_field=CharField()),
    ).filter(q).count()

    total_page_num = total_items // items + 1 if total_items % items else total_items / items

    result = Result.objects.annotate(
        date_created=Cast(
            TruncSecond('dateCreated', DateTimeField()), CharField()
        ),
        start_time_str=Cast(
            TruncSecond('start_time', DateTimeField()), CharField()
        ),
        end_time_str=Cast(
            TruncSecond('end_time', DateTimeField()), CharField()
        ),
        is_pass_str=Case(When(is_pass=True, then=Value("Passed")), default=Value("Failed"), output_field=CharField()),
        is_completed_str=Case(When(is_completed=True, then=Value("Completed")), default=Value("Incomplete"),
                              output_field=CharField()),
    ).values(*retrieve_values).order_by(sort_column)

    paginator = Paginator(result, items)
    paginated_result = paginator.get_page(page)

    result_details = ResultBreakdown.objects.filter(
        user__is_active=True
    ).values(
        'result__uid', 'scenario__module__module_name', 'scenario__scenario_title', 'scene_name', 'event_id',
        'event_keywords', 'event_type', 'description', 'action_performed', 'keywords_spoken', 'user_event_scores',
        'user_location', 'time_spent', 'total_event_scores', 'event_is_pass', 'is_critical', 'overall_is_pass',
        'dateCreated', 'dateUpdated')

    all_modules_scenarios = Module.objects.values('id', 'module_name', 'scenario__id', 'scenario__scenario_title')

    return Response(status=200,
                    data={
                        'data': {
                            'results': list(paginated_result),
                            'all_results': list(result),
                            'result_details': list(result_details),
                            'modules_scenarios': list(all_modules_scenarios),
                            'total_page_num': total_page_num
                        }, 'message': 'Get all results successfully'})


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
        user__is_active=True, uid=result_id
    ).values(
        'id', 'uid', 'user__username', 'user__soeId', 'user__division__grc__grc_name', 'config', 'critical_failure',
        'user__division__grc__id', 'user__division__id', 'user__division__grc__user_department__id',
        'user__division__division_name', 'user__division__grc__user_department__department_name', 'passing_score',
        'time_spend', 'results', 'is_pass', 'user_scores', 'total_scores', 'scenario_id', 'scenario__module_id',
        'scenario__scenario_title', 'scenario__module__module_name', 'scenario__inspection_site', 'dateCreated',
        'audio', 'start_time', 'end_time', 'breeding_points', 'breeding_points_not_found', 'breeding_points_found',
        'result_breakdown', 'teleport_path', 'is_completed'
    )

    result_breakdown = ResultBreakdown.objects.filter(
        user__is_active=True, result__uid=result_id
    ).values()

    if not result:
        return Response(status=400, data={'message': 'Result not found'})

    return Response(status=200, data={'data': {'result': list(result), 'result_breakdown': list(result_breakdown)},
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_critical_failure(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    from_date_str = request.GET.get('fromDate', '')
    to_date_str = request.GET.get('toDate', '')

    filter_division = request.GET.get('filterDivision', 'all')
    filter_grc = request.GET.get('filterGrc', 'all')
    filter_department = request.GET.get('filterDepartment', 'all')

    filter_title = request.GET.get('filterTitle', None)

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d') if from_date_str else \
            datetime(datetime.now().year, datetime.now().month, 1)
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d') + relativedelta(days=1) if to_date_str else datetime.now()

        critical_failure_overview, critical_failure_details, failure_dict = Result.objects.get_critical_failure(
            from_date, to_date, filter_division, filter_grc, filter_department, filter_title)

    except Exception as e:
        return Response(status=400, data={'message': str(e)})

    return Response(status=200, data={'overview': critical_failure_overview, 'details': list(critical_failure_details),
                                      'description': failure_dict,
                                      'message': 'Success'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event_analysis(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    from_date_str = request.GET.get('fromDate', '')
    to_date_str = request.GET.get('toDate', '')

    filter_division = request.GET.get('filterDivision', 'all')
    filter_grc = request.GET.get('filterGrc', 'all')
    filter_department = request.GET.get('filterDepartment', 'all')

    filter_title = request.GET.get('filterTitle', None)

    show_crit_only_str = request.GET.get('showCriticalEventOnly', 'false')

    if show_crit_only_str == 'false':
        show_crit_only = False
    else:
        show_crit_only = True

    last_attempt_only_str = request.GET.get('lastAttemptOnly', 'false')

    if last_attempt_only_str == 'false':
        last_attempt_only = False
    else:
        last_attempt_only = True

    try:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d') if from_date_str else \
            datetime(datetime.now().year, datetime.now().month, 1)
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d') + relativedelta(days=1) if to_date_str else datetime.now()

        event_info = ResultBreakdown.objects.get_event_analysis(
            from_date, to_date, filter_division, filter_grc, filter_department, filter_title, show_crit_only,
            last_attempt_only)

    except Exception as e:
        return Response(status=400, data={'message': str(e)})

    return Response(status=200, data={'event_info': event_info,
                                      'message': 'Success'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_result_breakdown(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    data = request.data
    required_params_list = ('resultId', 'resultBreakdown')
    for param_name in required_params_list:
        if param_name not in data:
            return Response(status=400, data={'message': 'Required argument %s is missing' % param_name})

    result_id = data['resultId']
    result_breakdown = data['resultBreakdown']
    scores = data.get('scores', None)
    user_scores = data.get('userScores', None)

    result = Result.objects.filter(uid=result_id).first()
    if not result:
        return Response(status=400, data={'message': 'Result not found'})

    try:
        result.update_result_breakdown(result_breakdown, scores, user_scores)
        return Response(status=200, data={'message': 'Success'})
    except Exception as e:
        return Response(status=400, data={'message': str(e)})

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def play_audio_file(request, path):
    document_root = os.path.join(BASE_DIR, 'upload/upload/audio/')

    return serve(request, path, document_root=document_root, show_indexes=False)