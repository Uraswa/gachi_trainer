# Generated by Django 3.2.18 on 2023-05-08 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordstorage',
            name='ignore2ndStage',
            field=models.BooleanField(default=False),
        ),
    ]
