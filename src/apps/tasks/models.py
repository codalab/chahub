import uuid

from django.conf import settings
from django.db import models

from settings.base import BundleStorage
from utils.data import PathWrapper


class Task(models.Model):
    creator_id = models.IntegerField()
    remote_id = models.IntegerField()

    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)

    # TODO: We might have to convert this to a char to handle it nicely, or set the value on serializer _create or something?
    # This will be how we access download URLS
    key = models.UUIDField(default=uuid.uuid4, blank=True, unique=True)

    # We can keep this, and allow null/blank. If the user has a chahub_id attached to their profile
    # (Or some such field when connecting), and have that sent across so we can associate this dataset back here with their user.
    # We will probably need to send their Chahub OAuth access token or some such to verify this for security reasons.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    created_by = models.TextField(null=True, blank=True)

    created_when = models.DateTimeField(default=None, blank=True, null=True)
    uploaded_when = models.DateTimeField(auto_now_add=True)

    is_public = models.BooleanField(default=False)

    # TODO: This may be redundant. (IDEALLY It is as the foreign key on dataset should hold the remote id.)

    # remote_ingestion_program = models.IntegerField()
    ingestion_program = models.ForeignKey('datasets.Data', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_ingestion_programs")

    # remote_input_data = models.IntegerField()
    input_data = models.ForeignKey('datasets.Data', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_input_datas")

    ingestion_only_during_scoring = models.BooleanField(default=False)

    # remote_reference_data = models.IntegerField()
    reference_data = models.ForeignKey('datasets.Data', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_reference_datas")

    # remote_scoring_program = models.IntegerField()
    scoring_program = models.ForeignKey('datasets.Data', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_scoring_programs")

    class Meta:
        unique_together = ['producer', 'remote_id']

    def __str__(self):
        return f"Task - {self.name} - ({self.id})"


class Solution(models.Model):
    creator_id = models.IntegerField()
    remote_id = models.IntegerField()

    # We can keep this, and allow null/blank. If the user has a chahub_id attached to their profile
    # (Or some such field when connecting), and have that sent across so we can associate this dataset back here with their user.
    # We will probably need to send their Chahub OAuth access token or some such to verify this for security reasons.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_solutions')
    created_by = models.TextField(null=True, blank=True)

    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True)

    # TODO: We might have to convert this to a char to handle it nicely, or set the value on serializer _create or something?
    key = models.UUIDField(default=uuid.uuid4, blank=True, unique=True)

    uploaded_when = models.DateTimeField(auto_now_add=True)

    # TODO: Same as above for redundant fields. We could probably store an Array of Remote Integers, but we
    # should figure out somethiing better.
    # tasks = models.ManyToManyField(Task, related_name="solutions")
    tasks = models.ManyToManyField(Task, related_name="solutions")

    data = models.ForeignKey('datasets.Data', null=True, blank=True, on_delete=models.SET_NULL)

    is_public = models.BooleanField(default=False)

    class Meta:
        unique_together = ['producer', 'remote_id']

    def __str__(self):
        return f"Solution - {self.data.name} - ({self.id})"

