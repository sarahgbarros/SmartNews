import random
from datetime import datetime
from typing import List, Dict
import sys
import os
import django

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

django.setup()

from news.models import News, NewsCategory
from utils import read_csv, read_json


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
    {
        "title": "Fusão entre {company_a} e {company_b} cria gigante de {sector}",
        "content": (
            "As empresas {company_a} e {company_b} anunciaram um acordo de fusão no valor de "
            "R$ {value} bilhões, criando uma nova gigante no setor de {sector}. "
            "O principal objetivo da união é {goal}, expandindo a atuação em {market}. "
            "A transação ainda depende da aprovação de órgãos reguladores, mas deve "
            "remodelar a competição no mercado de {related_sector}."
        ),
    },
    {
        "title": "Novo marco regulatório de {topic} aprovado pelo {governing_body}",
        "content": (
            "O {governing_body} aprovou hoje o novo marco regulatório para o setor de {topic}. "
            "A nova legislação visa {main_objective} e traz implicações diretas para {target_group}. "
            "Enquanto defensores destacam o potencial de {benefit}, críticos alertam para "
            "o risco de {risk} no curto prazo. A lei entra em vigor em {effective_date}."
        ),
    },
    {
        "title": "{Company} atinge meta de {goal_type} e investe R$ {investment} em {project_name}",
        "content": (
            "A {company} anunciou que atingiu sua meta de {goal_type} com dois anos de antecedência, "
            "reduzindo {reduction_metric} em suas operações globais. Para continuar o avanço, a empresa "
            "irá investir R$ {investment} milhões no projeto {project_name}, focado em {focus_area}. "
            "Este movimento reforça a tendência de {market_trend} no mercado de {sector}."
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
    "source": ["Gartner", "IDC", "McKinsey", "Forbes Tech"],
}

CATEGORIES = [
    {"id": 1, "name": "Tecnologia"},
    {"id": 2, "name": "Negócios"},
    {"id": 3, "name": "Ciência"},
    {"id": 4, "name": "Energia"},
]


def generate_news():
    template = random.choice(TEMPLATES)
    data = {k: random.choice(v) for k, v in DATASETS.items()}

    try:
        title = template["title"].format(**data)
        content = template["content"].format(**data)
        summary = content[:200] + "..." if len(content) > 200 else content
        category = random.choice(CATEGORIES)["name"]
        published_at = datetime.now()

        category_obj = NewsCategory.objects.filter(name=category).first()
        if not category_obj:
            category_obj = NewsCategory.objects.create(name=category)

        if not News.objects.filter(
            title=title,
            content=content,
            summary=summary,
            source=data["source"],
            category_id=category_obj,
            published_at=published_at,
        ).exists():

            news = News.objects.create(
                title=title,
                content=content,
                summary=summary,
                source=data["source"],
                category_id=category_obj,
                published_at=published_at,
                created_at=datetime.utcnow(),
            )
            return news.title
        
        else:
            return "Notícia duplicada. Nenhuma nova notícia foi criada."
    except Exception as e:
        raise e 

def import_news_from_files():
    try:
        csv_news = read_csv("src/data/tech_news.csv")
        json_news = read_json("src/data/tech_news_expanded.json")
        all_news = csv_news + json_news

        news_objects = []
        for n in all_news:
            if n.get("title") and n.get("content"):
            
                category_name = n.get("category", "Tecnologia")
                category_obj = NewsCategory.objects.filter(name=category_name).first()
                if not category_obj:
                    category_obj = NewsCategory.objects.create(name=category_name)
                
                news_objects.append(
                    News(
                        title=n["title"],
                        content=n["content"],
                        summary=n.get("summary", n["content"][:200]),
                        source=n.get("source", "Unknown"),
                        category_id=category_obj,
                        published_at=n.get("published_at", datetime.now()),
                        created_at=datetime.utcnow(),
                    )
                )
        News.objects.bulk_create(news_objects)
        return f"{len(news_objects)} notícias importadas com sucesso."

    except Exception as e:
        raise e


if __name__ == "__main__":
    generated_news = generate_news()
    extracted_news = import_news_from_files()
    print(f"Generated news: {generated_news}, extracted news: {extracted_news}")