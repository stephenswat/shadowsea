import datetime
import random

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


def get_next_post_datetime():
    return Post.objects.all().aggregate(Max('created'))['created__max'] + datetime.timedelta(seconds=random.randint(10, 1500))


class Post(models.Model):
    thread = models.ForeignKey(Thread, models.CASCADE, db_index=True)
    poster = models.ForeignKey(User, models.CASCADE)
    content = models.CharField(max_length=1024)
    created = models.DateTimeField(default=get_next_post_datetime)
    created_real = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "<Post in \"%s\">" % str(self.thread)


class ThreadRead(models.Model):
    thread = models.ForeignKey(Thread, models.CASCADE, db_index=True)
    user = models.ForeignKey(User, models.CASCADE, db_index=True)
    date = models.DateTimeField(auto_now=True)