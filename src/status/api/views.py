import json
from rest_framework import generics, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404

from accounts.api.permissions import IsOwnerOrReadOnly

from status.models import Status
from .serializers import StatusSerializer

def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid

class StatusAPIView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    generics.ListAPIView
    ):
    """
    One Endpoint to rule them all. Refactoring is necessary.
    """
    permission_classes                  = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class                    = StatusSerializer
    search_fields                       = ('user__username', 'content')
    passed_id                           = None    

    
    # def get_queryset(self):        
    #     qs = Status.objects.all()
    #     query = self.request.GET.get('q')               
    #     if query is not None:
    #         qs = qs.filter(content__icontains=query)
    #     return qs    

    def get_object(self):
        request         = self.request
        passed_id       = request.GET.get('id', None) or self.passed_id
        queryset        = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None

    def get(self, request, *args, **kwargs):        
        url_id       = request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_json(body_):
            json_data = json.loads(request.body)
        request_body_id = json_data.get('id', None)              
        self.passed_id = url_id or request_body_id or None        
        if self.passed_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        url_id       = request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_json(body_):
            json_data = json.loads(request.body)
        request_body_id = json_data.get('id', None)              
        self.passed_id = url_id or request_body_id or None 
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        url_id    = request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_json(body_):
            json_data = json.loads(request.body)
        request_body_id = json_data.get('id', None)              
        self.passed_id = url_id or request_body_id or None 
        return self.update(request, *args)

    def delete(self, request, *args, **kwargs):
        url_id    = request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_json(body_):
            json_data = json.loads(request.body)
        request_body_id = json_data.get('id', None)              
        self.passed_id = url_id or request_body_id or None 
        return self.destroy(request, *args, *kwargs)

class StatusCreateAPIView(generics.CreateAPIView):
    """
    Lets leave this here for reference but this has been taken care
    of by the above view by adding the create model view mixin
    """
    permission_classes                  = []
    authentication_classes              = []
    queryset                            = Status.objects.all()
    serializer_class                    = StatusSerializer
    
class StatusDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    permission_classes                  = []
    authentication_classes              = []
    queryset                            = Status.objects.all()
    serializer_class                    = StatusSerializer 

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)    

class StatusUpdateAPIView(generics.UpdateAPIView):
    """
    Lets leave this here for reference but this has been taken care
    of by the above view by adding the update mixin view mixin
    """
    permission_classes                  = []
    authentication_classes              = []
    queryset                            = Status.objects.all()
    serializer_class                    = StatusSerializer   
    
class StatusDeleteAPIView(generics.DestroyAPIView):
    """
    Lets leave this here for reference but this has been taken care
    of by the above view by adding the delete mixin view mixin
    """
    permission_classes                  = []
    authentication_classes              = []
    queryset                            = Status.objects.all()
    serializer_class                    = StatusSerializer