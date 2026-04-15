from abc import ABC, ABCMeta, abstractmethod
from django.db import models
from django.db.models.base import ModelBase


class Meta(ModelBase, ABCMeta):
    pass


class ReadyToRedis(ABC):
    @abstractmethod
    def redis_payload(self) -> dict:
        """Method to convert the model instance into a dictionary format suitable for Redis messages."""

        pass


class Language(models.Model, ReadyToRedis, metaclass=Meta):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"({self.code}) {self.name}"

    def redis_payload(self):
        return {
            "code": self.code,
            "name": self.name,
        }


class Guild(models.Model, ReadyToRedis, metaclass=Meta):
    id = models.BigIntegerField(primary_key=True)
    lang = models.ForeignKey(Language, on_delete=models.CASCADE, default="en")

    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"Guild {self.id}"

    def redis_payload(self):
        return {
            "id": str(self.id),
            "lang": self.lang.code,
        }
