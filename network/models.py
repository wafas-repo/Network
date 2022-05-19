from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
   username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   content = models.TextField()
   dt_posted = models.DateTimeField(auto_now_add=True, null=True)
# add likes starting with 0 ?
