from rest_framework import serializers

from .models import Role, Score, User

# to find the avg values based on receiver
from django.db.models import Avg, Count


class RoleSerializers(serializers.ModelSerializer):

    data_created = serializers.DateTimeField(format="%d/%m/%Y")
    users = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='user-detail'
    )

    class Meta:

        model = Role

        fields = (
            "id",
            "role",
            "data_created",
            "users"
        )

class UserSerializers(serializers.ModelSerializer):

    data_created = serializers.DateTimeField(format="%d/%m/%Y")
    data_updated = serializers.DateTimeField(format="%d/%m/%Y")
    
    avg_score_tech = serializers.SerializerMethodField()
    avg_score_social = serializers.SerializerMethodField()
    print(avg_score_social, 'teste aquiii')
    scoresUser = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='score-detail'
    )
    
    class Meta:

        model = User

        fields = (
            'id',
            'slack_user_id',
            'role',
            'active',
            'data_created',
            'data_updated',
            'avg_score_tech',
            'avg_score_social',
            'scoresUser'
        )

    # this function has have the same name of avg_score_tech with get 
    def get_avg_score_tech(self, obj):
        # prints the average value of score_tech
        average_tech = Score.objects.all().aggregate(Avg('score_technical')).get('score_technical__avg')
        slack_id = User.slack_user_id
        score_receiver = Score.receiver
        # Need to find the correlation between slack_user_id and receiver
        
        
        return average_tech

    def get_avg_score_social(self, obj):
        # prints the average value of score_social
        average_social = Score.objects.all().aggregate(Avg('score_social')).get('score_social__avg')
        return average_social
class ScoreSerializers(serializers.ModelSerializer):

    data_created = serializers.DateTimeField(format="%d/%m/%Y")
    class Meta:

        model = Score

        fields = (
            "id",
            "sender",
            "receiver",
            "score_technical",
            "score_social",
            "data_created",
            "scoresUser"
        )