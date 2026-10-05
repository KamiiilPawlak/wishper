# Technical Overview

## Architecture

- **Pojedyncza aplikacja z podziałem na części.** React SPA komunikuje się z dedykowanym backendem REST API, który zlecenia zasobożerne offloaduje asynchronicznie do workerów zadań w tle.
- **Architektura kontenerowa i lokalny zestaw usług.** Skonteneryzowane środowisko Docker Compose składa się z:
  - `backend` — serwer HTTP FastAPI / Uvicorn serwujący REST API i walidujący dane.
  - `celery_worker` — asynchronizny proces wykonujący ciężkie zadania AI (FFmpeg, `faster-whisper`, integracja z Ollama).
  - `db` — PostgreSQL 16 przechowywający metadane, transkrypcje, rozdziały oraz statusy zadań.
  - `redis` — in-memory broker wiadomości dla Celery oraz backend wyników i śledzenia statusów.
  - `storage` — lokalny emulator S3 (MinIO) do przechowywania plików audio (MP3) oraz wygenerowanych napisów (SRT).
- **Odciążenie LLM przez deterministyczny kod (Python Offloading).** Model LLM nie jest obciążany prostymi operacjami. Wykrywanie języka (`faster-whisper`), generowanie napisów `.srt`, analityka długości/tempu mowy oraz ekstraktory słów kluczowych dzieją się bezpośrednio w Pythonie. LLM (Ollama / Qwen2.5) służy wyłącznie do syntezy wysokiego poziomu (streszczenia, nazwy rozdziałów, propozycje tytułów/opisów).
- **Kolejkowanie z limitowaniem zasobów (GPU/VRAM Safety).** Aby zapobiec błędom OOM (Out of Memory) przy równoległych żądaniach, worker Celery realizujący zadania AI pracuje z rygorystycznym limitem współbieżności (`worker_concurrency = 1`).
- **Asynchroniczny Pipeline i Polling Statusów.** Przesłanie nagrania zwraca natychmiast status `202 Accepted` wraz z `task_id`. Frontend śledzi postęp etapu (`UPLOADED` → `TRANSCRIBING` → `SUMMARIZING` → `COMPLETED`) poprzez dedykowany endpoint statusowy.
- **Kontrakt API jako jedyne źródło prawdy.** FastAPI automatycznie generuje specyfikację OpenAPI (Swagger); frontend wykorzystuje wygenerowane typy i klienta API gwarantując spójność typowania na styku Python–TypeScript.

## Environments

Oba środowiska używają tych samych definicji Dockerfile / Docker Compose; różni je wyłącznie konfiguracja zmiennych środowiskowych.

**Lokalnie — `docker compose up`:**

- Stawia kompletny stack: FastAPI, Celery, Redis, PostgreSQL, MinIO; nie wymaga zewnętrznych usług w chmurze.
- Za obsługę modeli LLM lokalnie odpowiada zainstalowana na hoście instancja Ollamy (`http://host.docker.internal:11434`).
- Wartości techniczne (porty, credentials) zdefiniowane są w `.env.example` oraz `docker-compose.yml`.
- Sekrety i lokalne nadpisania pochodzą z pliku `.env` wykluczonego z repozytorium.
- Ustrukturyzowane logi aplikacji (Loguru) trafiają bezpośrednio na konsolę kontenerów.

## Technology Stack

| Warstwa                    | Wybór                                                                |
| -------------------------- | -------------------------------------------------------------------- |
| Backend Framework          | Python 3.12+, FastAPI, Uvicorn, Pydantic v2                          |
| Baza danych & ORM          | PostgreSQL 16, SQLAlchemy 2.0 (async), migracje Alembic              |
| Kolejka i zadania w tle    | Celery + Redis 7                                                     |
| Object Storage             | MinIO (S3 API) — przechowywanie plików audio MP3 i napisów SRT       |
| Speech-to-Text (STT)       | `faster-whisper` (z kwantyzacją `int8` i Silero VAD)                 |
| Large Language Model (LLM) | Ollama (`Qwen2.5:3b`), odpytywana w trybie Strict JSON Mode          |
| Audio & Text Utilities     | FFmpeg, `pysrt`, `mutagen`, `KeyBERT`                                |
| Logging                    | Loguru (ustrukturyzowane, kolorowe logi i śledzenie kontekstu)       |
| Frontend                   | React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui                  |
| Stan i dane                | TanStack Query (odpytywanie API), Zustand (stan lokalny/odtwarzacza) |
| Orkiestracja & Kontenery   | Docker & Docker Compose                                              |
| Jakość i Formatowanie      | Ruff (linter/formatter), `mypy` (statyczne typowanie), `pytest`      |

## Quality and Testing

**Bramka jakości i statyczna analiza kodu:**

- **Ruff:** Błyskawiczny linter i formatter kodu Python zastępujący Flake8, Black i isort.
- **mypy:** Rygorystyczna statyczna kontrola typów w całym projekcie backendowym.
- **Loguru:** Jednolite, czytelne logowanie zdarzeń błędu i przepływu danych.

**Piramida testów:**

| Poziom                     | Narzędzie                                                                                      |
| -------------------------- | ---------------------------------------------------------------------------------------------- |
| Testy jednostkowe backendu | `pytest` + `pytest-asyncio` (testy logiki biznesowej, generatora `.srt`, walidatorów Pydantic) |
| Testy integracyjne API     | `pytest` z `httpx.AsyncClient` testujące endpointy FastAPI w izolowanym środowisku             |
| Testy frontendu            | Vitest + React Testing Library                                                                 |

## Cross-Cutting Concerns

- **Konfiguracja przez zmienne środowiskowe.** Wszystkie ścieżki, dane dostępowe do bazy, parametry MinIO, adres Ollamy oraz limity czasowe zdefiniowane są w Pydantic `BaseSettings`.
- **Zarządzanie czasem i retries.** Długie zapytania do LLM oraz transkrypcji wyposażone są w mechanizm automatycznego ponawiania próby (Retry with exponential backoff) na poziomie zadań Celery.
- **Walidacja struktur wyjściowych z LLM.** Wyniki zwracane przez Ollamę są weryfikowane przez schematy Pydantic. W przypadku uszkodzonego JSON-a, moduł _Fallback & Repair_ czyści odpowiedź przed zgłoszeniem błędu.
- **Czyszczenie plików tymczasowych (Cleanup Handlers).** Pliki audio przetwarzane lokalnie w kontenerze workera są bezwzględnie usuwane w bloku `finally` po przesłaniu ich do MinIO lub zakończeniu zadania.
- **Brak wycieku sekretów.** Domyślne wartości w `.env.example` służą wyłącznie do lokalnego uruchomienia w Dockerze; produkcyjne sekrety muszą być przekazywane przez zmienne środowiskowe systemu.

## Consciously Omitted

Pominięte względem skomplikowanych architektur enterprise — świadome decyzje na rzecz wydajności, prostoty i pracy lokalnej:

| Pominięte                                                                               | Zamiast tego                                                      |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Przetwarzanie transkrypcji przez zewnętrzne płatne API (OpenAI Whisper API, AssemblyAI) | Lokalny `faster-whisper` uruchamiany w workerze Celery            |
| Przekazywanie całego tekstu do LLM (zastosowanie głośnego promptowania)                 | Offloading w Pythonie (język, SRT, statystyki) + chunking dla LLM |
| Zewnętrzny chmurowy LLM (GPT-4 / Claude)                                                | Lokalna Ollama z modelem `Qwen2.5:3b`                             |
| Komunikacja w czasie rzeczywistym przez WebSockety na starcie                           | Prosty i niezawodny Polling stanu zadania po `task_id`            |
| Skomplikowane mikrousługi                                                               | Modułowy monolith oparty o FastAPI + Celery worker                |
| Szyfrowanie kolumnowe w bazie danych                                                    | Standardowe zabezpieczenia PostgreSQL i izolacja w kontenerach    |
