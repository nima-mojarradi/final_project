from django.urls import path
from .views import RequestUrl, LikeView, BookMarkView

urlpatterns = [
    path('request_url/', RequestUrl.as_view(), name='parser'),
    path('like/', LikeView.as_view(), name='like'),
    path('bookmark/', BookMarkView.as_view(), name='bookmark'),
]