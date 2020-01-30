from django.contrib import admin

from utils.manager import DeletedAdmin
from . import models

admin.site.register(models.Competition, DeletedAdmin)
admin.site.register(models.Phase, DeletedAdmin)
admin.site.register(models.CompetitionParticipant, DeletedAdmin)
admin.site.register(models.Submission, DeletedAdmin)
