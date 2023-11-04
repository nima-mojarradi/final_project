from django.urls import path
from .views import RequestUrl, LikeView, BookMarkView, Comment

urlpatterns = [
    path('request_url/', RequestUrl.as_view(), name='parser'),
    path('like/<int:episode_id>', LikeView.as_view(), name='like'),
    path('bookmark/', BookMarkView.as_view(), name='bookmark'),
    path('comment/', Comment(), name='bookmark'),
]