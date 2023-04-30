from django.db import models
from datetime import datetime
# Create your models here.


class Hint(models.Model):
    name = models.CharField(default="", max_length=256)
    text = models.TextField(default="")
    def __str__(self):
        return self.name


class Pronounce(models.Model):
    word = models.CharField(max_length=256)
    repeatsCount = models.IntegerField(default=0)
    errorsCount = models.IntegerField(default=0)
    repeatDate = models.DateField(default=datetime.now)

    hint = models.ForeignKey(to=Hint, on_delete=models.CASCADE, related_name="words", null=True, default=None)

    def __str__(self):
        return self.word

