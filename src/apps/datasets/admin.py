from django.contrib import admin

from utils.manager import DeletedAdmin
from . import models


admin.site.register(models.Data, DeletedAdmin)
admin.site.register(models.DataGroup)
