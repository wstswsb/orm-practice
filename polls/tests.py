from django.test import TestCase
from django.db import models

# Create your tests here.
from polls.models.user import User
from polls.models.poll import Poll
from polls.models.question import Question
from polls.models.answer import Answer
from polls.models.user_answer import UserAnswer


class ORMPracticeTests(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(nickname="test-user-1")
        self.user2 = User.objects.create(nickname="test-user-2")

        self.poll1 = Poll.objects.create(author=self.user1, title="test-poll-1")
        self.poll2 = Poll.objects.create(author=self.user2, title="test-poll-2")

        self.question1_for_poll1 = Question.objects.create(
            poll=self.poll1,
            text="test-question-1-text",
            question_type="single_choice",
        )
        self.question2_for_poll1 = Question.objects.create(
            poll=self.poll1,
            text="test-question-2-text",
            question_type="multiple_choice",
        )
        self.question1_for_poll2 = Question.objects.create(
            poll=self.poll2,
            text="test-question-3-text",
            question_type="single_choice",
        )
        self.question2_for_poll2 = Question.objects.create(
            poll=self.poll2,
            text="test-question-4-text",
            question_type="multiple_choice",
        )

        self.answer1_for_question1_for_poll1 = Answer.objects.create(
            question=self.question1_for_poll1,
            text="test-answer-1-text"
        )
        self.answer2_for_question1_for_poll1 = Answer.objects.create(
            question=self.question1_for_poll1,
            text="test-answer-2-text"
        )
        self.answer1_for_question2_for_poll1 = Answer.objects.create(
            question=self.question2_for_poll1,
            text="test-answer-1-text"
        )
        self.answer2_for_question2_for_poll1 = Answer.objects.create(
            question=self.question2_for_poll1,
            text="test-answer-2-text"
        )

        self.answer1_for_question1_for_poll2 = Answer.objects.create(
            question=self.question1_for_poll2,
            text="test-answer-1-text"
        )
        self.answer2_for_question1_for_poll2 = Answer.objects.create(
            question=self.question1_for_poll2,
            text="test-answer-2-text"
        )

        self.answer1_fow_question2_for_poll2 = Answer.objects.create(
            question=self.question2_for_poll2,
            text="test-answer-1-text"
        )
        self.answer_2_for_question2_for_poll2 = Answer.objects.create(
            question=self.question2_for_poll2,
            text="test-answer-2-text"
        )

        # user1 answers for poll 1 only
        self.user_answer_for_user1_for_question1_for_poll1 = UserAnswer.objects.create(
            user=self.user1,
            answer=self.answer1_for_question1_for_poll1
        )
        self.user_answer_for_user1_for_question2_for_poll1 = UserAnswer.objects.create(
            user=self.user1,
            answer=self.answer2_for_question2_for_poll1
        )

        # user2 answers for poll 1-2
        self.user_answer1_for_user2_for_question1_for_poll1 = UserAnswer.objects.create(
            user=self.user2,
            answer=self.answer2_for_question1_for_poll1,
        )
        self.user_answer1_for_user2_for_question2_for_poll1 = UserAnswer.objects.create(
            user=self.user2,
            answer=self.answer2_for_question2_for_poll1,
        )
        # for most popular poll1
        self.user_answer2_for_user2_for_question1_for_poll1 = UserAnswer.objects.create(
            user=self.user2,
            answer=self.answer2_for_question1_for_poll1,
        )
        self.user_answer2_for_user2_for_question2_for_poll1 = UserAnswer.objects.create(
            user=self.user2,
            answer=self.answer2_for_question2_for_poll1,
        )

        self.user_answer_for_user2_for_question1_for_poll2 = UserAnswer.objects.create(
            user=self.user2,
            answer=self.answer1_for_question1_for_poll2
        )
        self.user_answer_for_user2_for_question2_for_poll2 = UserAnswer.objects.create(
            user=self.user2,
            answer=self.answer1_fow_question2_for_poll2
        )
        self.user_answer_for_user2_for_question2_for_poll2_multiple = \
            UserAnswer.objects.create(
                user=self.user2,
                answer=self.answer_2_for_question2_for_poll2
            )

    def test_user1_polls(self):
        """Получить все опросы, которые проходил пользователь с заданным id"""
        user1_polls = Poll.objects.filter(
            questions__answers__users_answers__user_id=self.user1.pk
        ).distinct()

        self.assertEqual([self.poll1], list(user1_polls))

    def test_user2_pools(self):
        """Получить все опросы, которые проходил пользователь с заданным id"""
        user2_polls = Poll.objects.filter(
            questions__answers__users_answers__user_id=self.user2.pk
        ).distinct()

        self.assertEqual([self.poll1, self.poll2], list(user2_polls))

    def test_most_popular_polls(self):
        num_polls = 1
        most_popular_poll = (
            Poll.objects
            .annotate(num_responses=models.Count("questions__answers__users_answers"))
            .order_by('-num_responses')
            [:num_polls]
        )

        self.assertEqual([self.poll1], list(most_popular_poll))

    def test_most_unpopular_polls(self):
        num_polls = 1
        most_popular_poll = (
            Poll.objects
            .annotate(num_responses=models.Count("questions__answers__users_answers"))
            .order_by('num_responses')
            [:num_polls]
        )

        self.assertEqual([self.poll2], list(most_popular_poll))

    def test_user1_answers_for_poll1(self):
        user1_answers = (
            UserAnswer.objects
            .filter(
                user_id=self.user1.pk,
                answer__question__poll_id=self.poll1.pk
            )
        )

        self.assertEqual(
            [
                self.user_answer_for_user1_for_question1_for_poll1,
                self.user_answer_for_user1_for_question2_for_poll1,
            ],
            list(user1_answers)
        )

    def test_user2_answers_for_poll1(self):
        user2_answers = (
            UserAnswer.objects
            .filter(
                user_id=self.user2.pk,
                answer__question__poll_id=self.poll1.pk
            )
        )

        self.assertEqual(
            [
                self.user_answer1_for_user2_for_question1_for_poll1,
                self.user_answer1_for_user2_for_question2_for_poll1,
                self.user_answer2_for_user2_for_question1_for_poll1,
                self.user_answer2_for_user2_for_question2_for_poll1,
            ],
            list(user2_answers)
        )