from django.contrib import admin
from .models import RSSLink, Comment, PodcastData, LikeEpisode, LikePodcast, EpisodeData

admin.site.register(RSSLink)
admin.site.register(LikePodcast)
admin.site.register(LikeEpisode)
admin.site.register(PodcastData)
admin.site.register(EpisodeData)
admin.site.register(Comment)
