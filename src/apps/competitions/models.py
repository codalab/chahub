import json

import datetime
from channels import Group
from django.conf import settings
from django.db import models
from django.utils import timezone


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
            if self.phases.all().order_by('end').last().end:
                self.end = self.phases.all().order_by('end').last().end.date()
        # Else we only have on
        elif len(self.phases.all()) == 1:
            # Set our end date to our first phase
            if self.phases.first().end:
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

    @property
    def is_active(self):
        if self.end is None:
            return True
        elif type(self.end) is datetime.datetime.date:
            return True if self.end is None else self.end > timezone.now().date()
        elif type(self.end) is datetime.datetime:
            return True if self.end is None else self.end > timezone.now()
        else:
            return False

    def get_active_phase_end(self):
        for phase in self.phases.all():
            if phase.is_active:
                if phase.end:
                    return str(phase.end.date())
        return "None"

    def get_current_phase(self, *args, **kwargs):
        all_phases = self.phases.all().order_by('start')
        phase_iterator = iter(all_phases)
        active_phase = None
        for phase in phase_iterator:
            # Get an active phase that isn't also never-ending, unless we don't have any active_phases
            if phase.is_active:
                if active_phase is None:
                    active_phase = phase
                elif not phase.phase_never_ends:
                    active_phase = phase
                    break
        return active_phase


class Phase(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='phases')
    index = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    never_ends = models.BooleanField(default=False)

    @property
    def is_active(self):
        """ Returns true when this phase of the competition is on-going. """
        if self.never_ends:
            return True
        else:
            next_phase = self.competition.phases.filter(index=self.index + 1)
            if (next_phase is not None) and (len(next_phase) > 0):
                # there is a phase following this phase, thus this phase is active if the current date
                # is between the start of this phase and the start of the next phase
                return self.start <= timezone.now() and (timezone.now() < next_phase[0].start)
            else:
                # there is no phase following this phase, thus this phase is active if the current data
                # is after the start date of this phase and the competition is "active"
                return self.start <= timezone.now() and self.competition.is_active


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
