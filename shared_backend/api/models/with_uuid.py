from uuid import uuid4

from django.db import models


class WithUUID(models.Model):
    id = models.UUIDField("id", default=uuid4, primary_key=True)

    objects = models.Manager["WithUUID"]()

    class Meta:
        abstract = True
