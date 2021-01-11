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
