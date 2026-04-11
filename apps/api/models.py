from django.db import models


class Guild(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    lang = models.CharField(
        max_length=2,
        default="en",
        choices=[
            ("en", "(EN) English"),
            ("es", "(ES) Spanish"),
        ],
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return self.name
