from datetime import datetime

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from nea.decorators import permission_exempt, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import SignUpSerializer, LoginSerializer, UserSerializer
from rest_framework.decorators import api_view


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_acc(request):
    form = SignUpSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.create_acc()
    return res


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mass_create_acc(request):
    invalid_creation = []
    records = request.data

    if not request.data:
        return Response(status=400, data={'data': {}, 'message': 'No data'})
    for record in records:
        form = SignUpSerializer(data=record)
        if not form.is_valid():
            invalid_creation.append({'user': record, 'error': form.errors})
        else:
            res = form.create_acc()

    if not invalid_creation:
        return Response(status=200, data={'data': {}, 'message': 'All accounts are created successfully'})
    else:
        return Response(
            status=400,
            data={
                'data': invalid_creation,
                'message': str(len(invalid_creation)) + ' account(s) is failed to create'
            })


@api_view(['POST'])
@permission_exempt
def login(request):
    form = LoginSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.login()
    return res


@api_view(['POST'])
@permission_exempt
def renewToken(request):
    print(request.data)
    user = request.user
    refresh_token = request.data['refreshToken']
    try:
        token = RefreshToken(refresh_token)

        data = {'refresh_token': str(token), 'access_token': str(token.access_token), 'user_id': user.id,
                'user_name': user.username, 'expires_at': datetime.now() + RefreshToken.lifetime}
        return Response(data={'data': data})
    except Exception as e:
        return Response(status=400, data={'message': str(e)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    user_id = request.GET.get('user_id')
    user = User.objects.filter(id=user_id).first()
    if user:
        res = Response(data={'data': {'user_id': user.id,
                                      'username': user.username,
                                      'date_of_birth': user.date_of_birth,
                                      'department': user.department,
                                      'soeId': user.soeId,
                                      }})
    else:
        res = Response(status=400, data={'error_message': 'User not found'})
    return res


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsers(request):
    user = User.objects.filter(is_staff=False, is_active=True).values('id', 'username', 'date_of_birth', 'department', 'soeId')
    return Response(data={'data': list(user), 'message': 'Get all users successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editUser(request):
    form = UserSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.update()
    return res


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    data = request.data
    user_id = data['user_id']

    user = User.objects.filter(id=user_id).first()
    if user:
        user.is_active = False
        user.save()

        return JsonResponse(data={'user_id': user.id}, message="User is deleted successfully")

    else:
        return JsonResponse(status_code='400', data={'user_id': user.id}, message="User not found")
