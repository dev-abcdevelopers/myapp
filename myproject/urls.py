from django.contrib import admin
from django.urls import path
from myapp.views import CreatePublicUserView, CreateUserAPIView, GetPublicUserView, GetUserAPIView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_user/', CreateUserAPIView.as_view(), name='create_user'),
    path('api_key_info/', GetUserAPIView.as_view(), name='api_key_info'),
    path('create_public_user/', CreatePublicUserView.as_view(), name='create_public_user'),
    path('get_public_user/', GetPublicUserView.as_view(), name='get_public_user'),
]
