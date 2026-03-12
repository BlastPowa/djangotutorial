import datetime
from django.test import TestCase, TransactionTestCase, RequestFactory, tag
from django.utils import timezone
from .models import Question
from .views import IndexView

# === 1. THE REQUEST FACTORY (Unit Testing Views Directly) ===
# This bypasses the entire Django middleware stack for speed.
class QuestionRequestFactoryTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @tag('fast')  # === 2. TAGGING (Categorizing Tests) ===
    def test_index_view_status(self):
        """
        Uses RequestFactory to call the view directly.
        Bypasses URL routing and middleware.
        """
        request = self.factory.get("/")
        # We manually call the view as a function
        response = IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

# === 3. ADVANCED TRANSACTION TESTING ===
class QuestionTransactionTests(TransactionTestCase):
    @tag('database')
    def test_database_integrity(self):
        """
        TransactionTestCase is used when you need to test 
        atomic blocks or specific database signals.
        """
        q = Question.objects.create(question_text="Transaction?", pub_date=timezone.now())
        self.assertEqual(Question.objects.count(), 1)

# === 4. TAGGING EXAMPLE (Existing Tests) ===
class QuestionModelTests(TestCase):
    @tag('logic', 'fast')
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)