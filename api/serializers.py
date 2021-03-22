from rest_framework import serializers

from .models import Role, Score, User

class RoleSerializers(serializers.ModelSerializer):

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
            'scoresUser'
        )

class ScoreSerializers(serializers.ModelSerializer):

    class Meta:

        model = Score

        fields = (
            "id",
            "sender",
            "receiver",
            "score_technical",
            "score_social",
            "data_created",
            "scoresUser_id"
        )