from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from ping.models import Url
from ping.forms import UrlForm
from ping.ping_pack.ping_data import Ping


class CustomUrlFormTests(TestCase):
    def test_create_form(self):
        form_good_1 = UrlForm(data={"url": "https://www.google.com", "regexp": "^<"})
        form_good_2 = UrlForm(data={"url": "http://www.google.com", "regexp": ""})
        form_missing_url = UrlForm(data={"url": "", "regexp": ""})  # url is mandatory
        form_bad_url = UrlForm(data={"url": "this is not a url", "regexp": ""})
        form_not_existing_url = UrlForm(data={"url": "https://www.websitethatdoesnotexist.com/", "regexp": ""})

        self.assertTrue(form_good_1.is_valid())
        self.assertTrue(form_good_2.is_valid())
        self.assertFalse(form_missing_url.is_valid())
        self.assertFalse(form_bad_url.is_valid())
        self.assertTrue(form_not_existing_url.is_valid())  # accepted because the url formatting is correct


class CustomUrlTests(TestCase):
    def test_create_url(self):
        custom_url = Url.objects.create(
            link="https://www.google.com",
            status=200,
            response_time=0.2,
            regexp="^google",
            regexp_match=False,
            match_details=None
        )
        self.assertEqual(custom_url.link, 'https://www.google.com')
        self.assertEqual(custom_url.status, 200)
        self.assertEqual(custom_url.response_time, 0.2)
        self.assertEqual(custom_url.regexp, '^google')
        self.assertEqual(custom_url.regexp_match, False)
        self.assertEqual(custom_url.match_details, None)


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


class TestPing(TestCase):
    def setUp(self):
        self.good_ping = Ping("https://www.google.com")

    def test_ping(self):
        self.assertIsInstance(self.good_ping, Ping)
        self.assertIsInstance(self.good_ping.status, int)
        self.assertEqual(self.good_ping.status, 200)
        self.assertIsInstance(self.good_ping.response_time, str)  # change to float !
        self.assertIsInstance(self.good_ping.content, str)  # check with other urls
        self.assertRaises(ConnectionError, Ping, "https://www.google_plus_some_random_stuff.com")
        self.assertRaises(ConnectionError, Ping, "ww.google.com")
        self.assertRaises(ConnectionError, Ping, "www.google.comm")

    def test_connect_attempt(self):
        self.assertRaises(ConnectionError, Ping.connect_attempt, "https://www.this_url_does_not_exist.com")
        self.assertIsNotNone(Ping.connect_attempt("https://www.google.com"))
        self.assertIsInstance(Ping.connect_attempt("https://www.google.com"), object)

    def test_is_regexp_matching(self):
        self.assertIsNotNone(Ping.is_regexp_matching("^m...h$", "match"))
        self.assertTrue(Ping.is_regexp_matching("^m...h$", "match")[0])
        self.assertEqual(Ping.is_regexp_matching("^m...h$", "match")[1], "match")
        self.assertFalse(Ping.is_regexp_matching("^m...h$", "not_a_match")[0])
        self.assertEqual(Ping.is_regexp_matching("^m...h$", "not_a_match")[1], "")
        self.assertIsInstance(Ping.is_regexp_matching("^m", "match")[1], str)

    def test_get_ping_data(self):
        self.assertIsInstance(self.good_ping.get_ping_data()[0], int)
        self.assertIsInstance(self.good_ping.get_ping_data()[1], str)
        self.assertIsInstance(self.good_ping.get_ping_data()[2], str)
        self.assertIn(".", self.good_ping.get_ping_data()[1])
