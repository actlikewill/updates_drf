from django.urls import include, path
from .views import (
    StatusAPIView,
    StatusCreateAPIView,
    StatusDetailAPIView,
    StatusUpdateAPIView,
    StatusDeleteAPIView,
)

urlpatterns = [
    path('', StatusAPIView.as_view()),
    # path('create/', StatusCreateAPIView.as_view()),
    # path('<int:pk>/', StatusDetailAPIView.as_view()),    
    # path('update/<int:pk>/', StatusUpdateAPIView.as_view()),    
    # path('delete/<int:pk>/', StatusDeleteAPIView.as_view()),    
]
 