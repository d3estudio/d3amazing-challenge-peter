from django.urls import path, re_path
from rest_framework.routers import SimpleRouter

from .views import (
    RoleAPIView,
    RolesAPIView,
    ScoresAPIView,
    UserAPIView,
    UsersAPIView,
    RoleViewSet,
    UserViewSet,
    ScoreViewSet
)

router = SimpleRouter()
router.register('roles', RoleViewSet)
router.register('users', UserViewSet)
router.register('scores', ScoreViewSet)

urlpatterns = [
    path('roles/', RolesAPIView.as_view(), name='roles'),
    path('roles/<int:pk>/', RoleAPIView.as_view(), name='role'),
    path('roles/<int:roles_pk>/users/', UsersAPIView.as_view(), name='role_users'),
    # path('roles/<int:roles_pk>/users/<int:user_pk>/', UserAPIView.as_view(), name='role_user'), # erro
    path('users/', UsersAPIView.as_view(), name='users'),
    path('users/<int:user_pk>/', UserAPIView.as_view(), name='user'),
    path('scores/', ScoresAPIView.as_view(), name='scores')
]