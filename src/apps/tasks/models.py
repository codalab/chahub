import uuid

from django.db import models
from django.utils.timezone import now

from utils.manager import ChaHubModelManager


class Task(models.Model):
    remote_id = models.IntegerField()
    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    created_by = models.TextField(null=True, blank=True)
    creator_id = models.IntegerField(null=True, blank=True)
    created_when = models.DateTimeField(default=now, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    key = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    is_public = models.BooleanField(default=False)

    ingestion_program = models.ForeignKey('datasets.Data', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_ingestion_programs")
    input_data = models.ForeignKey('datasets.Data', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_input_datas")
    ingestion_only_during_scoring = models.NullBooleanField(default=False)

    reference_data = models.ForeignKey('datasets.Data', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_reference_datas")
    scoring_program = models.ForeignKey('datasets.Data', on_delete=models.SET_NULL, null=True, blank=True, related_name="task_scoring_programs")

    deleted = models.BooleanField(default=False)

    objects = ChaHubModelManager()

    def __str__(self):
        return f"Task - {self.name} - ({self.id})"


class Solution(models.Model):
    remote_id = models.IntegerField()
    producer = models.ForeignKey('producers.Producer', on_delete=models.SET_NULL, null=True, blank=True, related_name='solutions')
    name = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    key = models.UUIDField(default=uuid.uuid4, blank=True, null=True)
    tasks = models.ManyToManyField(Task, related_name="solutions", blank=True)
    data = models.ForeignKey('datasets.Data', null=True, blank=True, on_delete=models.CASCADE, related_name='solutions')
    deleted = models.BooleanField(default=False)

    objects = ChaHubModelManager()

    def __str__(self):
        return f"Solution - ({self.id})"
