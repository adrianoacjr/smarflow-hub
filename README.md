SMART HUB – AUTOMACAO OMNICHANNEL COM WHATSAPP/INSTAGRAM (IA)
Visão Geral

SmartHub é uma plataforma modular para automatizar comunicação, atendimento e fluxos operacionais via WhatsApp e Instagram, utilizando IA para análise e respostas inteligentes.
O objetivo é entregar automações, campanhas, bots e integrações corporativas de forma simples e escalável.

Arquitetura do Projeto

Estrutura de pastas recomendada:

/smarthub
backend/
src/
api/
application/
domain/
infrastructure/
shared/
main.py
tests/
requirements.txt
README.md

frontend/
    src/
        components/
        pages/
        services/
        context/
        hooks/
        App.jsx
    public/
    package.json
    README.md

docs/
    architecture/
    diagrams/
    gantt-chart.png

.gitignore
README.md

Modulos do Sistema

Core Features:

Gestao de bots (WhatsApp e Instagram)

Fluxos automatizados

Templates de mensagens

Campanhas omnichannel

Inteligencia artificial para respostas e analise

Dashboard com metricas

Integracoes externas via webhooks e API

Tecnologias Utilizadas

Backend:

Python (FastAPI)

SQLAlchemy

PostgreSQL

Redis

Celery ou RQ

Webhooks + Meta APIs

Frontend:

React (Vite)

Zustand ou Context API

TailwindCSS

Axios

Infra:

Docker e Docker Compose

NGINX

GitHub Actions (CI/CD)

Como Executar o Projeto

Clonar o repositorio:
git clone https://github.com/seu-usuario/smarthub.git

cd smarthub

Criar arquivos .env no backend e frontend

Exemplo Backend .env:
DATABASE_URL=postgresql://user:pass@localhost:5432/smarthub
REDIS_HOST=localhost
META_WHATSAPP_TOKEN=
META_INSTAGRAM_TOKEN=

Subir containers:
docker-compose up --build

Executar manualmente (desenvolvimento)

Backend:
cd backend
uvicorn src.main:app --reload

Frontend:
cd frontend
npm install
npm run dev

Documentação da API

Acesse:
http://localhost:8000/docs

Testes

Backend:
pytest

Frontend:
npm test

Roadmap do MVP

Sprint 01 (MVP):

Setup inicial backend e frontend

CI/CD basico

Autenticacao e CRUD inicial

Conexao com WhatsApp Cloud API

Envio minimo de mensagens

Dashboard inicial

Sprints Futuras:

Conector Instagram

IA para classificacao de mensagens

Automatizacao de fluxos

Modulo de campanhas

Analytics avancado

Marketplace de templates

Licenca

MIT License

Contribuindo

Pull requests sao bem-vindos. Para mudancas maiores, abra uma issue.

Autor

Adriano Augusto de Carvalho Junior
Full-stack Developer | Python | React | IA | Automacao