from django.urls import path
from .views import RequestUrl

urlpatterns = [
    path('request_url/', RequestUrl.as_view(), name='parser'),
]