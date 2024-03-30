from django.db import models
from django.contrib.auth.models import User


class AuthUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField(default='1')

# Create your models here.
