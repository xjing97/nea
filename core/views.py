from django.http import JsonResponse
from rest_framework.response import Response
from nea.decorators import permission_exempt
from .models import User
from .serializers import SignUpSerializer, LoginSerializer, UserSerializer
from rest_framework.decorators import api_view


@api_view(['POST'])
@permission_exempt
def sign_up(request):
    form = SignUpSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.sign_up()
    return res.as_json_response()


@api_view(['POST'])
@permission_exempt
def login(request):
    form = LoginSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.login()
    return res.as_json_response()


@api_view(['POST'])
@permission_exempt
def editUser(request):
    form = UserSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.update()
    return res.as_json_response()


@api_view(['POST'])
@permission_exempt
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
