from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize 
from django.shortcuts import render
from django.views.generic import View
from src.mixins import JsonResponseMixin

from .models import Update

def update_model_detail_view(request):
    data = {
        "data": 2111,
        "message": "detail view"
    }
    return JsonResponse(data)

class JsonCBV(View):
    def get(self, request, *args, **kwargs):
        data = {
        "data": 2111,
        "message": "class based view"
        }
        return JsonResponse(data)


class SerializedDetailView(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = Update.objects.get(id=1).serialize()       
        return HttpResponse(data, content_type='application/json')

class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        data = Update.objects.all().serialize()
        return HttpResponse(data, content_type='application/json')
