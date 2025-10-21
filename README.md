# User API Flask
API REST para gerenciamento de usuários com autenticação JWT, documentação Swagger e PostgreSQL.

## Stack
- Python 3.11+
- Flask 3, SQLAlchemy, Flask-Migrate
- PyJWT / flask-jwt-extended
- Flasgger (Swagger UI)
- PostgreSQL

## Executar com Docker (recomendado)
```bash
cp .env.example .env
docker compose up --build
```
API: http://localhost:5000  |  Swagger: http://localhost:5000/apidocs

## Executar local
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade || true
flask run
```

## Testes
```bash
pytest -q
```

## Endpoints
- POST /auth/register
- POST /auth/login
- GET /users/me (token)
- PUT /users/me  (token)
