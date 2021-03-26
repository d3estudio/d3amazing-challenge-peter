from rest_framework import generics, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.generics import get_object_or_404

from .models import Role, Score, User
from .serializers import RoleSerializers, ScoreSerializers, UserSerializers

# to find thje 
from django.db.models import Avg, Count
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

class UserAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializers

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

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializers

    @action(detail=True, methods=['get'])
    def score(self, request, pk=None):

        score = Score.objects.filter(scoreUser=pk)

        serializer = ScoreSerializers(score)

        return Response(serializer.data)


  
    

    @action(detail=True, methods=['get'])
    def avg_social(self, request, pk=None):
        
        slack_id = User.objects.get(slack_user_id)

        receiver = Score.objects.get(receiver)

        avg_score_social = Score.objects.all().aggregate(Avg('score_social')).get('score_social__avg')

        serializer = UserSerializers(avg_score_social, many=True)

        if slack_id == receiver:

            return Response(serializer.data)


class ScoreViewSet(viewsets.ModelViewSet):

    queryset = Score.objects.all()
    serializer_class = ScoreSerializers