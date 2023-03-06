from django.contrib.auth.models import User
from django.db import models


class BlogPost(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    subtitle = models.CharField(max_length=255, blank=True, default='')
    body = models.TextField()
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
