# Generated by Django 3.2.18 on 2023-03-05 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('math_gachi_train', '0002_auto_20230305_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='banned',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
