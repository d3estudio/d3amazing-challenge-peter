from rest_framework import serializers

from .models import Role, Score, User

class RoleSerializers(serializers.ModelSerializer):

    users = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='user-detail'
    )

    class Meta:

        # extra_kwargs = {
        #     'role': {
        #         'write_only': True
        #     }
        # }

        model = Role

        fields = (
            "id",
            "role",
            "data_created",
            "users"
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
            "data_created"
        )

class UserSerializers(serializers.ModelSerializer):

    class Meta:

        # extra_kwargs = {
        #     'slack_user_id': {
        #         'write_only': True
        #     }
        # }

        model = User

        fields = (
            'id',
            'slack_user_id',
            'role',
            'active',
            'data_created',
            'data_updated'
        )