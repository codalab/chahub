from django.contrib import admin

from utils.manager import DeletedAdmin
from . import models

admin.site.register(models.Task, DeletedAdmin)
admin.site.register(models.Solution, DeletedAdmin)
