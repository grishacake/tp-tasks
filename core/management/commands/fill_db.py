from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
import random


class Command(BaseCommand):
    help = "Fill database with test data. Usage: python manage.py fill_db <ratio>"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Base ratio for filling data')

    def handle(self, *args, **options):
        ratio = options['ratio']
        fake = Faker()

        User = get_user_model()

        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        self.stdout.write(self.style.NOTICE(f"ratio = {ratio}"))
        self.stdout.write(self.style.NOTICE(f"Users: {num_users}"))
        self.stdout.write(self.style.NOTICE(f"Questions: {num_questions}"))
        self.stdout.write(self.style.NOTICE(f"Answers: {num_answers}"))
        self.stdout.write(self.style.NOTICE(f"Tags: {num_tags}"))
        self.stdout.write(self.style.NOTICE(f"Likes (questions+answers): {num_likes * 2}"))

        # ---------- Users ----------
        self.stdout.write("Creating users...")
        users = []
        existing_users = User.objects.count()
        for i in range(num_users):
            username = f"user_{existing_users + i + 1}"
            u = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="12345678"
            )
            users.append(u)
        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users"))

        # ---------- Tags ----------
        self.stdout.write("Creating tags...")
        tags = []
        for _ in range(num_tags):
            t = Tag.objects.create(name=fake.unique.word()[:32])
            tags.append(t)
        self.stdout.write(self.style.SUCCESS(f"Created {len(tags)} tags"))

        # ---------- Questions ----------
        self.stdout.write("Creating questions...")
        questions = []
        for _ in range(num_questions):
            q = Question.objects.create(
                title=fake.sentence(nb_words=6),
                detailed=fake.text(max_nb_chars=400),
                author=random.choice(users),
                rating=random.randint(-10, 100),
            )
            if tags:
                q.tags.add(*random.sample(tags, k=min(3, len(tags))))
            questions.append(q)
        self.stdout.write(self.style.SUCCESS(f"Created {len(questions)} questions"))

        # ---------- Answers ----------
        self.stdout.write("Creating answers...")
        answers = []
        for _ in range(num_answers):
            a = Answer.objects.create(
                question=random.choice(questions),
                author=random.choice(users),
                answer_text=fake.text(max_nb_chars=300),
                rating=random.randint(-10, 100),
            )
            answers.append(a)
        self.stdout.write(self.style.SUCCESS(f"Created {len(answers)} answers"))

        # ---------- QuestionLikes ----------
        self.stdout.write("Creating question likes...")
        q_like_pairs = set()
        question_likes = []
        attempts = 0
        target_q_likes = num_likes

        while len(q_like_pairs) < target_q_likes and attempts < target_q_likes * 10:
            attempts += 1
            u = random.choice(users)
            q = random.choice(questions)
            key = (u.id, q.id)
            if key in q_like_pairs:
                continue
            q_like_pairs.add(key)
            value = random.choice([1, -1])
            question_likes.append(QuestionLike(
                user=u,
                question=q,
                value=value
            ))
        QuestionLike.objects.bulk_create(question_likes)
        self.stdout.write(self.style.SUCCESS(f"Created {len(question_likes)} question likes"))

        # ---------- AnswerLikes ----------
        self.stdout.write("Creating answer likes...")
        a_like_pairs = set()
        answer_likes = []
        attempts = 0
        target_a_likes = num_likes

        while len(a_like_pairs) < target_a_likes and attempts < target_a_likes * 10:
            attempts += 1
            u = random.choice(users)
            a = random.choice(answers)
            key = (u.id, a.id)
            if key in a_like_pairs:
                continue
            a_like_pairs.add(key)
            value = random.choice([1, -1])
            answer_likes.append(AnswerLike(
                user=u,
                answer=a,
                value=value
            ))
        AnswerLike.objects.bulk_create(answer_likes)
        self.stdout.write(self.style.SUCCESS(f"Created {len(answer_likes)} answer likes"))

        self.stdout.write(self.style.SUCCESS("Database filled successfully"))
