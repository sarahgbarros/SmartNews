import random
from datetime import datetime
from celery import shared_task
from news.models import News, NewsCategory
from agent.utils import read_csv, read_json
from typing import List, Dict

TEMPLATES: List[Dict[str, str]] = [
            {
                "title": "Lançamento do {product} pela {company}",
                "content": (
                    "A {company} anunciou hoje o lançamento do {product}, uma inovação que promete "
                    "revolucionar o setor de {sector}. O novo dispositivo traz {features}, com foco "
                    "em {impact}. Especialistas acreditam que essa tecnologia pode {prediction}."
                    ),
                    },
            {
                "title": "Avanço em {technology} surpreende {audience}",
                "content": (
                    "Pesquisadores da {university} apresentaram um avanço significativo em {technology}. "
                    "O estudo publicado recentemente mostra como essa descoberta pode {impact}, "
                    "abrindo espaço para aplicações em {applications}."
                    ),
                    },
            {
                "title": "Mercado de {topic} cresce {percent}% em {year}",
                "content": (
                    "Segundo dados divulgados pela {source}, o mercado de {topic} registrou um crescimento "
                    "de {percent}% no último ano. Esse resultado reflete a crescente demanda por {products}, "
                    "especialmente em regiões como {region}. Analistas projetam que até {future_year}, o setor "
                    "poderá alcançar um faturamento de {revenue} bilhões."
                    ),
            },
            ]

DATASETS = {
            "company": ["TechNova", "CloudX", "NeuralSoft", "GreenAI"],
            "product": ["NeuroChip X2", "CloudBox One", "EcoDrone Pro"],
            "sector": ["inteligência artificial", "computação em nuvem", "energia renovável"],
            "features": ["alta performance", "baixo consumo de energia", "design modular"],
            "impact": ["transformar indústrias", "melhorar a produtividade", "reduzir custos"],
            "prediction": ["mudar o mercado global", "gerar novos empregos", "aumentar a competitividade"],
            "technology": ["computação quântica", "aprendizado profundo", "baterias de lítio-enxofre"],
            "university": ["MIT", "USP", "Stanford", "Oxford"],
            "applications": ["saúde", "finanças", "transportes"],
            "audience": ["investidores", "cientistas", "indústrias"],
            "topic": ["inteligência artificial", "computação em nuvem", "realidade aumentada"],
            "percent": ["15", "32", "48"],
            "year": ["2024", "2025"],
            "future_year": ["2030", "2035"],
            "revenue": ["120", "450", "980"],
            "products": ["soluções de IA", "plataformas em nuvem", "dispositivos inteligentes"],
            "region": ["América Latina", "Europa", "Ásia"],
            "source": ["Gartner", "IDC", "McKinsey", "Forbes Tech"],}

CATEGORIES = [
    {"id": 1, "name": "Tecnologia"},
    {"id": 2, "name": "Negócios"},
    {"id": 3, "name": "Ciência"},
    {"id": 4, "name": "Energia"},
]

@shared_task(name="generate_news_task")
def generate_news_task():
    template = random.choice(TEMPLATES)
    data = {k: random.choice(v) for k, v in DATASETS.items()}

    title = template["title"].format(**data)
    content = template["content"].format(**data)
    summary = content[:200] + "..." if len(content) > 200 else content
    category = random.choice(CATEGORIES)["name"]
    published_at = datetime.now()

    category_obj = NewsCategory.objects.filter(name=category).first()
    if not category_obj:
        category_obj = NewsCategory.objects.create(name=category)

    news = News.objects.create(
        title=title,
        content=content,
        summary=summary,
        source=data["source"],
        category=category_obj,
        published_at=published_at,
        created_at=datetime.utcnow()
    )
    return news.title

@shared_task(name="import_news_from_files")
def import_news_from_files():
    
    try:
        csv_news = read_csv("src/data/tech_news.csv")
        json_news = read_json("src/data/tech_news_expanded.json")
        all_news = csv_news + json_news

        news_objects = []
        for n in all_news:
            if n.get("title") and n.get("content"):
                news_objects.append(
                    News(
                        title=n["title"],
                        content=n["content"],
                        summary=n.get("summary", n["content"][:200]),
                        source=n.get("source", "Unknown"),
                        category=n.get("category", "Tecnologia"),
                        published_at=n.get("published_at", datetime.now()),
                        created_at=datetime.utcnow()
                    )
                )
        News.objects.bulk_create(news_objects)
        return f"{len(news_objects)} notícias importadas com sucesso."

    except Exception as e:
        raise e
    