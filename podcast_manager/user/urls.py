from django.urls import path
from .views import RegisterUserView, LoginUserView, UserAPIView, LogoutUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('user/', UserAPIView.as_view(), name='user')
]