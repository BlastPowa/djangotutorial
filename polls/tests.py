import datetime
from django.test import TestCase, SimpleTestCase, TransactionTestCase, LiveServerTestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice

# === Requirement 1: TestCase (Now 5 tests for extra credit) ===
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionViewTests(TestCase):
    def test_future_question_does_not_appear_on_index(self):
        """Questions with a pub_date in the future aren't displayed on index."""
        Question.objects.create(question_text="Future question.", pub_date=timezone.now() + datetime.timedelta(days=30))
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")

    def test_choice_content(self):
        """Verify that a choice is correctly linked to a question."""
        q = Question.objects.create(question_text="Choice Test", pub_date=timezone.now())
        c = Choice.objects.create(question=q, choice_text="The Choice", votes=0)
        self.assertEqual(c.question, q)

# === Requirement 2: SimpleTestCase (2 tests) ===
class PollsSimpleTests(SimpleTestCase):
    def test_admin_login_url_status(self):
        """
        Checking the admin login. This works in SimpleTestCase 
        because it doesn't query the 'polls' database tables.
        """
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)

    def test_admin_redirect(self):
        """Check if the base admin URL redirects correctly (302)."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

# === Requirement 3: TransactionTestCase (1 test) ===
class QuestionTransactionTests(TransactionTestCase):
    def test_question_persistence(self):
        """Verify database record creation persists across transactions."""
        Question.objects.create(question_text="Transaction test", pub_date=timezone.now())
        self.assertEqual(Question.objects.count(), 1)

# === Requirement 4: LiveServerTestCase (1 test) ===
class PollsLiveTests(LiveServerTestCase):
    def test_admin_page_availability(self):
        """Verify the live server serves the admin login page."""
        response = self.client.get(self.live_server_url + '/admin/login/')
        self.assertEqual(response.status_code, 200)