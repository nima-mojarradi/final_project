from django.db import models
from user.models import CustomUser

class RSSLink(models.Model):
    url = models.URLField(unique=True)

    def __str__(self) -> str:
        return self.url


class PodcastData(models.Model):
    link = models.URLField(null=True,blank=True, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    itunes_author = models.CharField(max_length=100, default='Unknown', null=True, blank=True)
    itunes_duration = models.CharField(max_length=100, null=True, blank=True)
    rss_link=models.OneToOneField(RSSLink, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class EpisodeData(models.Model):
    link = models.URLField(null=True,blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    itunes_author = models.CharField(max_length=100, default='Unknown', null=True, blank=True)
    itunes_duration = models.CharField(max_length=100, null=True, blank=True)
    images=models.TextField(default='image url')
    podcast=models.ForeignKey(PodcastData, on_delete=models.CASCADE)
    guid = models.CharField(max_length=100, unique=True)

    # def __str__(self) -> str:
    #     return self.title


class LikeEpisode(models.Model):
    user1 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='user')
    title = models.ForeignKey(EpisodeData, on_delete=models.CASCADE)

class LikePodcast(models.Model):
    user2 = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.ForeignKey(PodcastData, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    context = models.TextField()
    podcast = models.ForeignKey(EpisodeData, on_delete=models.CASCADE)
    
