from django.contrib import admin
from . import models


admin.site.register(models.Competition)
admin.site.register(models.Phase)
admin.site.register(models.CompetitionParticipant)
admin.site.register(models.Submission)
