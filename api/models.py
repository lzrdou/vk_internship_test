from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username_validator = RegexValidator(
        regex=r'^[a-zA-z0-9]',
        message=(
            'Неверный формат'
        )
    )
    username = models.CharField(
        max_length=150,
        validators=[username_validator, ],
        unique=True
    )
    friends = models.ManyToManyField(
        'self',
    )


class FriendRequest(models.Model):
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requested_by',
    )
    requested_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requested_to'
    )

    class Meta:
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'
        constraints = [
            models.UniqueConstraint(
                fields=['requested_by', 'requested_to'],
                name='unique_friend_request'
            )
        ]
