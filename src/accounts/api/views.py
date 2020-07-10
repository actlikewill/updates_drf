from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.conf import settings

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import UserRegisterSerializer

User = get_user_model()



jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class RegisterAPIView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer    
    

class AuthView(APIView):
    authentication_classes = []    
    permission_classes      = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
       
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload) 
                response = jwt_response_payload_handler(token, user, request=request)       
                return Response(response)
        return Response({"detail": "Invalid Credentials."}, status=401)

class RegisterView(APIView):
    """This is better achieved by a serializer."""
    authentication_classes = []    
    permission_classes      = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        
        username = data.get('username') or None
        email = data.get('email') or None
        password = data.get('password') or None
        password2 = data.get('password2') or None

        print(username)
        print(email)
        print(password)
        print(password2)

        if username is None or email is None or password is None or password2 is None:
            return Response(
                            {"detail":"Some fields are missing. Fields required are username,"
                                 "email, password, and password2"}, status=401)

                            
        qs = User.objects.filter(
            Q(username__iexact=username) |
            Q(email__iexact=username)
        )
        if qs.exists():
            return Response({"detail": "This user already exists."}, status=401)
        elif password != password2:
            return Response({"detail": "Passwords do not match."})
        else: 
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload) 
            response = jwt_response_payload_handler(token, user, request=request)       
            return Response(response)        
        return Response({"detail": "Invalid Reqeuest."}, status=401)