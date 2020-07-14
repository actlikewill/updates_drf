from django.urls import path, re_path


from .views import UserDetailAPIView, UserStatusAPIView

urlpatterns = [
    re_path(r'^(?P<username>\w+)/$', UserDetailAPIView.as_view(), name='detail'),    
    re_path(r'^(?P<username>\w+)/status$', UserStatusAPIView.as_view(), name='status_list'),    
]

app_name = 'api-user'