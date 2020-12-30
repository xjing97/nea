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
    date_of_birth = serializers.DateField(required=False)
    soeId = serializers.CharField(max_length=256, required=True)
    department = serializers.CharField(max_length=256, required=True)
    # profile_pic = serializers.ImageField(allow_null=True, required=False)
    # password = serializers.CharField(max_length=256, required=True)

    def validate(self, data: MutableMapping[str, str]):
        username = data.get('username')
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            raise serializers.ValidationError({'username': 'Username is already taken'}, code='invalid')

        return data

    def create_acc(self):
        with transaction.atomic():
            user = User.objects.admin_create_user(**self.validated_data)
                
        return JsonResponse(data={'data': {'user_id': user.id}, 'message': "User creation success"})


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(max_length=256, required=True)
    mac_id = serializers.CharField(max_length=256, required=False)

    def validate(self, data: MutableMapping[str, str]):
        user = authenticate(**data)
        if user is None:
            raise serializers.ValidationError('Username/Password not match', code='credential-not-match')

        return data

    def login(self):
        user = authenticate(**self.validated_data)
        if 'mac_id' in self.validated_data:
            users = User.objects.select_for_update().filter(mac_id=self.validated_data['mac_id'])
            with transaction.atomic():
                for u in users:
                    u.mac_id = ""
                    u.save()
            user.mac_id = self.validated_data['mac_id']
            user.save()
        token = RefreshToken.for_user(user)

        data = {'refresh_token': str(token), 'access_token': str(token.access_token), 'user_id': user.id,
                'user_name': user.username, 'expires_at': datetime.now() + RefreshToken.lifetime}
        return JsonResponse(data={'data': data, 'message': 'Login successfully'})


class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=256, required=True)
    date_of_birth = serializers.DateField(required=True)
    soeId = serializers.CharField(max_length=256, required=True)
    department = serializers.CharField(max_length=256, required=True)
    # password = serializers.CharField(max_length=256, required=True)

    def validate(self, data: MutableMapping[str, str]):
        user_id = data.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise serializers.ValidationError('User does not exists', code='invalid')

        return data

    def update(self):
        user_id = self.validated_data['user_id']
        user = User.objects.filter(id=user_id).first()
        with transaction.atomic():
            if user:
                user.username = self.validated_data['username']
                user.date_of_birth = self.validated_data['date_of_birth']
                user.soeId = self.validated_data['soeId']
                user.department = self.validated_data['department']
                # user.password = self.validated_data['password']
                user.save()

                return JsonResponse(data={'data': {'user_id': user.id, 'username': user.username, 'soeId': user.soeId,
                                                   'department': user.department, 'date_of_birth': user.date_of_birth},
                                          'message': "Updated user successfully"})

            else:
                return JsonResponse(status_code='400', data={'data': {'user_id': user.id}, 'message': "User not found"})
