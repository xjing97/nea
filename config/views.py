from django.db.models import F, Case, When, Value, CharField
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.models import Config


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_config_by_macid(request):
    mac_id = request.GET.get('mac_id', '')
    if not mac_id:
        return Response(status=400, data={'message': 'mac_id is required'})

    config = Config.objects.filter(
        mac_ids__contains=mac_id
    ).annotate(
        module_name=F('scenario__module__module_name'),
        building_type=Case(When(scenario__high_rise=True, then=Value('High rise')),
                           default=Value('Low rise'), output_field=CharField()),
        cover_photo=F('scenario__cover_image'),
        description=F('scenario__description'),
        level=F('scenario__level'),
        scenario_title=F('scenario__scenario_title')
    ).values(
        'config', 'module_name', 'building_type', 'cover_photo', 'description', 'level', 'scenario_title'
    )

    return Response(data={'data': list(config)})
