Smart Newsletter
Uma aplicação full-stack para curadoria e exibição inteligente de notícias, desenvolvida com arquitetura headless e comunicação assíncrona.


🎯 Sobre o Projeto

O Newsletter Inteligente é uma aplicação que automatiza a curadoria de conteúdo através de um agente inteligente, processando e organizando notícias para apresentação em uma interface web moderna e responsiva.
Características Principais

Backend API REST: Desenvolvido em Django REST Framework

Frontend SPA: Interface React responsiva

Processamento Assíncrono: Celery + RabbitMQ para tarefas em background

Agente Curador: Sistema high-code de curadoria automática de conteúdo

Arquitetura Headless: Separação completa entre frontend e backend

🛠️ Tecnologias Utilizadas

Backend

Django 5.2 - Framework web robusto e escalável
Django REST Framework - Toolkit para construção de APIs REST
PostgreSQL 16 - Banco de dados relacional
Celery - Processamento de tarefas assíncronas
RabbitMQ - Message broker para comunicação assíncrona

Frontend

React 18 - Biblioteca para construção de interfaces
Axios - Cliente HTTP para comunicação com a API
React Router - Navegação SPA
CSS Modules/Styled Components - Estilização modular

DevOps & Infraestrutura

Docker & Docker Compose - Containerização
Python 3.12 - Linguagem principal do backend
Node.js 18 - Runtime para o frontend

💡 Decisões Técnicas

Por que PostgreSQL?

ACID Compliance: Garante consistência e integridade dos dados

Relações Complexas: Ideal para modelar relacionamentos entre notícias, categorias e metadados

Performance: Excelente desempenho para consultas complexas com filtros e paginação

JSON Support: Suporte nativo a campos JSON para metadados flexíveis

Por que RabbitMQ + Celery?

Desacoplamento: Permite processamento assíncrono sem bloquear a API

Escalabilidade: Facilita a adição de workers conforme a demanda

Confiabilidade: RabbitMQ oferece persistência de mensagens e garantia de entrega

Flexibilidade: Celery integra perfeitamente com Django

Por que Arquitetura Headless?

Flexibilidade: Frontend e backend podem evoluir independentemente

Performance: React SPA oferece experiência de usuário mais fluida

Escalabilidade: Possibilita múltiplos frontends (web, mobile, etc.)

Separação de Responsabilidades: Cada camada foca em sua especialidade


📋 Pré-requisitos

Docker 20.10+
Docker Compose 2.0+
Git

🚀 Instalação e Execução

1. Clone o repositório
bashgit clone <url-do-repositorio>
cd newsletter-inteligente
2. Configure as variáveis de ambiente
bash# Crie um arquivo .env na raiz do projeto
cp .env.example .env

# Edite as variáveis conforme necessário

DATABASE_URL=postgresql://postgres:password@db:5432/newsletter
CELERY_BROKER_URL=pyamqp://guest@rabbitmq//
SECRET_KEY=your-secret-key-here
DEBUG=True

3. Execute com Docker Compose

bash# Construa e inicie todos os serviços
docker-compose up --build

# Para executar em background

docker-compose up -d --build

4. Execute as migrações

bash# Em outro terminal
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput

5. Crie um superusuário (opcional)
bashdocker-compose exec backend python manage.py createsuperuser

6. Acesse a aplicação

Frontend: http://localhost:3000

API Backend: http://localhost:8000/api/

Admin Django: http://localhost:8000/admin/


🔌 API Endpoints

admin/

api/news/ [name='news-list']

api/news/categories/ [name='news-categories']

api/user/register/ [name='user-register']

api/user/login/ [name='user-login']

api/user/preferences/ [name='user-preferences']

api/token/ [name='token_obtain_pair']

api/token/refresh/ [name='token_refresh']

## Exemplo de Resposta

    {
        "id": 34,
        "title": "Lançamento do NeuroChip X2 pela CloudX",
        "content": "A CloudX anunciou hoje o lançamento do NeuroChip X2, uma inovação que promete revolucionar o setor de computação em nuvem. O novo dispositivo traz baixo consumo de energia, com foco em melhorar a produtividade. Especialistas acreditam que essa tecnologia pode aumentar a competitividade.",
        "summary": "A CloudX anunciou hoje o lançamento do NeuroChip X2, uma inovação que promete revolucionar o setor de computação em nuvem. O novo dispositivo traz baixo consumo de energia, com foco em melhorar a prod...",
        "source": "IDC",
        "category": {
            "id": 3,
            "name": "Negócios"
        },
        "published_at": "2025-09-25T23:52:24.072986Z",
        "created_at": "2025-09-26T03:52:24.153771Z"
    }

✅ Funcionalidades Implementadas


 Backend API REST com Django REST Framework

 Frontend React responsivo com paginação

 Filtros por período (dia/semana/mês)

 Agente Curador High-Code para geração de conteúdo

 Banco PostgreSQL com modelagem relacional

 Docker Compose para orquestração de serviços

 Sistema de Mensageria (RabbitMQ + Celery)

 Processamento Assíncrono de conteúdo
  
 Arquitetura Headless completa

 Containerização com Docker

 Organização de Código em estrutura modular

🔧 Desenvolvimento Local

Backend Standalone

bashcd backend

python -m venv venv

source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

python manage.py runserver

Frontend Standalone

bashcd frontend

npm install

npm start

Executar Celery Worker

bashcd backend

celery -A newsletter worker --loglevel=info

🏛️ Arquitetura do Agente Curador

O agente curador implementa um sistema high-code de processamento de conteúdo:

Geração de Conteúdo: Cria notícias baseadas em templates e regras de negócio

Processamento Assíncrono: Utiliza Celery para processamento em background

Classificação Inteligente: Categoriza automaticamente o conteúdo

Persistência: Salva dados estruturados no PostgreSQL

Fluxo de Processamento

Agente Trigger → RabbitMQ Queue → Celery Worker → Content Processing → Database