import uuid

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Data(models.Model):
    created_by = models.TextField(null=True, blank=True)
    creator_id = models.IntegerField(null=True, blank=True)
    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets')
    remote_id = models.IntegerField(null=True)
    created_when = models.DateTimeField(default=now)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64, default="")
    description = models.TextField(null=True, blank=True)
    key = models.UUIDField(default=uuid.uuid4)
    download_url = models.URLField(null=True, blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} dataset on {self.producer}"


class DataGroup(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_when = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    datas = models.ManyToManyField(Data, related_name="groups")
