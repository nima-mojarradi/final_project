from django.urls import path
from .parser import ParseRssFeed
from .views import LikedPodcasts

urlpatterns = [
    path('parser/', ParseRssFeed, name='parser'),
    path('likes/', LikedPodcasts.as_view(), name='likes'),
]