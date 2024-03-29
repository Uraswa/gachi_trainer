from django.db import models


class WordStorage(models.Model):
    storageName = models.CharField(max_length=256)

    initialData = models.TextField(max_length=99999999, null=True, default="", blank=True)
    ignore2ndStage = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.storageName}"


class Word(models.Model):
    storage = models.ForeignKey(to=WordStorage, on_delete=models.CASCADE, related_name="words")
    word = models.TextField(max_length=9999999)

    errors = models.IntegerField(default=0)
    totalRepeatedTimes = models.IntegerField(default=0)
    repeatIndex = models.IntegerField(default=0)
    repeatDate = models.DateField(null=True)

    def __str__(self):
        return f"{self.word}"
