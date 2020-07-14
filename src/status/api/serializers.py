from rest_framework import serializers
from accounts.api.serializers import UserPublicSerializer
from status.models import Status

'''
Serializer turns data into JSON and also Validate the data.
'''

class StatusInlineUserSerializer(serializers.ModelSerializer):
    uri         = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Status
        fields = [
            'id',
            'content',
            'image',
            'uri'
        ]

    def get_uri(self, obj):
        return '/api/status/?id={id}'.format(id=obj.id)
 



class StatusSerializer(serializers.ModelSerializer):
    uri         = serializers.SerializerMethodField(read_only=True)
    user        = UserPublicSerializer(read_only=True)
    class Meta:
        model = Status
        fields = [
            'id',
            'content',
            'image',
            'user',
            'uri'
        ]
        read_only_fields = ['user']

    def get_uri(self, obj):
        return '/api/status/?id={id}'.format(id=obj.id)

        
    def validate_content(self, value):
        if len(value) > 10000:
            raise serializers.ValidationError("Content too long.")
        return value

    def validate(self, data):
        content = data.get("content", None)
        if content == "":
            content = None
        image = data.get("image", None)
        if content is None and image is None:
            raise serializers.ValidationError("Content or image is required.")
        return data