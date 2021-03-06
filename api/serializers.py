from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(["Password fields didn't match."])

        if attrs['password'] == attrs['old_password']:
            raise serializers.ValidationError(['New password must be different from old password.'])

        return attrs

    def validate_old_password(self, value):
        user = User.objects.filter(id=self.context['request'].user.id).first()
        if not user:
            raise serializers.ValidationError(["User not found"])
        if not user.check_password(value):
            raise serializers.ValidationError(["Old password is not correct"])
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
