from datetime import timedelta, datetime

from django.contrib.auth import authenticate
from django.db import transaction
from django.http import JsonResponse
from rest_framework import serializers
from typing import MutableMapping
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from core.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)
    grc = serializers.CharField(max_length=256, required=False)
    regional_office = serializers.CharField(max_length=256, required=False)
    soeId = serializers.CharField(max_length=256, required=False)
    department = serializers.CharField(max_length=256, required=True)
    # profile_pic = serializers.ImageField(allow_null=True, required=False)
    # password = serializers.CharField(max_length=256, required=True)

    def validate(self, data: MutableMapping[str, str]):
        username = data.get('username')
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            raise serializers.ValidationError({'username': 'Username is already taken'}, code='invalid')

        if not data.get('soeId'):
            raise serializers.ValidationError({'soeId': 'Soe ID is required'}, code='invalid')
        if not data.get('grc'):
            raise serializers.ValidationError({'grc': 'GRC is required'}, code='invalid')
        if not data.get('regional_office'):
            raise serializers.ValidationError({'regional_office': 'Regional Office is required'}, code='invalid')

        return data

    def create_acc(self):
        with transaction.atomic():
            print(self.validated_data)
            user = User.objects.admin_create_user(**self.validated_data)
                
        return JsonResponse(data={'data': {'user_id': user.id}, 'message': "User creation success"})


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=False)
    password = serializers.CharField(max_length=256, required=False)
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

    def login(self):
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

        data = {'refresh_token': str(token), 'access_token': str(token.access_token), 'user_id': user.id,
                'user_name': user.username, 'expires_at': datetime.now() + RefreshToken.lifetime,
                'first_time_login': first_time_login}
        return JsonResponse(data={'data': data, 'message': 'Login successfully'})


class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=256, required=True)
    grc = serializers.CharField(max_length=256, required=True)
    regional_office = serializers.CharField(max_length=256, required=True)
    soeId = serializers.CharField(max_length=256, required=True)
    department = serializers.CharField(max_length=256, required=True)
    # password = serializers.CharField(max_length=256, required=True)

    def validate(self, data: MutableMapping[str, str]):
        user_id = data.get('user_id')
        user = User.objects.filter(id=user_id, is_active=True).first()
        if user is None:
            raise serializers.ValidationError('User does not exists', code='invalid')

        return data

    def update(self):
        user_id = self.validated_data['user_id']
        user = User.objects.filter(id=user_id).first()
        with transaction.atomic():
            if user:
                user.username = self.validated_data['username']
                user.grc = self.validated_data['grc']
                user.regional_office = self.validated_data['regional_office']
                user.soeId = self.validated_data['soeId']
                user.department = self.validated_data['department']
                # user.password = self.validated_data['password']
                user.save()

                return JsonResponse(data={'data': {'user_id': user.id, 'username': user.username, 'soeId': user.soeId,
                                                   'department': user.department, 'grc': user.grc,
                                                   'regional_office': user.regional_office},
                                          'message': "Updated user successfully"})

            else:
                return JsonResponse(status_code='400', data={'data': {'user_id': user.id}, 'message': "User not found"})
