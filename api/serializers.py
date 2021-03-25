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
    
    scoresUser = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='score-detail'
    )
    avg_score_tech = serializers.SerializerMethodField()
    avg_score_social = serializers.SerializerMethodField()
    

    # succes print 4.5000
    # will get all the items from the Score object
    # will aggregate all the items and sum up getting the average value
    # the get() will get the key value from the aggregate output
    print(Score.objects.all().aggregate(Avg('score_social')).get('score_social__avg'))
    print(Score.objects.all().aggregate(Avg('score_technical')).get('score_technical__avg'))
    
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
        average_tech = Score.objects.all().aggregate(Avg('score_technical')).get('score_technical__avg')
       
        return average_tech

    def get_avg_score_social(self, obj):
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