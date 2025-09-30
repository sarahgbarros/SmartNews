import random

from datetime import datetime
from django.utils import timezone
from celery import shared_task
from agent.utils import read_csv, read_json
from .consumer import process_and_save_news_task
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
        "title": "{company} atinge meta de {goal_type} e investe R$ {investment} em {project_name}",
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
    "company_a": ["TechNova", "CloudX", "NeuralSoft", "GreenAI"],
    "company_b": ["InnovateX", "SkyNet", "GreenTech", "NextAI"],
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
    "value": ["200", "450", "780"],
    "goal": ["expandir mercado", "aumentar receita", "melhorar eficiência"],
    "market": ["global", "regional", "local"],
    "related_sector": ["tecnologia", "finanças", "energia"],
    "governing_body": ["Conselho Federal", "Agência Nacional de Tecnologia", "Ministério da Economia"],
    "main_objective": ["proteger consumidores", "garantir transparência", "fomentar inovação"],
    "target_group": ["empresas", "cidadãos", "startups"],
    "benefit": ["oportunidades de crescimento", "novas parcerias", "eficiência operacional"],
    "risk": ["aumento de custos", "diminuição da competitividade", "impacto ambiental"],
    "effective_date": ["2025-01-01", "2025-06-01", "2025-12-01"],
    "goal_type": ["lucro", "eficiência", "sustentabilidade"],
    "investment": ["50", "120", "300"],
    "project_name": ["Project Alpha", "Green Initiative", "Cloud Expansion"],
    "reduction_metric": ["custos operacionais", "emissões de CO2", "tempo de produção"],
    "focus_area": ["inovação tecnológica", "sustentabilidade", "expansão de mercado"],
    "market_trend": ["crescimento acelerado", "digitalização", "automação"],
}

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

    try:
        title = template["title"].format(**data)
        content = template["content"].format(**data)
        category = random.choice(CATEGORIES)["name"]

        news_data = {
            "title": title,
            "content": content,
            "source": data["source"],
            "category": category,
            "published_at": datetime.now().isoformat(),
        }

        process_and_save_news_task.apply_async((news_data,), queue='consumer')
        
        return news_data
        
    except Exception as err:
        print(f"Erro ao gerar e enviar notícia para a fila: {err}")
        raise err



@shared_task(name="import_news_from_files")
def import_news_from_files_task():

    count = 0
    
    try:
        csv_news = read_csv("agent/data/tech_news.csv")
        json_news = read_json("agent/data/tech_news_expanded.json")
        
        csv_news = csv_news if isinstance(csv_news, list) else []
        json_news = json_news if isinstance(json_news, list) else []
        
        all_news = csv_news + json_news
        
        if not all_news:
            return "Nenhuma notícia encontrada nos arquivos."

        for n in all_news:
            if n.get("title") and n.get("content"):
                
                news_data = {
                    "title": n["title"],
                    "content": n["content"],
                    "source": n.get("source", "Unknown"),
                    "category": n.get("category", "Tecnologia"),
                    "published_at": n.get("published_at", timezone.now().isoformat()),
                }
        
                process_and_save_news_task.apply_async((news_data,), queue='consumer')
                count += 1

        return news_data
    
    except Exception as err:
        print(f"Erro ao gerar e enviar notícia para a fila: {err}")
        raise err
    