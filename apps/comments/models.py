from django.db import models
from django.conf import settings
from apps.posts.models import Post


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.author) + ': "' + str(self.content) + '"'

