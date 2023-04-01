from django.db import models


class WordStorage(models.Model):
    storageName = models.CharField(max_length=256)

    initialData = models.TextField(max_length=99999999, null=True)


class Word(models.Model):
    storage = models.ForeignKey(to=WordStorage, on_delete=models.CASCADE, related_name="words")
    word = models.TextField(max_length=9999999)

    errors = models.IntegerField(default=0)
    totalRepeatedTimes = models.IntegerField(default=0)
    repeatIndex = models.IntegerField(default=0)
    repeatDate = models.DateField(null=True)
