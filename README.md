<p align="center">
  <img src="./wishpher-logo.png" alt="Wishpher Logo" width="220" />
</p>

<h1 align="center">Wishper</h1>

<p align="center">
  <strong>Automatyczne przetwarzanie, transkrypcja i analiza nagrań audio przy użyciu lokalnych modeli AI.</strong>
</p>

<p align="center">
  <a href="#-o-projekcie">O projekcie</a> •
  <a href="#-kluczowe-funkcje">Funkcje</a> •
  <a href="#%EF%B8%8F-stack-technologiczny">Stack</a> •
  <a href="#-roadmapa">Roadmapa</a>
</p>

---

## 💡 O projekcie

aplikacja służąca do automatycznej zamiany nagrań audio (MP3) na tekst, ich głębokiej analizy oraz tworzenia gotowych materiałów do publikacji.

System działa w oparciu o lokalne modele AI (`faster-whisper`) oraz lekkie heurystyki NLP (`sumy`, `KeyBERT`, `sentence-transformers`), co gwarantuje pełną prywatność danych, brak opłat za API, pracę bez karty graficznej oraz nieograniczone możliwości przetwarzania.

---

## Funkcje

- 🎙️ **Upload MP3:** Przesyłanie nagrań i bezpieczne przechowywanie na lokalnym storage (filesystem).
- 📝 **Transkrypcja (STT):** Zamiana mowy na tekst z dokładnymi znacznikami czasu (`faster-whisper`).
- 🧮 **Analiza heurystyczna (NLP):** Automatyczne generowanie streszczenia (`sumy`), podziału na rozdziały (`sentence-transformers`) oraz propozycji tytułu i opisu na bazie słów kluczowych (`KeyBERT`) — bez LLM, w pełni na CPU.
- 🎬 **Automatyczne napisy:** Generowanie gotowych plików `.srt` bez angażowania modeli AI.
- ⚡ **Asynchroniczne przetwarzanie:** Długie zadania wykonywane w tle (Celery + Redis) bez blokowania interfejsu.

---

## 🛠️ Stack Technologiczny

| Obszar                   | Technologie                                                          |
| :----------------------- | :------------------------------------------------------------------- |
| **Backend**              | Python, FastAPI, Pydantic v2, Structlog                              |
| **Baza & Storage**       | PostgreSQL, SQLAlchemy 2.0, Alembic, lokalny storage plików          |
| **Kolejka & Pracownicy** | Celery, Redis                                                        |
| **Przetwarzanie AI**     | `faster-whisper`, `sumy`, `KeyBERT`, `sentence-transformers`, FFmpeg |
| **Frontend**             | React, TypeScript, Zustand, shadcn/ui, Tailwind CSS                  |
| **Narzędzia & Jakość**   | Docker Compose, pytest, Ruff, mypy, GitHub Actions                   |

---

## 🗺️ Roadmapa

Szczegółowa specyfikacja techniczna oraz etapy wdrażania poszczególnych funkcji znajdują się w pliku [ROADMAP.md](./ROADMAP.md).

## 📚 Dokumentacja

Pełna dokumentacja projektu (architektura, koncepcja produktu, specyfikacje zadań) znajduje się w [docs/](./docs/README.md). Zasady współpracy — [CONTRIBUTING.md](./CONTRIBUTING.md). Historia zmian — [CHANGELOG.md](./CHANGELOG.md).
