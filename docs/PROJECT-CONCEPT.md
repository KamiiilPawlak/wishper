# WHISHPER

Aplikacja wykorzystująca lokalne modele AI do automatycznego przetwarzania i analizy nagrań audio. Użytkownik przesyła plik MP3, a system asynchronicznie zamienia nagranie na tekst, analizuje jego zawartość oraz generuje komplet gotowych materiałów do publikacji.

---

## KLUCZOWE CECHY

- **Upload MP3:** Wczytywanie plików dźwiękowych i bezpieczne przechowywanie w obiektowym storage.
- **Transkrypcja (Speech-to-Text):** zamiana mowy na tekst wraz z timestampami (`faster-whisper`).
- **Analiza treści (LLM):**
  - Automatyczne streszczenie nagrania.
  - Podział nagrania na rozdziały z dokładnymi czasami.
  - Propozycje chwytliwych tytułów oraz opisu (SEO/Show Notes).
- **Generowanie napisów:** Automatyczna eksportacja transkrypcji do pliku `.srt`.
- **Asynchroniczne przetwarzanie:** Przetwarzanie długich zadań w tle bez blokowania API.

---

## 🛠️ Stack Technologiczny

### Backend

| Obszar               | Technologia           | Zastosowanie                                                        |
| :------------------- | :-------------------- | :------------------------------------------------------------------ |
| **Framework**        | Python / FastAPI      | Wydajne REST API                                                    |
| **Walidacja**        | Pydantic v2           | Walidacja requestów, response'ów i konfiguracji                     |
| **Baza danych**      | PostgreSQL            | Przechowywanie metadanych, transkrypcji i rozdziałów                |
| **ORM**              | SQLAlchemy 2.0        | Asynchroniczna komunikacja z bazą danych                            |
| **Migracje**         | Alembic               | Zarządzanie schematem bazy danych                                   |
| **File Storage**     | MinIO (S3)            | Przechowywanie plików audio (MP3) oraz wygenerowanych napisów (SRT) |
| **Audio Processing** | FFmpeg                | Analiza, konwersja i przygotowanie plików dźwiękowych               |
| **Speech-to-Text**   | `faster-whisper`      | Zamiana mowy na tekst z timestampami                                |
| **LLM**              | Ollama (`Qwen2.5:3b`) | Generowanie streszczeń, rozdziałów, tytułów i opisów                |
| **Background Jobs**  | Celery                | Kolejkowanie i obsługa zasobożernych zadań AI                       |
| **Message Broker**   | Redis                 | Broker kolejki Celery + przechowywanie stanu zadań                  |
| **Napisy**           | Python                | Dedykowany moduł do generowania plików `.srt`                       |
| **Logging**          | Loguru                | Czytelne i ustrukturyzowane logowanie zdarzeń                       |

### Frontend

| Obszar               | Technologia        | Zastosowanie                                                              |
| :------------------- | :----------------- | :------------------------------------------------------------------------ |
| **UI Framework**     | React + TypeScript | Interaktywny i bezpiecznie typowany interfejs użytkownika                 |
| **State Management** | Zustand            | Lekkie zarządzanie stanem (statusy uploadu, postęp zadań AI, filtrowanie) |
| **UI Components**    | shadcn/ui          | Dostępne i estetyczne komponenty UI (formularze, modale, paski postępu)   |
| **Styling & RWD**    | Tailwind CSS       | Responsywny design (RWD) i szybkie stylizowanie interfejsu                |

### Dev Tools & Jakość Kodu

| Obszar                 | Technologia             | Zastosowanie                                                      |
| :--------------------- | :---------------------- | :---------------------------------------------------------------- |
| **API Docs**           | Swagger / OpenAPI       | Automatyczna i interaktywna dokumentacja API                      |
| **Testy**              | `pytest`                | Testy jednostkowe oraz integracyjne                               |
| **Linter / Formatter** | Ruff                    | Błyskawiczna analiza statyczna i formatowanie kodu                |
| **Type Checking**      | `mypy`                  | Statyczna kontrola typów w Pythonie                               |
| **Konteneryzacja**     | Docker & Docker Compose | Jednolite środowisko uruchomieniowe dla wszystkich usług          |
| **CI/CD**              | GitHub Actions          | Automatyzacja uruchamiania testów i lintera przy każdym commit/PR |

---

## Architektura Przepływu Danych

```text
[Klient / Frontend]
│
│ Upload MP3
▼
[FastAPI Backend] ──Zapis pliku──► [MinIO / S3 Storage]
│
│ Zlecenie zadania
▼
[Redis Broker]
│
▼
[Celery Worker]
│
├─► FFmpeg & faster-whisper  ──► Transkrypcja + Timestampy
│
├─► Ollama (Qwen2.5:3b)       ──► Streszczenie, Rozdziały, Tytuł + Opis
│
└─► Moduł SRT                 ──► Generowanie pliku .srt (Zapis w MinIO)
│
▼
[PostgreSQL DB] (Zapis zagregowanych wyników)

```

---

## Szybkie Uruchomienie (Lokalnie)

### Wymagania wstępne

- [Docker](https://www.docker.com/) oraz Docker Compose
- [Ollama](https://ollama.ai/) uruchomiona lokalnie z pobranym modelem `Qwen2.5:3b`
