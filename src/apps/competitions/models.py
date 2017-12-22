from django.conf import settings
from django.db import models


class Competition(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_when = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)

    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True)
    remote_id = models.PositiveIntegerField()

    class Meta:
        unique_together = ('remote_id', 'producer')


class Phase(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='phases')


class Submission(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='submissions')
