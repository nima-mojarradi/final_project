from django.contrib import admin
from .models import RSSLink, Comment, PodcastData, LikeEpisode, LikePodcast, EpisodeData, Recommendation, Subscription, BookMark, Notification

admin.site.register(RSSLink)
admin.site.register(LikePodcast)
admin.site.register(LikeEpisode)
admin.site.register(PodcastData)
admin.site.register(EpisodeData)
admin.site.register(Comment)
admin.site.register(Recommendation)
admin.site.register(Subscription)
admin.site.register(BookMark)
admin.site.register(Notification)



