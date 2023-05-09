from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from api.models import User, FriendRequest


class UserSerializer(BaseUserSerializer):
    """Общий сериализатор модели User."""
    friendship_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'friendship_status'
        )

    def get_friendship_status(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        if obj in user.friends.all():
            return 'Friend'
        if FriendRequest.objects.filter(
            requested_by=obj,
            requested_to=user
        ).exists():
            return 'Requested to be your friend'
        if FriendRequest.objects.filter(
            requested_to=obj,
            requested_by=user
        ).exists():
            return 'You requested to be friends'
        return 'Not friends'


class UserCreateSerializer(BaseUserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def to_representation(self, instance):
        serializer = UserCreateResponseSerializer(instance)
        return serializer.data


class UserCreateResponseSerializer(UserSerializer):
    """Сериализатор для ответа при создании пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


class FriendRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения заявок на добавление в друзья."""
    requested_by = serializers.CharField(source='requested_by.username')
    requested_to = serializers.CharField(source='requested_to.username')

    class Meta:
        model = FriendRequest
        fields = (
            'id',
            'requested_by',
            'requested_to'
        )


class FriendRequestBySerializer(FriendRequestSerializer):
    class Meta:
        model = FriendRequest
        fields = (
            'requested_to',
        )


class FriendRequestToSerializer(FriendRequestSerializer):
    class Meta:
        model = FriendRequest
        fields = (
            'id',
            'requested_by'
        )
