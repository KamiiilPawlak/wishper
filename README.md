<p align="center">
  <img src="./wishpher-logo.png" alt="Wishpher Logo" width="220" />
</p>

<h1 align="center">Wishpher</h1>

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

System działa w oparciu o lokalne modele AI (`faster-whisper` oraz `Ollama / Qwen2.5`), co gwarantuje pełną prywatność danych, brak opłat za API oraz nieograniczone możliwości przetwarzania.

---

## Funkcje

- 🎙️ **Upload MP3:** Przesyłanie nagrań i bezpieczne przechowywanie w chmurze obiektowej (MinIO/S3).
- 📝 **Transkrypcja (STT):** Zamiana mowy na tekst z dokładnymi znacznikami czasu (`faster-whisper`).
- 🤖 **Analiza LLM (Qwen2.5):** Automatyczne generowanie streszczenia, podziału na rozdziały oraz propozycji tytułu i opisu (Show Notes).
- 🎬 **Automatyczne napisy:** Generowanie gotowych plików `.srt` bez angażowania LLM.
- ⚡ **Asynchroniczne przetwarzanie:** Długie zadania wykonywane w tle (Celery + Redis) bez blokowania interfejsu.

---

## 🛠️ Stack Technologiczny

| Obszar                   | Technologie                                         |
| :----------------------- | :-------------------------------------------------- |
| **Backend**              | Python, FastAPI, Pydantic v2, Loguru                |
| **Baza & Storage**       | PostgreSQL, SQLAlchemy 2.0, Alembic, MinIO (S3)     |
| **Kolejka & Pracownicy** | Celery, Redis                                       |
| **Przetwarzanie AI**     | `faster-whisper`, Ollama (`Qwen2.5:3b`), FFmpeg     |
| **Frontend**             | React, TypeScript, Zustand, shadcn/ui, Tailwind CSS |
| **Narzędzia & Jakość**   | Docker Compose, pytest, Ruff, mypy, GitHub Actions  |

---

## 🗺️ Roadmapa

Szczegółowa specyfikacja techniczna oraz etapy wdrażania poszczególnych funkcji znajdują się w pliku [ROADMAP.md](./ROADMAP.md).
