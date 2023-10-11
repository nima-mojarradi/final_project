from django.urls import path
from .views import RegisterUserView, LoginUserView, UserAPIView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/', UserAPIView.as_view(), name='user')
]