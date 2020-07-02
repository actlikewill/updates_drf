
from django.urls import path
from .views import (
    UpdateModelDetailAPIView,
    UpdateModelListView
)

urlpatterns = [
        path('', UpdateModelListView.as_view()),
        path('<int:id>/', UpdateModelDetailAPIView.as_view()),
    ]