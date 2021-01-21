from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from module.models import Module
from nea.validator import ValidateIsAdmin


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_modules(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    modules = Module.objects.get_all_modules()

    return Response(data={'data': modules})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count_modules_by_difficulty(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    modules = Module.objects.count_modules_by_difficulty()

    return Response(data={'data': modules})
