# Generated by Django 2.0.1 on 2018-01-05 19:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20180105_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2072, 11, 22, 0, 0)),
        ),
    ]
