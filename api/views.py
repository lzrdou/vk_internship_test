from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import User, FriendRequest
from api.serializers import UserSerializer, FriendRequestSerializer, FriendRequestToSerializer, \
    FriendRequestBySerializer


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для пользователей."""

    @action(
        permission_classes=[IsAuthenticated],
        methods=['post'],
        detail=True
    )
    def add_friend(self, request, id):
        """Метод добавления друга."""
        user = request.user
        friend = get_object_or_404(User, id=id)

        if user == friend:
            return Response(
                {'error': 'Нельзя добавить себя в друзья'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if friend in user.friends.all():
            return Response(
                {'error': 'Этот пользователь уже у вас в друзьях'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Проверка на то, что пользователь отправил нам запрос в друзья
        if FriendRequest.objects.filter(
                requested_by=friend,
                requested_to=user
        ).exists():
            friend_request = FriendRequest.objects.get(
                requested_by=friend,
                requested_to=user
            )
            friend_request.delete()
            if user.friends.add(friend):
                serializer = UserSerializer(
                    friend, context={'request': request}
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                {'error': 'Не удалось добавить в друзья'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            friend_request = FriendRequest.objects.create(
                    requested_by=user,
                    requested_to=friend
            )
            serializer = FriendRequestSerializer(
                friend_request, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': 'Не удалось отправить заявку на добавление в друзья', 'err_msg': e},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        permission_classes=[IsAuthenticated],
        methods=['delete'],
        detail=True
    )
    def delete_friend(self, request, id):
        """Метод удаления друга."""
        user = request.user
        friend = get_object_or_404(User, id=id)

        if friend not in user.friends.all():
            return Response(
                {'error': 'Этого пользователя нет у вас в друзьях'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.friends.remove(friend):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Не удалось удалить друга'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        permission_classes=[IsAuthenticated],
        methods=['get'],
        detail=False
    )
    def friends(self, request):
        """Метод просмотра списка друзей"""
        user = request.user
        friends = user.friends.all()
        serializer = UserSerializer(friends, many=True, context={'request': request})
        return Response(serializer.data)


class OutgoingRequestViewSet(ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет просмотра списка исходящих заявок."""
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestBySerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(requested_by=user).all()


class IncomingRequestViewSet(ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет просмотра списка исходящих заявок."""
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestToSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(requested_to=user)

    @action(
        permission_classes=[IsAuthenticated],
        methods=['post'],
        detail=True
    )
    def accept(self, request, pk):
        """Метод подтверждения заявки."""
        user = request.user
        friend_request = get_object_or_404(FriendRequest, id=pk)
        friend = get_object_or_404(User, id=friend_request.requested_by.id)
        try:
            user.friends.add(friend)
            serializer = UserSerializer(
                friend, context={'request': request}
            )
            friend_request.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception or IntegrityError as e:
            return Response(
                {'error': 'Не удалось добавить в друзья', 'err_msg': e},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        permission_classes=[IsAuthenticated],
        methods=['post'],
        detail=True
    )
    def decline(self, request, pk):
        """Метод подтверждения заявки."""
        friend_request = get_object_or_404(FriendRequest, id=pk)
        if friend_request.delete():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Не удалось отклонить заявку'},
            status=status.HTTP_400_BAD_REQUEST
        )
