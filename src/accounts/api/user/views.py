from django.contrib.auth import get_user_model
from rest_framework import generics, pagination
from .serializers import UserDetailSerializer
from status.api.serializers import StatusInlineUserSerializer, Status

User = get_user_model()


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = UserDetailSerializer   
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'username'

class UserStatusAPIView(generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = StatusInlineUserSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get('username', None)
        if username is None:
            return Status.objects.none()
        return Status.objects.filter(user__username=username)