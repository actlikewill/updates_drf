from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import AuthView, RegisterAPIView

urlpatterns = [
    path('token/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('register/', RegisterAPIView.as_view()),     
    path('', AuthView.as_view())      
]
