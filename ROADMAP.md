# Roadmap

## Faza 1 — Quality Tools, Konteneryzacja i CI/CD

- [ ] [PF1](docs/features/phase-1/pf1-szkielet-i-docker.md) — Szkielet aplikacji: Docker & Docker Compose dla FastAPI, Celery, Redis, PostgreSQL.
- [ ] [PF2](docs/features/phase-1/pf2-bramka-jakosci-i-ci.md) — Bramka jakości: konfiguracja Ruff, mypy, pytest, Loguru oraz GitHub Actions (CI/CD).

## Faza 2 — Backend, Baza Danych i AI Pipeline

- [ ] [PF3](docs/features/phase-2/pf3-szkielet-fastapi-i-healthcheck.md) — Szkielet FastAPI + Uvicorn: uruchomienie serwera API, konfiguracja Pydantic v2 oraz endpointy healthcheck (`/health`).
- [ ] [PF4](docs/features/phase-2/PF4-baza-danych-i-storage.md) — Baza danych i Storage: podpięcie PostgreSQL (SQLAlchemy 2.0 + Alembic) oraz lokalnego storage plików (filesystem) do zapisywania plików MP3.
- [ ] [PF5](docs/features/phase-2/PF5-kolejka-celery-redis.md) — Kolejka i obsługa zadań: integracja Celery + Redis oraz obróbka audio w FFmpeg.
- [ ] [PF6](docs/features/phase-2/PF6-stt-i-odciazenie-llm.md) — Transkrypcja i Analiza NLP: integracja `faster-whisper`, detekcja języka i generowanie napisów `.srt` w Pythonie.
- [ ] [PF7](docs/features/phase-2/PF7-llm-pipeline.md) — Pipeline Heurystyczny NLP (bez LLM): ekstrakcyjne streszczenie (`sumy`), detekcja rozdziałów przez embeddingi (`sentence-transformers`) oraz tytuł/opis na bazie słów kluczowych (`KeyBERT`) — w pełni na CPU.
- [ ] [PF8](docs/features/phase-2/PF8-api-podcastow.md) — REST API Podcastów: pełne endpointy do przesyłania audio, uruchamiania procesu i pobierania wyników (JSON + SRT).
- [ ] [PF9](docs/features/phase-2/PF9-statusy-i-dokumentacja.md) — Śledzenie statusów i Dokumentacja: endpointy sprawdzania postępu zadań oraz ostateczna dokumentacja Swagger/OpenAPI.

## Faza 3 — Frontend i UX

Praca równoległa:

- [ ] [PF10](docs/features/phase-3/PF10-szkielet-frontend.md) — Szkielet UI: konfiguracja React, TypeScript, Tailwind CSS (RWD) oraz komponentów shadcn/ui.
- [ ] [PF11](docs/features/phase-3/PF11-state-management.md) — Zarządzanie stanem: magazyny Zustand do obsługi uploadu, stanu odtwarzacza i filtrowania.
- [ ] [PF12](docs/features/phase-3/PF12-upload-i-dashboard.md) — Widok Uploadu i Dashboard: formularz wysyłania MP3 z paskiem postępu oraz lista przetworzonych podcastów.
- [ ] [PF13](docs/features/phase-3/PF13-odtwarzacz-i-podglad.md) — Odtwarzacz i Detale Podcastu: podgląd transkrypcji, interaktywne rozdziały z przeskakiwaniem audio, streszczenie oraz kopiowanie opisu.
- [ ] [PF14](docs/features/phase-3/PF14-pobieranie-napisow.md) — Eksport danych: pobieranie plików `.srt` oraz eksport treści do gotowych szablonów.
