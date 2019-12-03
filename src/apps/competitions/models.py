import datetime
from django.db import models
from django.utils import timezone
from django.utils.timezone import now


class Competition(models.Model):
    created_by = models.TextField(null=True, blank=True)
    creator_id = models.IntegerField(null=True, blank=True)
    created_when = models.DateTimeField(default=now)
    start = models.DateTimeField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    prize = models.PositiveIntegerField(null=True, blank=True)
    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True, related_name='competitions')
    remote_id = models.CharField(max_length=128, null=True, blank=True)
    logo_url = models.URLField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    admins = models.ManyToManyField('CompetitionParticipant', related_name='admins', blank=True)
    html_text = models.TextField(default="", null=True, blank=True)
    current_phase_deadline = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('remote_id', 'producer')

    def __str__(self):
        return self.title or f'{getattr(self.producer, "name", "N/A")} competition {self.remote_id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.logo_url and not self.logo:
            from competitions.tasks import download_competition_image
            download_competition_image.apply_async((self.id,))

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
    remote_id = models.IntegerField(null=True, blank=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='phases')
    index = models.PositiveIntegerField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    never_ends = models.BooleanField(default=False)
    status = models.CharField(max_length=128, null=True, blank=True)
    tasks = models.ManyToManyField('tasks.Task', blank=True, related_name="phases")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.competition.title} - {self.name}"

    @property
    def is_active(self):
        """ Returns true when this phase of the competition is on-going. """
        return self.status == "Current"


class Submission(models.Model):
    remote_id = models.PositiveIntegerField()
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    participant = models.TextField(null=True, blank=True)
    data = models.ForeignKey('datasets.Data', on_delete=models.CASCADE, related_name='submissions', null=True, blank=True)
    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions')
    deleted = models.BooleanField(default=False, blank=True)


class CompetitionParticipant(models.Model):
    remote_id = models.CharField(max_length=128, null=True, blank=True)
    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True, related_name='competition_participants')
    user = models.IntegerField(null=True, blank=True)
    competition = models.ForeignKey(Competition, related_name='participants', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'CompetitionParticipant - user remote_id: {self.user} for comp: {self.competition.title}'
