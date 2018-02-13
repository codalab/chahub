import json

from channels import Group
from django.conf import settings
from django.db import models


class Competition(models.Model):
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.TextField()
    created_when = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)

    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True)
    remote_id = models.PositiveIntegerField()

    logo = models.URLField(null=True, blank=True)
    url = models.URLField()

    class Meta:
        unique_together = ('remote_id', 'producer')

    def save(self, *args, **kwargs):
        from api.serializers.competitions import CompetitionSerializer
        Group("updates").send({
            "text": json.dumps({
                "type": "competition_update",
                "data": CompetitionSerializer(self).data
            }),
        })
        return super().save(*args, **kwargs)


class Phase(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='phases')
    index = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)


class Submission(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='submissions')


class CompetitionParticipant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='participants',
                             on_delete=models.SET_NULL)
    competition = models.ForeignKey(Competition, related_name='participants', on_delete=models.CASCADE)
