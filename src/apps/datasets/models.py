import uuid

from django.conf import settings
from django.db import models


class Data(models.Model):
    creator_id = models.IntegerField()
    remote_id = models.IntegerField()

    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_datasets')
    created_by = models.TextField(null=True, blank=True)

    created_when = models.DateTimeField(default=None, blank=True, null=True)
    uploaded_when = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    key = models.UUIDField(default=uuid.uuid4, blank=True, unique=True)

    is_public = models.BooleanField(default=False)

    class Meta:
        unique_together = ['producer', 'remote_id']

    def __str__(self):
        return f"Dataset - {self.name} - ({self.id})"


# TODO: Figure out exactly how grouped/sub datasets are going to work?

class DataGroup(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_when = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    datas = models.ManyToManyField(Data, related_name="groups")
