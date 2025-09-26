# Smart Newsletter

Uma aplicação full-stack para curadoria e exibição inteligente de notícias, desenvolvida com arquitetura headless e processamento assíncrono.

🎯 **Sobre o Projeto**

O Newsletter Inteligente automatiza a curadoria de conteúdo através de um agente inteligente, processando e organizando notícias para apresentação em uma interface web moderna e responsiva.

**Características Principais:**

* Backend API REST com Django REST Framework
* Frontend SPA em React responsivo
* Processamento assíncrono: Celery + Redis
* Agente Curador: Sistema high-code de curadoria automática de conteúdo
* Arquitetura Headless: Separação completa entre frontend e backend
* Monitoramento de tarefas Celery via Flower

---

🛠️ **Tecnologias Utilizadas**

### Backend

* Django 5.2
* Django REST Framework
* PostgreSQL 16
* Celery
* Redis
* Flower

### Frontend

* React 18
* Axios
* React Router
* CSS Modules / Styled Components

### DevOps & Infraestrutura

* Docker & Docker Compose
* Python 3.12
* Node.js 18

---

💡 **Decisões Técnicas**

### Por que PostgreSQL?

* **ACID Compliance:** Consistência e integridade dos dados
* **Relações Complexas:** Modelagem de notícias, categorias e metadados
* **Performance:** Consultas complexas com filtros e paginação
* **JSON Support:** Campos JSON nativos para metadados flexíveis

### Por que Redis + Celery?

* **Desacoplamento:** Processamento assíncrono sem bloquear a API
* **Escalabilidade:** Adição de workers conforme a demanda
* **Confiabilidade:** Redis oferece persistência opcional
* **Flexibilidade:** Celery integra perfeitamente com Django

### Por que Arquitetura Headless?

* **Flexibilidade:** Frontend e backend evoluem independentemente
* **Performance:** React SPA oferece experiência de usuário fluida
* **Escalabilidade:** Suporta múltiplos frontends
* **Separação de Responsabilidades:** Cada camada foca em sua especialidade

---

📋 **Pré-requisitos**

* Docker 20.10+
* Docker Compose 2.0+
* Git

---

🚀 **Instalação e Execução**

1. **Clone o repositório**

```bash
git clone <url-do-repositorio>
cd newsletter-inteligente
```

2. **Configure as variáveis de ambiente**

```bash
cp .env.example .env
```

Edite conforme necessário.

3. **Execute com Docker Compose**

```bash
docker-compose up --build
```

Ou em background:

```bash
docker-compose up -d --build
```

4. **Execute as migrações**

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```

5. **Crie um superusuário (opcional)**

```bash
docker-compose exec backend python manage.py createsuperuser
```

6. **Acesse a aplicação**

* Frontend: [http://localhost:3000](http://localhost:3000)
* API Backend: [http://localhost:8000/api/](http://localhost:8000/api/)
* Admin Django: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* Flower: [http://localhost:5555](http://localhost:5555)

---

### 🐳 Docker Compose

```yaml
version: "3.9"

services:
  backend:
    build:
      context: .
      dockerfile: setup/Dockerfile
    container_name: django_app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  frontend:
    build: ./webapp
    container_name: react_app
    volumes:
      - ./webapp:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    stdin_open: true
    tty: true

  celery:
    build:
      context: .
      dockerfile: setup/Dockerfile
    container_name: celery_worker
    command: celery -A setup worker --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - backend
      - redis

  flower:
    image: mher/flower:latest
    container_name: flower
    command: flower --broker=redis://redis:6379/0 --port=5555
    ports:
      - "5555:5555"
    depends_on:
      - redis
      - celery

  db:
    image: postgres:16
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_DB: ${DB_NAME:-smartnews}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "${DB_PORT:-5432}:5432"

  redis:
    image: redis:7-alpine
    container_name: redis_broker
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

### 🔌 API Endpoints

* `admin/`
* `api/news/` [name='news-list']
* `api/news/categories/` [name='news-categories']
* `api/user/register/` [name='user-register']
* `api/user/login/` [name='user-login']
* `api/user/preferences/` [name='user-preferences']
* `api/token/` [name='token_obtain_pair']
* `api/token/refresh/` [name='token_refresh']

**Exemplo de Resposta**

```json
{
    "id": 34,
    "title": "Lançamento do NeuroChip X2 pela CloudX",
    "content": "A CloudX anunciou hoje o lançamento do NeuroChip X2...",
    "summary": "A CloudX anunciou hoje o lançamento do NeuroChip X2...",
    "source": "IDC",
    "category": {
        "id": 3,
        "name": "Negócios"
    },
    "published_at": "2025-09-25T23:52:24.072986Z",
    "created_at": "2025-09-26T03:52:24.153771Z"
}
```

---

✅ **Funcionalidades Implementadas**

* Backend API REST com Django REST Framework
* Frontend React responsivo com paginação
* Filtros por período (dia/semana/mês)
* Agente Curador High-Code para geração de conteúdo
* Banco PostgreSQL com modelagem relacional
* Docker Compose para orquestração de serviços
* Sistema de Mensageria (Redis + Celery)
* Processamento Assíncrono de conteúdo
* Arquitetura Headless completa
* Containerização com Docker
* Organização de Código em estrutura modular

---

🔧 **Desenvolvimento Local**

### Backend Standalone

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py runserver
```

### Frontend Standalone

```bash
cd frontend
npm install
npm start
```

### Executar Celery Worker

```bash
cd backend
celery -A newsletter worker --loglevel=info
```

### Executar Flower

```bash
celery -A newsletter flower --port=5555
```

---

🏛️ **Arquitetura do Agente Curador**

O agente curador implementa um sistema high-code de processamento de conteúdo:

* **Geração de Conteúdo:** Cria notícias baseadas em templates e regras de negócio
* **Processamento Assíncrono:** Utiliza Celery para processamento em background
* **Classificação Inteligente:** Categoriza automaticamente o conteúdo
* **Persistência:** Salva dados estruturados no PostgreSQL

**Fluxo de Processamento**
Agente Trigger → **Redis Queue** → Celery Worker → Content Processing → Database

---

### `.env.example` integrado

```env
# ===========================
# Django Settings
# ===========================

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

# ===========================
# Database
# ===========================

DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''

DATABASE_URL=''

# ===========================
# Celery / Redis
# ===========================

CELERY_BROKER_URL=''
CELERY_RESULT_BACKEND=''

# ===========================
# Flower
# ===========================

FLOWER_PORT=''
```
