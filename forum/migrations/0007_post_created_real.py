# Generated by Django 2.0.1 on 2018-01-07 14:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_threadread'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_real',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 1, 1, 0, 0)),
            preserve_default=False,
        ),
    ]
