from rest_framework import generics, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.generics import get_object_or_404

from .models import Role, Score, User
from .serializers import RoleSerializers, ScoreSerializers, UserSerializers

class RolesAPIView(generics.ListCreateAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializers

class RoleAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Role.objects.all()
    serializer_class = RoleSerializers

class ScoresAPIView(generics.ListCreateAPIView):

    queryset = Score.objects.all()
    serializer_class = ScoreSerializers

class ScoreAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Score.objects.all()
    serializer_class = ScoreSerializers

class UsersAPIView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_queryset(self):

        if self.kwargs.get('roles_pk'):

            return self.queryset.filter(roles_id=self.kwargs.get('roles_pk'))

        return self.queryset.all()

class UserAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_object(self):

        if self.kwargs.get('roles_pk'):

            return get_object_or_404(self.get_queryset(), roles_id=self.kwargs.get('roles_pk'), pk=self.kwargs.get('user_pk'))

        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('user_pk'))

class RoleViewSet(viewsets.ModelViewSet):

    queryset = Role.objects.all()
    serializer_class = RoleSerializers

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):

        self.pagination_class.page_size = 3

        users = User.objects.filter(role_id=pk)

        page = self.paginate_queryset(users)

        if page is not None:

            serializer = UserSerializers(page, many=True)

            return self.get_paginated_response(serializer.data)


        serializer = UserSerializers(users, many=True)

        return Response(serializer.data)

class UserViewSet(
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    viewsets.GenericViewSet
                ):

    queryset = User.objects.all()
    serializer_class = UserSerializers

class ScoreViewSet(
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    viewsets.GenericViewSet
                ):

    queryset = Score.objects.all()
    serializer_class = ScoreSerializers