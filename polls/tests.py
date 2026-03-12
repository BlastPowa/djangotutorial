import datetime
from django.test import TestCase, SimpleTestCase, TransactionTestCase, LiveServerTestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# === TESTING TOOLS: Using the Client and Context (TestCase) ===
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Uses the 'Client' tool to check that if no questions exist,
        the appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        # Verifying context data as shown in the Testing Tools docs
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        The index page displays questions with a pub_date in the past.
        """
        question = Question.objects.create(question_text="Past question.", pub_date=timezone.now() - datetime.timedelta(days=30))
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question_404(self):
        """
        The detail view of a future question returns a 404 not found.
        """
        future_question = Question.objects.create(question_text="Future question.", pub_date=timezone.now() + datetime.timedelta(days=5))
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

# === TESTING TOOLS: SimpleTestCase (No Database) ===
class PollsSimpleTests(SimpleTestCase):
    def test_admin_login_template(self):
        """
        Uses 'assertTemplateUsed' tool to verify the admin page 
        is rendered with the correct template.
        """
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

# === TESTING TOOLS: TransactionTestCase (Database Logic) ===
class QuestionTransactionTests(TransactionTestCase):
    def test_was_published_recently_logic(self):
        time = timezone.now() - datetime.timedelta(hours=23)
        recent_question = Question.objects.create(question_text="Recent?", pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

# === TESTING TOOLS: LiveServerTestCase (Live Environment) ===
class PollsLiveTests(LiveServerTestCase):
    def test_live_index_access(self):
        """Checks accessibility via the live server URL."""
        response = self.client.get(self.live_server_url + reverse('polls:index'))
        self.assertEqual(response.status_code, 200)