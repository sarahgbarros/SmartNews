from django.test import TestCase
from news.models import News
from agent.generate_news import generate_news, import_news_from_files

class GenerateNewsTest(TestCase):
    def test_generate_news_creates_new_entry(self):
        title = generate_news()
        self.assertTrue(News.objects.filter(title=title).exists())

    def test_generate_news_returns_duplicate_message(self):
        title = generate_news()
        result = generate_news()
        self.assertIn("Notícia duplicada", result)

class ImportNewsTest(TestCase):
    def test_import_news_creates_entries(self):
        result = import_news_from_files()
        self.assertIsInstance(result, str)
        self.assertIn("notícias importadas", result)
        self.assertGreater(News.objects.count(), 0)


