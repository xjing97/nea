from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from module.models import Module, Scenario
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_quiz_attempt(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    data = request.data
    required_params_list = ('quizAttempt', 'scenarioId')
    for param_name in required_params_list:
        if param_name not in data:
            return Response(status=400, data={'message': 'Required argument %s is missing' % param_name})

    quiz_attempt = data['quizAttempt']
    scenario_id = data['scenarioId']

    scenario = Scenario.objects.filter(id=scenario_id).first()

    if not scenario:
        return Response(status=400, data={'message': 'Scenario not found'})

    scenario.edit_quiz_attempt(quiz_attempt)

    return Response(data={'quiz_attempt': quiz_attempt, 'message': "Quiz Attempt updated successfully"})
