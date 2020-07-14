from rest_framework import serializers
from django.contrib.auth import get_user_model

from status.api.serializers import StatusInlineUserSerializer

User = get_user_model()



class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    status_list = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'uri',
            'username',
            'status_list',
        ]
    def get_uri(self, obj):
        return '/api/users/{username}'.format(username=obj.username)

    def get_status_list(self, obj):
        qs = obj.status_set.all()
        return StatusInlineUserSerializer(qs, many=True).data


class UserStatusSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    status_list = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'uri',
            'username',
            'status_list',
        ]
    def get_uri(self, obj):
        return '/api/users/{username}'.format(username=obj.username)

    def get_status_list(self, obj):
        qs = obj.status_set.all()
        return StatusInlineUserSerializer(qs, many=True).data