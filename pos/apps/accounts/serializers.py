from apps.core.services.status import *
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from .models import User, ActivationSMSCode
from apps.dashboard.models import UserRole


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRole
        fields = ("id", "name")

    def to_representation(self, instance: UserRole):
        data = super(RoleSerializer, self).to_representation(instance=instance)
        data["permissions"] = instance.permissions
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializes registration requests and creates a new user."""

    phone = serializers.CharField(max_length=13, required=True)
    password = serializers.CharField(max_length=128, min_length=5, write_only=True)

    class Meta:
        model = User
        fields = (
            "phone",
            "username",
            "first_name",
            "last_name",
            "fullname",
            "password"
        )

        # validators = [
        #     UniqueTogetherValidator(queryset=User.objects.all(), fields=['phone'])
        # ]

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     user.status = UserStatus.ACTIVE
    #     user.activated_date = timezone.now()
    #     user.save()
    #     return user

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("User already exists!")
        return value


class UserDetailSerializer(serializers.ModelSerializer):
    """ Full account serializers """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "fullname",
            "email",
            "phone",
            "activated_date",
            "images",
            "roles",
            "created_at"
        )


class UserListSerializer(serializers.ModelSerializer):
    """ Full account serializers """

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "fullname",
            "phone",
            "images",
            "roles",
            "created_at"
        )


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "fullname",
            "phone",
            "activated_date",
            "roles",
        )


class UserMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "fullname",
            "phone"
        )


class ActivationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivationSMSCode
        exclude = ["phone", "code", ]


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    password = serializers.CharField(max_length=25)


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    password = serializers.CharField(max_length=25)
    token = serializers.CharField(max_length=125)