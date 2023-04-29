from django.db import models
from datetime import datetime
# Create your models here.

class Pronounce(models.Model):
    word = models.CharField(max_length=256)
    repeatsCount = models.IntegerField(default=0)
    errorsCount = models.IntegerField(default=0)
    repeatDate = models.DateField(default=datetime.now)

    def __str__(self):
        return self.word
