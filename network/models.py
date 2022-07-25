from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User,blank=True, related_name='following')

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
