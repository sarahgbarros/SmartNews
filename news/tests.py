from django.test import TestCase
from news.models import News, NewsCategory
from datetime import datetime

class NewsModelTest(TestCase):
    def test_create_news_with_category(self):
        category = NewsCategory.objects.create(name="Tecnologia")
        news = News.objects.create(
            title="Título Teste",
            content="Conteúdo de teste",
            summary="Resumo de teste",
            source="Fonte Teste",
            category=category,
            published_at=datetime.now(),
            created_at=datetime.utcnow()
        )
        self.assertEqual(str(news.title), "Título Teste")
        self.assertEqual(news.category.name, "Tecnologia")
        self.assertIsInstance(news.published_at, datetime)
        self.assertIsInstance(news.created_at, datetime)