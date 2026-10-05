# Roadmap

## Faza 1 — Quality Tools, Konteneryzacja i CI/CD

- [ ] [PF1](docs/project-features/faza1/PF1-szkielet-i-docker.md) — Szkielet aplikacji: Docker & Docker Compose dla FastAPI, Celery, Redis, PostgreSQL, MinIO.
- [ ] [PF2](docs/project-features/faza1/PF2-bramka-jakosci-i-ci.md) — Bramka jakości: konfiguracja Ruff, mypy, pytest, Loguru oraz GitHub Actions (CI/CD).

## Faza 2 — Backend, Baza Danych i AI Pipeline

- [ ] [PF3](docs/project-features/faza2/PF3-szkielet-fastapi-i-healthcheck.md) — Szkielet FastAPI + Uvicorn: uruchomienie serwera API, konfiguracja Pydantic v2 oraz endpointy healthcheck (`/health`).
- [ ] [PF4](project-features/PF4-baza-danych-i-storage.md) — Baza danych i Storage: podpięcie PostgreSQL (SQLAlchemy 2.0 + Alembic) oraz MinIO/S3 do zapisywania plików MP3.
- [ ] [PF5](project-features/PF5-kolejka-celery-redis.md) — Kolejka i obsługa zadań: integracja Celery + Redis oraz obróbka audio w FFmpeg.
- [ ] [PF6](project-features/PF6-stt-i-odciazenie-llm.md) — Transkrypcja i Odciążenie LLM: integracja `faster-whisper`, detekcja języka i generowanie napisów `.srt` w Pythonie.
- [ ] [PF7](project-features/PF7-llm-pipeline.md) — Pipeline LLM (Ollama): podpięcie Qwen2.5:3b do generowania streszczeń, rozdziałów oraz tytułu i opisu.
- [ ] [PF8](project-features/PF8-api-podcastow.md) — REST API Podcastów: pełne endpointy do przesyłania audio, uruchamiania procesu i pobierania wyników (JSON + SRT).
- [ ] [PF9](project-features/PF9-statusy-i-dokumentacja.md) — Śledzenie statusów i Dokumentacja: endpointy sprawdzania postępu zadań oraz ostateczna dokumentacja Swagger/OpenAPI.

## Faza 3 — Frontend i UX

Praca równoległa:

- [ ] [PF10](project-features/PF10-szkielet-frontend.md) — Szkielet UI: konfiguracja React, TypeScript, Tailwind CSS (RWD) oraz komponentów shadcn/ui.
- [ ] [PF11](project-features/PF11-state-management.md) — Zarządzanie stanem: magazyny Zustand do obsługi uploadu, stanu odtwarzacza i filtrowania.
- [ ] [PF12](project-features/PF12-upload-i-dashboard.md) — Widok Uploadu i Dashboard: formularz wysyłania MP3 z paskiem postępu oraz lista przetworzonych podcastów.
- [ ] [PF13](project-features/PF13-odtwarzacz-i-podglad.md) — Odtwarzacz i Detale Podcastu: podgląd transkrypcji, interaktywne rozdziały z przeskakiwaniem audio, streszczenie oraz kopiowanie opisu.
- [ ] [PF14](project-features/PF14-pobieranie-napisow.md) — Eksport danych: pobieranie plików `.srt` oraz eksport treści do gotowych szablonów.
