import uuid

from django.db import models
from polls.models.user import User


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="polls_authored",
    )
    title = models.CharField(max_length=255, blank=False, null=False)
