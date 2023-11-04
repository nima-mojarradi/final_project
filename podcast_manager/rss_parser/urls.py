from django.urls import path
from .views import RequestUrl, LikeView, BookMarkView, CommentView, SubscribeView

urlpatterns = [
    path('request_url/', RequestUrl.as_view(), name='parser'),
    path('like/<int:episode_id>', LikeView.as_view(), name='like'),
    path('bookmark/<int:episode_id>', BookMarkView.as_view(), name='bookmark'),
    path('comment/<int:podcast_id>', CommentView.as_view(), name='comment'),
    path('subscribe/<int:channel_id>', SubscribeView.as_view(), name='subscription'),
]