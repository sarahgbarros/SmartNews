from celery import shared_task
from django.db import transaction
from django.utils import timezone
from agent.services.gemini_service import GeminiService
from news.models import News, NewsCategory 
from typing import Dict, Any
import logging


logger = logging.getLogger(__name__)


@shared_task(name="process_and_save_news_task")
def process_and_save_news_task(news_data: Dict[str, Any], *args):

    try:
        gemini_service = GeminiService()
        summary = gemini_service.generate_summary(news_data)
        with transaction.atomic():
            category_name = news_data.get("category")
            if NewsCategory.objects.filter(name=category_name).exists():
                category_obj = NewsCategory.objects.get(name=category_name)
            else:
                category_obj = NewsCategory(name=category_name)
                category_obj.save() 
            
            if not News.objects.filter(
                title=news_data.get("title", ""),
                content=news_data.get("content", ""),
                summary=summary,
                source=news_data.get("source", "Unknown"),
                category=category_obj,
                published_at=news_data.get("published_at", timezone.now()),
                created_at=timezone.now()
            ).exists():
                
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
            
            else:
                return "Notícia duplicada."
            
    except Exception as e:
        logger.error(f"Erro ao salvar notícia: {e}")
        return f"Erro ao salvar notícia: {e}"   