from django.test import TestCase
from news.models import News
from .news.generate_news import generate_news, import_news_from_files
from .agent.services.gemini import GeminiService

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

class GeminiTest(TestCase):
    def test_gemini_integration(self):
        result = GeminiService.generate_text("Test prompt")
        self.assertIsInstance(result, str)
        self.assertTrue(True)  


