# Technical Overview

## Architecture

- **Pojedyncza aplikacja z podziałem na części.** React SPA komunikuje się z dedykowanym backendem REST API, który zlecenia zasobożerne offloaduje asynchronicznie do workerów zadań w tle.
- **Architektura kontenerowa i lokalny zestaw usług.** Skonteneryzowane środowisko Docker Compose składa się z:
  - `backend` — serwer HTTP FastAPI / Uvicorn serwujący REST API i walidujący dane.
  - `celery_worker` — asynchronizny proces wykonujący ciężkie zadania AI (FFmpeg, `faster-whisper`, ekstrakcyjna analiza NLP: `sumy`, `KeyBERT`, `sentence-transformers`).
  - `db` — PostgreSQL 16 przechowywający metadane, transkrypcje, rozdziały oraz statusy zadań.
  - `redis` — in-memory broker wiadomości dla Celery oraz backend wyników i śledzenia statusów.
  - `storage` — lokalny emulator S3 (MinIO) do przechowywania plików audio (MP3) oraz wygenerowanych napisów (SRT).
- **Brak LLM — w pełni deterministyczny pipeline NLP (CPU-only).** Cała analiza treści działa na lekkich, ekstrakcyjnych modelach NLP zamiast modelu generatywnego: wykrywanie języka i transkrypcja (`faster-whisper`), ekstrakcyjne streszczenie (`sumy`), detekcja rozdziałów poprzez porównanie embeddingów sąsiednich bloków tekstu (`sentence-transformers`, np. `all-MiniLM-L6-v2`) oraz słowa kluczowe do tytułu/opisu (`KeyBERT`). Umożliwia to pracę bez GPU na zwykłym CPU (np. laptop z i5 8. generacji) i eliminuje koszty oraz niedeterminizm LLM.
- **Kolejkowanie z limitowaniem zasobów (CPU/RAM Safety).** Aby zapobiec przeciążeniu CPU/RAM przy równoległych żądaniach, worker Celery realizujący zadania AI pracuje z rygorystycznym limitem współbieżności (`worker_concurrency = 1`).
- **Asynchroniczny Pipeline i Polling Statusów.** Przesłanie nagrania zwraca natychmiast status `202 Accepted` wraz z `task_id`. Frontend śledzi postęp etapu (`UPLOADED` → `TRANSCRIBING` → `SUMMARIZING` → `COMPLETED`) poprzez dedykowany endpoint statusowy.
- **Kontrakt API jako jedyne źródło prawdy.** FastAPI automatycznie generuje specyfikację OpenAPI (Swagger); frontend wykorzystuje wygenerowane typy i klienta API gwarantując spójność typowania na styku Python–TypeScript.

## Environments

Oba środowiska używają tych samych definicji Dockerfile / Docker Compose; różni je wyłącznie konfiguracja zmiennych środowiskowych.

**Lokalnie — `docker compose up`:**

- Stawia kompletny stack: FastAPI, Celery, Redis, PostgreSQL, MinIO; nie wymaga zewnętrznych usług w chmurze ani GPU.
- Wszystkie modele AI (`faster-whisper`, `sentence-transformers`) ładowane są bezpośrednio w kontenerze `celery_worker` i działają na CPU.
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
| Analiza treści (NLP)       | `sumy` (streszczenie ekstrakcyjne), `sentence-transformers` (rozdziały), `KeyBERT` (słowa kluczowe) — bez LLM, CPU-only |
| Audio & Text Utilities     | FFmpeg, `pysrt`, `mutagen`                                           |
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

- **Konfiguracja przez zmienne środowiskowe.** Wszystkie ścieżki, dane dostępowe do bazy, parametry MinIO oraz limity czasowe zdefiniowane są w Pydantic `BaseSettings`.
- **Zarządzanie czasem i retries.** Długotrwałe operacje (transkrypcja, generowanie embeddingów) wyposażone są w mechanizm automatycznego ponawiania próby (Retry with exponential backoff) na poziomie zadań Celery.
- **Walidacja struktur wyjściowych NLP.** Wyniki ekstrakcyjnej analizy (rozdziały, słowa kluczowe, streszczenie) są weryfikowane przez schematy Pydantic przed zapisem do bazy.
- **Czyszczenie plików tymczasowych (Cleanup Handlers).** Pliki audio przetwarzane lokalnie w kontenerze workera są bezwzględnie usuwane w bloku `finally` po przesłaniu ich do MinIO lub zakończeniu zadania.
- **Brak wycieku sekretów.** Domyślne wartości w `.env.example` służą wyłącznie do lokalnego uruchomienia w Dockerze; produkcyjne sekrety muszą być przekazywane przez zmienne środowiskowe systemu.

## Consciously Omitted

Pominięte względem skomplikowanych architektur enterprise — świadome decyzje na rzecz wydajności, prostoty i pracy lokalnej:

| Pominięte                                                                               | Zamiast tego                                                      |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Przetwarzanie transkrypcji przez zewnętrzne płatne API (OpenAI Whisper API, AssemblyAI) | Lokalny `faster-whisper` uruchamiany w workerze Celery            |
| Jakikolwiek model LLM (lokalny lub chmurowy, np. Ollama/Qwen, GPT-4, Claude)            | Deterministyczne, ekstrakcyjne NLP (`sumy`, `KeyBERT`, `sentence-transformers`) działające w pełni na CPU |
| Komunikacja w czasie rzeczywistym przez WebSockety na starcie                           | Prosty i niezawodny Polling stanu zadania po `task_id`            |
| Skomplikowane mikrousługi                                                               | Modułowy monolith oparty o FastAPI + Celery worker                |
| Szyfrowanie kolumnowe w bazie danych                                                    | Standardowe zabezpieczenia PostgreSQL i izolacja w kontenerach    |
