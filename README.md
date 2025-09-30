# Smart Newsletter 🗞️
Uma aplicação full-stack para curadoria e exibição inteligente de notícias, desenvolvida com arquitetura headless e processamento assíncrono. O projeto é centrado em um Agente Curador High-Code que utiliza IA (Gemini) para processar e resumir conteúdo automaticamente.

🎯 Sobre o Projeto
O Smart Newsletter automatiza a curadoria de conteúdo, garantindo que as notícias sejam processadas, resumidas (via Gemini) e persistidas em background antes de serem servidas a uma interface web moderna.

## Características Principais:
Agente Curador High-Code: Sistema automático de curadoria e ingestão de conteúdo.

Arquitetura Produtor/Consumidor: Celery Workers segregados por filas para desacoplar tarefas (Produtor: busca/disparo; Consumidor: IA/DB).

Inteligência Artificial: Integração com a Gemini API para gerar resumos concisos e profissionais.

Backend API REST: Desenvolvido com Django REST Framework.

Frontend SPA: Interface moderna e responsiva em React.

Monitoramento: Flower para acompanhamento em tempo real das tarefas Celery.

🛠️ Tecnologias Utilizadas
Backend: Django 5.2, Django REST Framework

Processamento: Celery, Redis (7.x)

Inteligência Artificial: Google Gemini API (gemini-2.5-flash)

Banco de Dados: PostgreSQL 16

Frontend: React 18, Axios, React Router

DevOps: Docker & Docker Compose 3.9

💡 Decisões Técnicas
1. Arquitetura Assíncrona (Celery Produtor/Consumidor)
O pipeline de curadoria é dividido em dois workers e filas dedicadas, garantindo que tarefas lentas (Chamadas à Gemini) não bloqueiem o pipeline de ingestão.

Fila producer: Tarefas rápidas (busca e disparo).

Fila consumer: Tarefas lentas e caras (processamento de IA e persistência no DB).

2. Por que PostgreSQL?
ACID Compliance: Essencial para a integridade dos dados, garantindo que cada notícia seja salva de forma atômica.

Relações Complexas: Modelagem robusta de notícias, categorias e metadados.

3. Por que Arquitetura Headless?
Flexibilidade e Escalabilidade: Frontend e backend evoluem e escalam independentemente, permitindo que a API atenda a múltiplos clientes.

📋 Pré-requisitos
Docker 20.10+

Docker Compose 2.0+

Git

Variáveis de Ambiente: A chave da API Gemini (GEMINI_API_KEY) deve ser configurada no seu arquivo .env e é carregada automaticamente para os workers Celery.

🚀 Instalação e Execução
1. Clone o repositório
git clone <url-do-repositorio>
cd smartnews

2. Configure as variáveis de ambiente
Crie e edite o arquivo .env com as credenciais do banco e a chave Gemini:

cp .env.example .env

3. Execute com Docker Compose
Este comando inicia todos os 7 serviços (DB, Redis, Backend, Frontend, Produtor, Consumidor, Beat e Flower):

docker-compose up --build

4. Setup Inicial
Execute as migrações do banco de dados e a coleta de arquivos estáticos (essencial para o Admin):

docker-compose exec backend python manage.py migrate --noinput
docker-compose exec backend python manage.py collectstatic --noinput

5. Iniciar a Curadoria
O fluxo de curadoria é iniciado através de uma task Celery.

Para Teste Imediato: Dispare o processo usando o Management Command:

docker-compose exec backend python manage.py start_curation

Para Agendamento Contínuo: Configure a frequência de execução das tarefas produtoras (agent.tasks.generate_news_task, etc.) no Django Admin (Seção Celery Beat).

🌐 Endpoints Principais
Frontend: http://localhost:3000

API Backend: http://localhost:8000/api/

Admin Django: http://localhost:8000/admin/

Flower (Monitor Celery): http://localhost:5555

🏛️ Fluxo de Processamento do Agente Curador
Agente Trigger (start_curation.py) → Redis Queue (producer) → Celery Worker (celery_producer) → Roteamento → Redis Queue (consumer) → Celery Worker (celery_consumer com Gemini Service) → PostgreSQL (Persistência)