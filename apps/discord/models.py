from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    id = models.BigIntegerField(primary_key=True)

    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"
