from django.contrib import admin
from django.db import models


class ChaHubModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def all_objects(self):
        return super().get_queryset()


class DeletedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """Overriding to show deleted objects"""
        qs = self.model.objects.all_objects()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
