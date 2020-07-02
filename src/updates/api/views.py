import json
from django.views.generic import View
from django.http import HttpResponse

from updates.forms import UpdateModelForm
from updates.models import Update as UpdateModel

from src.mixins import CSRFExemptMixin

from .utilities import is_json

class UpdateModelDetailAPIView(CSRFExemptMixin, View):

    def get_object(self, id=None):        
        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None        

    def get(self, request, id, *args, **kwargs):
        obj = self.get_object(id)
        if obj is None:
            data = json.dumps({"message": "update does not exist"})
            return HttpResponse(data, content_type='application/json', status=404)
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json', status=200)

    def post(self, request, *args, **kwargs):
        data = json.dumps({"message": "Not allowed. Use the endpoint api/details/ to create an update"})
        return HttpResponse(data, content_type='application/json', status=401)

    def put(self, request, id, *args, **kwargs):
        valid_json = request.body
        if not is_json(valid_json):
            error_message = json.dumps({"message": "not valid json data"})
            return HttpResponse(error_message, content_type='application/json', status=400)
        
        obj = self.get_object(id)
        if obj is None:
            data = json.dumps({"message": "update does not exist"})
            return HttpResponse(data, content_type='application/json', status=404)
        
        original_data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)
        for key, value in passed_data.items():
            original_data[key] = value

        form = UpdateModelForm(original_data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            data = obj.serialize()            
            return HttpResponse(data, content_type='application/json', status=201)
        if form.errors:            
            error = json.dumps(form.errors)
            return HttpResponse(error, content_type='application/json', status=400)

        data = json.dumps({"message": "something went wrong"})     
        return HttpResponse(data, content_type='application/json', status=400)        
        

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id)
        if obj is None:
            data = json.dumps({"message": "update does not exist"})
            return HttpResponse(data, content_type='application/json', status=404)

        deleted = obj.delete()
        print(deleted)
        message = json.dumps({"message": "update deleted"})
        return HttpResponse(message, content_type='application/json')


class UpdateModelListView(CSRFExemptMixin, View): 
    def get(self, request, *args, **kwargs):
        qs = UpdateModel.objects.all()
        json_data = qs.serialize()
        return HttpResponse(json_data, content_type='application/json')

    def post(self, request, *args, **kwargs):
        valid_json = request.body
        if not is_json(valid_json):
            error_message = json.dumps({"message": "not valid json data"})
            return HttpResponse(error_message, content_type='application/json', status=400)
        
        form_data = json.loads(request.body)
        form = UpdateModelForm(form_data)
        if form.is_valid():
            obj = form.save(commit=True)
            data = obj.serialize()            
            return HttpResponse(data, content_type='application/json', status=201)
        if form.errors:            
            error = json.dumps(form.errors)
            return HttpResponse(error, content_type='application/json', status=400)

        data = json.dumps({"message": "something went wrong"})     
        return HttpResponse(data, content_type='application/json', status=400)
        