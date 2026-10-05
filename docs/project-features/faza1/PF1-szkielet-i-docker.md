# PF1-szkielet-i-docker

## 📌 Opis zadania

Celem tego zadania jest stworzenie bazowego szkieletu repozytorium oraz skonfigurowanie środowiska Docker Compose. Po zakończeniu prac cały stos technologiczny (FastAPI, Celery Worker, Redis, PostgreSQL, MinIO) powinien uruchamiać się za pomocą jednego polecenia CLI i być gotowy do rozbudowy o kolejne funkcjonalności.

---

## 🎯 Kryteria Akceptacji (Acceptance Criteria)

1. **Struktura repozytorium:** Stworzona czytelna i modularna struktura katalogów dla backendu i frontendu.
2. **Plik `docker-compose.yml`:** Zdefiniowane i połączone kontenerowe usługi:
   - `backend` (FastAPI / Uvicorn)
   - `celery_worker` (Celery background worker)
   - `db` (PostgreSQL 16)
   - `redis` (Redis 7 - broker & result backend)
   - `storage` (MinIO - S3 Object Storage)
3. **Plik `.env.example`:** Zawiera wszystkie wymagane zmienne środowiskowe dla usług (porty, credentials, dsn-y).
4. **Healthcheck usługi:** Przeglądarka / curl pod adresem `http://localhost:8000/health` zwraca status `200 OK`.
5. **Dostępność konsoli MinIO:** Dostępny panel administracyjny MinIO pod adresem `http://localhost:9001`.

---

## 📁 Proponowana Struktura Projektu

```text
wishper/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
├── ROADMAP.md
├── docs/
│   └── project-features/
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       └── main.py
└── frontend/
    └── Dockerfile
```
