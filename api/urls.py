from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, OutgoingRequestViewSet, IncomingRequestViewSet

app_name = 'api'

router = SimpleRouter()

router.register('users', UserViewSet)
router.register('friend_requests/outgoing', OutgoingRequestViewSet, basename='friends/outgoing')
router.register('friend_requests/incoming', IncomingRequestViewSet, basename='friends/incoming')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
