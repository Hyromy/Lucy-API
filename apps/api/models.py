from django.db import models

class Guild(models.Model):
    id = models.BigIntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    lang = models.CharField(
        max_length = 2,
        default = "en",
        choices = [
            ("en", "English"),
            ("es", "Spanish"),
        ]
    )
    joined_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
