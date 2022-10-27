from django.contrib.auth.models import AbstractUser
from django.db import models

class UserManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }

    def natural_key(self):
        return (self.username)

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MyPosts")
    content = models.TextField( )
    posted = models.DateTimeField(auto_now_add=True)
    lastmodified = models.DateTimeField(auto_now=True)
    likecount = models.IntegerField(default=0)

    def serialize(self):
        return {
        "poster": self.poster.id,
        "content": self.content,
        "posted": self.posted,
        "lastmodified": self.lastmodified,
        "likecount": self.likecount
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MyLikes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    timestamp = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myfollowing")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myfollowers")
