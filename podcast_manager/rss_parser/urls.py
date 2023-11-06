from django.urls import path
from .views import RequestUrl, LikeView, BookMarkView, WriteCommentView, SubscribeView, AllPodcasts, AllBookmarkedPodcasts, AllLikedPodcasts, AllCommentsOnEpisode, CountOfLikes, DeleteCommentView

urlpatterns = [
    path('', AllPodcasts.as_view(), name='all_podcasts'),
    path('request_url/', RequestUrl.as_view(), name='parser'),
    path('like/<int:episode_id>', LikeView.as_view(), name='like'),
    path('bookmark/<int:episode_id>', BookMarkView.as_view(), name='bookmark'),
    path('comment/<int:podcast_id>', WriteCommentView.as_view(), name='comment'),
    path('delete_comment/<int:comment_id>', DeleteCommentView.as_view(), name='delete_comment'),
    path('subscribe/<int:channel_id>', SubscribeView.as_view(), name='subscription'),
    path('all_liked/', AllLikedPodcasts.as_view(), name='liked_podcasts'),
    path('all_bookmarked/', AllBookmarkedPodcasts.as_view(), name='bookmarked_podcasts'),
    path('all_comments/<int:episode_id>', AllCommentsOnEpisode.as_view(), name='all_comments'),
    path('all_likes/<int:episode_id>', CountOfLikes.as_view(), name='all_likes'),

]