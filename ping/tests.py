from django.test import TestCase, SimpleTestCase
from ping.models import Url
from django.urls import reverse
from ping.forms import UrlForm


class CustomUrlTests(TestCase):
    def test_create_url(self):
        url_entity = Url
        test_url = url_entity.objects.create(
            link="https://www.google.com",
            status=200,
            response_time=0.2,
            regexp="^google",
            regexp_match=False,
            match_details=None
        )
        self.assertEqual(test_url.link, 'https://www.google.com')
        self.assertEqual(test_url.status, 200)
        self.assertEqual(test_url.response_time, 0.2)
        self.assertEqual(test_url.regexp, '^google')
        self.assertEqual(test_url.regexp_match, False)
        self.assertEqual(test_url.match_details, None)


class IndexPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_index_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_page_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_index_page_contains_correct_html(self):
        self.assertContains(self.response, 'Url Ping')

    def test_index_page_does_not_contain_incorrect_html(self):  # new
        self.assertNotContains(self.response, "Your Ping information on")

    def test_url_ping_form(self):  # new
        form = self.response.context.get('form')
        self.assertIsInstance(form, UrlForm)


class ResultPageTests(TestCase):
    def setUp(self):
        url = reverse('ping')
        data = {"url": "https://www.google.com", "regexp": "g....e"}
        self.response_correct = self.client.post(url, data)
        self.response_missing_data = self.client.post(url)  # form data are missing in this POST request
        self.response_wrong = self.client.get(url)  # it should be a POST request, not GET

    def test_result_page_status_code(self):
        self.assertEqual(self.response_correct.status_code, 200)
        self.assertEqual(self.response_missing_data.status_code, 302)  # code for redirecting
        self.assertEqual(self.response_wrong.status_code, 302)

    def test_result_page_template(self):
        self.assertTemplateUsed(self.response_correct, "result.html")
        self.assertRedirects(self.response_missing_data, reverse("home"))
        self.assertRedirects(self.response_missing_data, "/")
        self.assertRedirects(self.response_wrong, reverse("home"))

    def test_result_page_contains_correct_html(self):
        self.assertContains(self.response_correct, 'Your Ping information on')

    def test_result_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response_correct, "What will you get")
