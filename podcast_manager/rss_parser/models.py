from django.db import models
from user.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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
    category=models.CharField(max_length=100)

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

    def __str__(self) -> str:
        return str(self.title)


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

    def __str__(self) -> str:
        return f'{self.user}: {self.context}'
    


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    channel = models.ForeignKey(PodcastData, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'channel']]

    def __str__(self):
        return f'{self.channel} subscribed by {self.user}'
    


class BookMark(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookmarks')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    episode = models.ForeignKey(EpisodeData, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} bookmarked {self.content_object}'
    

class Recommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='category_recommendations')
    category = models.ForeignKey(PodcastData, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} interest in: {self.category.name}'

    class Meta:
        ordering = ['-count']



class Notification(models.Model):
    title = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=50)
    recipients = models.ManyToManyField(CustomUser, blank=True, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_read = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification: {self.title}'