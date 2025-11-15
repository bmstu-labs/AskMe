# management/commands/fill_db.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike, Profile
import random

class Command(BaseCommand):
    help = 'Fill DB with test data: python manage.py fill_db [ratio]'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, nargs='?', default=1)

    def handle(self, *args, **options):
        ratio = options['ratio']
        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        self.stdout.write('Filling DB...')

        users = []
        for i in range(0, num_users):
            users.append(User(username=f'user{i}', email=f'user{i}@example.com'))
        User.objects.bulk_create(users, batch_size=1000)

        users_qs = list(User.objects.all()[:num_users])

        tags = [Tag(name=f'tag{i}') for i in range(1, num_tags+1)]
        Tag.objects.bulk_create(tags)

        tags_qs = list(Tag.objects.all()[:num_tags])

        questions = []
        for i in range(0, num_questions):
            author = random.choice(users_qs)
            tag = random.choice(tags_qs)
            q = Question(author=author, title=f'Title {i}', text=f'Question text {i}')
            questions.append(q)
        Question.objects.bulk_create(questions, batch_size=1000)
        for q in Question.objects.all():
            q.tags.add(random.choice(tags_qs))

        questions_qs = list(Question.objects.all()[:num_questions])

        answers = []
        for i in range(0, num_answers):
            author = random.choice(users_qs)
            question = random.choice(questions_qs)
            answers.append(Answer(author=author, question=question, text=f'Answer text {i}'))
            if len(answers) >= 1000:
                Answer.objects.bulk_create(answers)
                answers = []
        if answers:
            Answer.objects.bulk_create(answers)

        likes = []
        for i in range(num_likes):
            user = random.choice(users_qs)
            question = random.choice(questions_qs)
            value = random.choice([QuestionLike.LIKE, QuestionLike.DISLIKE])
            likes.append(QuestionLike(user=user, question=question, value=value))

            if len(likes) >= 1000:
                QuestionLike.objects.bulk_create(likes, ignore_conflicts=True)
                likes = []

        if likes:
            QuestionLike.objects.bulk_create(likes, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Done.'))