from datetime import datetime

from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from nea.decorators import permission_exempt, permission_classes
from rest_framework.permissions import IsAuthenticated

from nea.validator import ValidateIsAdmin
from result.models import Result
from .models import User
from .serializers import SignUpSerializer, LoginSerializer, UserSerializer
from rest_framework.decorators import api_view


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_acc(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    form = SignUpSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.create_acc()
    return res


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mass_create_acc(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

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
        print(form.errors)
        return Response(status=400, data=form.errors)
    print(form.validated_data['user_id'])
    validator = ValidateIsAdmin()
    if not validator.validate(form.validated_data['user_id']):
        return Response(status=403, data={'username': [ErrorDetail(string=validator.error_message, code='blank')]})

    res = form.login()
    return res


@api_view(['POST'])
@permission_exempt
def renewToken(request):
    if 'refreshToken' not in request.data:
        return Response(status=400, data={'message': 'Required argument refreshToken is missing'})

    refresh_token = request.data['refreshToken']
    try:
        token = RefreshToken(refresh_token)

        data = {'refresh_token': str(token), 'access_token': str(token.access_token),
                'expires_at': datetime.now() + RefreshToken.lifetime}
        return Response(data={'data': data})
    except Exception as e:
        return Response(status=400, data={'message': str(e)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    if 'user_id' not in request.GET:
        return Response(status=400, data={'message': 'Required argument user_id is missing'})

    user_id = request.GET.get('user_id', '')
    user = User.objects.filter(id=user_id).first()
    if user:
        res = Response(data={'data': {'user_id': user.id,
                                      'username': user.username,
                                      'grc': user.grc,
                                      'regional_office': user.regional_office,
                                      'department': user.department,
                                      'soeId': user.soeId,
                                      }})
    else:
        res = Response(status=400, data={'error_message': 'User not found'})
    return res


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsers(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    user = User.objects.filter(
        is_staff=False, is_active=True
    ).values(
        'id', 'username', 'grc', 'regional_office', 'department', 'soeId'
    )
    return Response(data={'data': list(user), 'message': 'Get all users successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changeUserPassword(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    data = request.data
    required_params_list = ('userId', 'newPassword', 'confirmPassword')
    for param_name in required_params_list:
        if param_name not in data:
            return Response(status=400, data={'message': 'Required argument %s is missing' % param_name})

    user_id = data['userId']
    new_password = data['newPassword']
    confirm_password = data['confirmPassword']
    if new_password != confirm_password:
        return Response(status=400, data={'message': {"confirmPassword": "Password fields didn't match."}})

    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response(status=400, data={'message': {"userId": "User not found"}})

    user.set_password(new_password)
    user.save()

    return Response(data={'data': {'username': user.username, 'user_id': user.id, 'pwd': user.password}, 'message': 'Password changed successfully.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editUser(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    form = UserSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.update()
    return res


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    if 'user_id' not in request.data:
        return Response(status=400, data={'message': 'Required argument user_id is missing'})

    data = request.data
    user_id = data['user_id']

    user = User.objects.filter(id=user_id).first()

    if user and user.is_active:
        user.is_active = False
        user.save()

        return Response(data={'username': user.username, 'message': "User '" + user.username + "' is deleted"})

    else:
        return Response(status=400, data={'message': "User " + user.username + " not found"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id).first()
    user.mac_id = ''
    user.save()
    return Response(data={'message': "User logout successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDashboard(request):
    validator = ValidateIsAdmin()
    if not validator.validate(request.user.id):
        return Response(status=403, data={'message': validator.error_message})

    department_active = User.objects.get_total_users_by_department()
    overall_pass_fail = Result.objects.get_total_result_status()
    module_pass_fail = Result.objects.group_result_status_by_module()
    return Response(data={'department_active': list(department_active),
                          'overall_pass_fail': overall_pass_fail,
                          'module_pass_fail': list(module_pass_fail)})
