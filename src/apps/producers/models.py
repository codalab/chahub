import uuid

from django.db import models


class Producer(models.Model):
    api_key = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.TextField()
    contact = models.EmailField(null=True, blank=True)
    url = models.URLField()

    competition_count = models.IntegerField(default=0)
    dataset_count = models.IntegerField(default=0)
    participant_count = models.IntegerField(default=0)
    submission_count = models.IntegerField(default=0)
    user_count = models.IntegerField(default=0)
    organizer_count = models.IntegerField(default=0)

    def __str__(self):
        return "{} @ {}".format(self.name, self.url)
