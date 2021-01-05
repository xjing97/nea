from django.db.models import F, Case, When, Value, CharField, Count, IntegerField, BooleanField
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.models import Config
from core.models import User
from result.models import Result


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

    # check quiz can be retake or not and user's attempt
    attended_modules = Result.objects.filter(
        user__id=user_id
    ).values(
        'scenario__module__id'
    ).annotate(
        attempt=Count('scenario__module__id')
    )

    attended_dict = {}
    for module in list(attended_modules):
        attended_dict[module['scenario__module__id']] = module['attempt']

    whens = [
        When(scenario__module__id=k, then=v) for k, v in attended_dict.items()
    ]
    config = Config.objects.filter(
        mac_ids__contains=mac_id
    ).annotate(
        module_name=F('scenario__module__module_name'),
        building_type=Case(When(scenario__high_rise=True, then=Value('High rise')),
                           default=Value('Low rise'), output_field=CharField()),
        cover_photo=F('scenario__cover_image'),
        description=F('scenario__description'),
        level=F('scenario__level'),
        scenario_title=F('scenario__scenario_title'),
        passing_score=F('scenario__module__passing_score'),
        quiz_attempt=F('scenario__module__quiz_attempt'),
        user_attempt=Case(*whens, default=0, output_field=IntegerField()),
    ).annotate(
        user_can_attend=Case(
            When(user_attempt__lt=F('scenario__module__quiz_attempt'), then=Value(True)),
            default=Value(False), output_field=BooleanField()
        ),
    ).values(
        'id', 'config', 'module_name', 'building_type', 'cover_photo', 'description', 'level', 'scenario_title',
        'passing_score', 'user_can_attend', 'quiz_attempt', 'user_attempt'
    )

    return Response(data={'data': list(config)})
