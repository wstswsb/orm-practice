import uuid

from django.db import models
from typing import NamedTuple, Literal

from polls.models.poll import Poll


class QuestionType(NamedTuple):
    value: Literal["single_choice", "multiple_choice"]
    human_readable_view: str


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(blank=False, null=False)
    question_type = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=[
            QuestionType(
                value="single_choice",
                human_readable_view="Single Choice",
            ),
            QuestionType(
                value="multiple_choice",
                human_readable_view="Multiple Choice",
            )
        ]
    )
