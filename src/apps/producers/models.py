import uuid

from django.db import models


class Producer(models.Model):
    api_key = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.TextField()
    contact = models.EmailField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return "{} @ {}".format(self.name, self.url)

    @property
    def competition_count(self):
        return self.competitions.exclude(deleted=True).count()

    @property
    def dataset_count(self):
        return self.datasets.exclude(type='submission').exclude(deleted=True).count()

    @property
    def participant_count(self):
        return self.competition_participants.count()

    @property
    def submission_count(self):
        return self.submissions.exclude(deleted=True).count()

    @property
    def user_count(self):
        return self.profiles.count()

    @property
    def organizer_count(self):
        return 0
