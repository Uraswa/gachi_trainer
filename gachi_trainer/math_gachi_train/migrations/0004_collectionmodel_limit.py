# Generated by Django 3.2.18 on 2023-03-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('math_gachi_train', '0003_taskmodel_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionmodel',
            name='limit',
            field=models.IntegerField(default=9999),
        ),
    ]
