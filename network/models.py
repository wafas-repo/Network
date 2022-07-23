from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)

class Post(models.Model):
   username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   content = models.TextField()
   dt_posted = models.DateTimeField(auto_now_add=True, null=True)
   likes = models.ManyToManyField(User, related_name='like_post')

   def total_likes(self):
       return self.likes.count()
   
   def serialize(self):
       return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "timestamp": self.dt_posted.strftime("%b %-d %Y, %-I:%M %p"),
        }

