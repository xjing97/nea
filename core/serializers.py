from datetime import timedelta, datetime

from django.contrib.auth import authenticate
from django.db import transaction
from django.http import JsonResponse
from rest_framework import serializers
from typing import MutableMapping
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from core.models import User
from department.models import Division, GRC, UserDepartment


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)
    division = serializers.CharField(max_length=256, required=False)
    grc = serializers.CharField(max_length=256, required=False)
    department = serializers.CharField(max_length=256, required=False)
    soeId = serializers.CharField(max_length=256, required=False)

    def validate(self, data: MutableMapping[str, str]):
        username = data.get('username')
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            raise serializers.ValidationError({'username': 'Invalid username. Username already exists'}, code='invalid')

        soe_id = data.get('soeId')
        if not soe_id:
            raise serializers.ValidationError({'soeId': 'SOE ID is required'}, code='invalid')

        duplicated_soe = User.objects.filter(soeId=soe_id).first()
        if duplicated_soe:
            raise serializers.ValidationError({'soeId': 'Invalid SOE ID. SOE ID already exists'}, code='invalid')

        division = data.get('division')

        if not division:
            raise serializers.ValidationError({'division': 'Division is required'}, code='invalid')

        grc = data.get('grc')
        department = data.get('department')

        if not grc and not department:
            division_obj = Division.objects.filter(id=division).first()
            if not division_obj:
                raise serializers.ValidationError({'division': 'Division does not exists'}, code='invalid')
        else:
            if not grc:
                raise serializers.ValidationError({'grc': 'GRC is required'}, code='invalid')
            if not department:
                raise serializers.ValidationError({'department': 'User Department is required'}, code='invalid')

            department_obj = UserDepartment.objects.filter(department_name=department).first()
            if not department_obj:
                raise serializers.ValidationError({'department': 'User Department does not exists'}, code='invalid')

            grc_obj = GRC.objects.filter(grc_name=grc, user_department=department_obj).first()
            if not grc_obj:
                raise serializers.ValidationError({'grc': 'GRC does not exists'}, code='invalid')

            division_obj = Division.objects.filter(division_name=division, grc=grc_obj).first()
            if not division_obj:
                raise serializers.ValidationError({'division': 'Division does not exists'}, code='invalid')

        return data

    def create_acc(self):
        try:
            with transaction.atomic():
                user = User.objects.admin_create_user(**self.validated_data)
            return JsonResponse(data={'data': {'user_id': user.id}, 'message': "User creation success"})

        except Exception as e:
            return JsonResponse(status=400, data={'message': str(e)})


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True, allow_blank=True)
    password = serializers.CharField(max_length=256, required=True, allow_blank=True)
    mac_id = serializers.CharField(max_length=256, required=False)

    def validate(self, data: MutableMapping[str, str]):
        if not data.get('username') and not data.get('password'):
            raise serializers.ValidationError({'username': 'Username is required', 'password': 'Password is required'},
                                              code='blank')

        if not data.get('username'):
            raise serializers.ValidationError({'username': 'Username is required'}, code='blank')
        if not data.get('password'):
            raise serializers.ValidationError({'password': 'Password is required'}, code='blank')

        user = authenticate(**data)
        if user is None:
            raise serializers.ValidationError('Username/Password does not match', code='credential-not-match')

        if not user.is_active:
            raise serializers.ValidationError('Account is deleted by admin', code='credential-not-match')

        data['user_id'] = user.id

        return data

    def login(self, login_type='unity-api'):
        user = authenticate(**self.validated_data)

        first_time_login = False
        if not user.last_login:
            first_time_login = True

        if 'mac_id' in self.validated_data:
            users = User.objects.select_for_update().filter(mac_id=self.validated_data['mac_id'])
            with transaction.atomic():
                for u in users:
                    u.mac_id = ""
                    u.save()
            user.mac_id = self.validated_data['mac_id']
        user.last_login = datetime.now()
        user.save()
        token = RefreshToken.for_user(user)

        if login_type == 'unity-api':
            # So Unity side will not need to keep refreshing token
            token.access_token.set_exp(lifetime=timedelta(days=1))

        data = {'refresh_token': str(token), 'access_token': str(token.access_token), 'user_id': user.id,
                'user_name': user.username, 'expires_at': datetime.now() + token.lifetime,
                'first_time_login': first_time_login}

        return JsonResponse(data={'data': data, 'message': 'Login successfully'})


class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=256, required=True)
    soeId = serializers.CharField(max_length=256, required=True)
    division = serializers.CharField(max_length=256, required=True)

    def validate(self, data: MutableMapping[str, str]):
        user_id = data.get('user_id')
        user = User.objects.filter(id=user_id, is_active=True).first()
        if user is None:
            raise serializers.ValidationError('User does not exists', code='invalid')

        return data

    def update(self):
        user_id = self.validated_data['user_id']
        user = User.objects.filter(id=user_id).first()
        division = Division.objects.filter(id=self.validated_data['division']).first()
        with transaction.atomic():
            if user:
                user.username = self.validated_data['username']
                user.soeId = self.validated_data['soeId']
                user.division = division
                user.save()

                return JsonResponse(data={'data': {'user_id': user.id, 'username': user.username, 'soeId': user.soeId,
                                                   'division': user.division.division_name},
                                          'message': "Updated user successfully"})

            else:
                return JsonResponse(status_code='400', data={'data': {'user_id': user.id}, 'message': "User not found"})
