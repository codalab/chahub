import json

from channels import Group
from django.conf import settings
from django.db import models


class Competition(models.Model):
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.TextField()
    created_when = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True)
    remote_id = models.PositiveIntegerField()

    logo = models.URLField(null=True, blank=True)
    url = models.URLField()

    admins = models.ManyToManyField('CompetitionParticipant', related_name='admins')

    class Meta:
        unique_together = ('remote_id', 'producer')

    def save(self, *args, **kwargs):
        # Calculate our end-date
        # If more than one phase
        if len(self.phases.all()) > 1:
            # Order all by end date, grab the last and set our comp end date to that end date
            self.end = self.phases.all().order_by('end').last().end.date()
        # Else we only have on
        elif len(self.phases.all()) == 1:
            # Set our end date to our first phase
            self.end = self.phases.first().end.date()
            # Else?: Do nothing. we don't need to set the field for now.

        # Send off our data
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

    def __unicode__(self):
        return str(self.user.username)

    def __str__(self):
        return str(self.user.username)
