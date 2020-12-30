from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from module.models import Module


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_modules(request):
    modules = Module.objects.get_all_modules()

    return Response(data={'data': modules})
