from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"({self.code}) {self.name}"


class Guild(models.Model):
    id = models.BigIntegerField(primary_key=True)
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, default="en")

    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"Guild {self.id}"
