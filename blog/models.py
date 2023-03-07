from django.contrib.auth.models import User
from django.db import models
from treebeard.mp_tree import MP_Node


class BlogPost(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    subtitle = models.CharField(max_length=255, blank=True, default='')
    body = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='blogposts', on_delete=models.CASCADE)


# max default depth: 63
# (source: https://django-treebeard.readthedocs.io/en/latest/mp_tree.html#treebeard.mp_tree.MP_Node.path)
class BlogPostComment(MP_Node):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    blogpost = models.ForeignKey('BlogPost', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
