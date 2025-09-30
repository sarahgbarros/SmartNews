from celery import shared_task
from django.db import transaction
from django.utils import timezone
from agent.services.gemini_service import GeminiService
from news.models import News, NewsCategory 
from typing import Dict, Any


@shared_task(bind=True, name="process_and_save_news_task")
def process_and_save_news_task(self, news_data: Dict[str, Any], *args):

    try:
        gemini_service = GeminiService()
        summary = gemini_service.generate_summary(news_data)
        with transaction.atomic():
            category_name = news_data.get("category", "Tecnologia")
            category_obj, created = NewsCategory.objects.get_or_create(name=category_name)
            
            news_obj = News(
                title=news_data["title"],
                content=news_data["content"],
                summary=summary,
                source=news_data.get("source", "Unknown"),
                category=category_obj,
                published_at=news_data.get("published_at", timezone.now()),
                created_at=timezone.now()
            )
            news_obj.save()
            
            return f"Notícia '{news_obj.title}' salva com sucesso."
    
    except Exception as e:
        print(f"Erro ao processar e salvar notícia: {e}")
        return f"Erro ao salvar notícia: {e}"   