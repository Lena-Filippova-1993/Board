from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthUser(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # code = models.CharField(max_length=25, blank=True, null=True)
    pass
# Create your models here.
# class User(AbstractUser):
#     code = models.CharField(max_length=25, blank=True, null=True)