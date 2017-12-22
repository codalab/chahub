from django.db import models


class Producer(models.Model):
    api_key = models.UUIDField()
    name = models.TextField()
    contact = models.EmailField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return "{} @ {}".format(self.name, self.url)
