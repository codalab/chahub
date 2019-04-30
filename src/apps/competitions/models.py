import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone


class Competition(models.Model):
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.TextField(null=True, blank=True)
    creator_id = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='organized_competitions') # Added so we can tie back to Chahub Users
    created_when = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(null=True, blank=True)
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    prize = models.PositiveIntegerField(null=True, blank=True)
    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True)
    remote_id = models.CharField(max_length=128, null=True, blank=True)
    logo_url = models.URLField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    url = models.URLField()
    admins = models.ManyToManyField('CompetitionParticipant', related_name='admins', blank=True)
    participant_count = models.IntegerField(default=0)
    html_text = models.TextField(default="", null=True, blank=True)
    current_phase_deadline = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    class Meta:
        unique_together = ('remote_id', 'producer')

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if self.logo_url and not self.logo:
            from competitions.utils import competition_download_image
            competition_download_image(self.pk)
        super().save(**kwargs)

    # def save(self, *args, **kwargs):
    #     # Send off our data
    #     from api.serializers.competitions import CompetitionSerializer
    #     Group("updates").send({
    #         "text": json.dumps({
    #             "type": "competition_update",
    #             "data": CompetitionSerializer(self).data
    #         }),
    #     })
    #     return super().save(*args, **kwargs)

    def get_current_phase_deadline(self):
        # TODO: We may need to have a celery task that updates ElasticSearch deadlines.
        # We can't do sorting by deadline when we get a bunch of competitions.
        # Could save this as a property on the model
        for phase in self.phases.all():
            if phase.is_active and not phase.never_ends:
                if phase.start and phase.end:
                    if phase.end.year >= datetime.date.today().year:
                        return phase.end.isoformat()
        return None

    def get_is_active(self):
        # TODO: Check submission count from last 30 days
        if self.end is None:
            return True
        elif type(self.end) is datetime.datetime.date:
            return True if self.end is None else self.end > timezone.now().date()
        elif type(self.end) is datetime.datetime:
            return True if self.end is None else self.end > timezone.now()
        else:
            return False

    def get_current_phase(self, *args, **kwargs):
        for phase in self.phases.all().order_by('start'):
            if phase.is_active or phase.never_ends:
                return phase


class Phase(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='phases')
    index = models.PositiveIntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    never_ends = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.competition.title} - {self.name}"

    @property
    def is_active(self):
        """ Returns true when this phase of the competition is on-going. """
        if self.never_ends:
            if self.start and self.end:
                return self.start < timezone.now() < self.end
            else:
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
    remote_id = models.PositiveIntegerField()
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField()
    participant = models.TextField()


class CompetitionParticipant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='participants',
                             on_delete=models.SET_NULL)
    competition = models.ForeignKey(Competition, related_name='participants', on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.user.username)

    def __str__(self):
        return str(self.user.username)
