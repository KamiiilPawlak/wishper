# Backend Challenges & Architecture Solutions

Przetwarzanie audio i analiza przy użyciu lokalnych modeli AI (`faster-whisper` + `Ollama / Qwen2.5`) niesie ze sobą konkretne wyzwania inżynieryjne. Poniżej znajduje się zestawienie najważniejszych problemów architektonicznych w backendzie oraz rozwiązań zastosowanych w projekcie.

---

## 1. Zarządzanie Zasobami i Wydajnością (VRAM / CPU / RAM)

> **Problem Statement:** _Równoległe przetwarzanie kilku plików audio i jednoczesne uruchamianie modeli `faster-whisper` oraz `Qwen2.5:3b` stwarza wysokie ryzyko wyczerpania pamięci (OOM — Out of Memory) i awarii kontenerów Docker._

### Rozwiązanie:

- **Kolejkowanie i limitowanie współbieżności:** Ustawienie `worker_concurrency = 1` w Celery dla workerów obsługujących zadania AI, co wymusza sekwencyjne przetwarzanie zasobożernych kroków.
- **Optymalizacja kwantyzacji:** Wykorzystanie wariantów `int8` dla `faster-whisper` oraz `q4_k_m` dla Ollamy w celu drastycznego zmniejszenia zapotrzebowania na pamięć VRAM/RAM.
- **Sekwencyjne zwalnianie zasobów:** Pipeline najpierw kończy etap Speech-to-Text, a dopiero po zwolnieniu zasobów przekazuje dane do LLM.

---

## 2. Długo Trwające Zadania w Tle i Przetwarzanie Dużych Plików

> **Problem Statement:** _Procesowanie 1–2 godzinnych plików MP3 powoduje ryzyko zerwania połączeń HTTP (timeout), zablokowania głównego wątku API oraz nadmiernego obciążenia pamięci RAM serwera przy uploadzie._

### Rozwiązanie:

- **Streamowanie do S3 (MinIO):** Odbieranie pliku w FastAPI poprzez strumień (`UploadFile`) i bezpośredni zapis w MinIO bez ładowania całego nagrania do pamięci RAM.
- **Architektura Asynchroniczna:** Endpoint API rejestruje plik, natychmiast zwraca `task_id` ze statusem `ACCEPTED` (202), a całą ciężką pracę przekazuje do Celery.
- **Granularne statusy (Polling):** Przechowywanie postępu prac w Redis (`UPLOADED` $\rightarrow$ `TRANSCRIBING` $\rightarrow$ `SUMMARIZING` $\rightarrow$ `COMPLETED` / `FAILED`), co umożliwia frontendowi precyzyjne informowanie użytkownika o etapie przetwarzania.

---

## 3. Ograniczenia Kontekstu LLM przy Długich Transkrypcjach

> **Problem Statement:** _Transkrypcja wielogodzinnego podcastu może przekraczać 30 000 tokenów. Bezpośrednie przekazanie takiego tekstu do małego modelu lokalnego (`Qwen2.5:3b`) powoduje gubienie faktów, halucynacje lub błędy generowania._

### Rozwiązanie:

- **Hierarchiczny Chunking (Map-Reduce):** Dzielenie transkrypcji na logiczne bloki czasowe (np. bloki 10–15 minutowe), generowanie podsumowań dla każdego bloku z osobna (krok _Map_), a następnie scalanie wyników w ostateczne streszczenie i listę rozdziałów (krok _Reduce_).
- **Wstępny podział w Pythonie:** Przekazywanie do LLM wstępnie pogrupowanych bloków wraz z zebranymi z Whispera znacznikami czasu.

---

## 4. Walidacja i Formatowanie Odpowiedzi LLM (JSON Parsing)

> **Problem Statement:** _Modele LLM bywają niestabilne przy generowaniu strukturyzowanych danych (np. tablicy obiektów z rozdziałami) – ucięte cudzysłowy lub dodatkowy tekst komentarza uniemożliwiają zapis do bazy PostgreSQL._

### Rozwiązanie:

- **Strict JSON Mode:** Wymuszanie odpowiedzi w formacie JSON w konfiguracji zapytań do Ollamy.
- **Walidacja Pydantic v2:** Każda odpowiedź z LLM przechodzi przez ścisłą walidację schematu.
- **Fallback & Auto-retry:** W przypadku błędu parsowania, specjalny moduł naprawczy czyszczący tekst (np. usuwanie znaczników markdown) podejmuje próbę naprawy struktury lub wysyła szybkie zapytanie korygujące do LLM.

---

## 5. Idempotentność i Obsługa Awarii (Fault Tolerance)

> **Problem Statement:** _Awaria workera w trakcie wieloetapowego procesu (np. niespodziewany restart Ollamy) może prowadzić do pozostawienia sierocych plików tymczasowych i spójności danych w bazie._

### Rozwiazanie:

- **Wznowienie od punktu awarii:** Zapisywanie pośrednich wyników (np. surowej transkrypcji) w bazie/MinIO, co pozwala powtórzyć tylko nieudany krok (np. ponowić generowanie opisu bez ponownego uruchamiania transkrypcji Whisperm).
- **Cleanup Handlers:** Automatyczne czyszczenie plików tymczasowych z dysku lokalnego workera w bloku `finally` po zakończeniu zadania.

---

## 📊 Podsumowanie Wyzwań i Rozwiązań

| Challenge                        | Potencjalne ryzyko            | Rozwiązanie w backendzie                            |
| :------------------------------- | :---------------------------- | :-------------------------------------------------- |
| **Brak VRAM / OOM**              | Awaria kontenera Docker       | `worker_concurrency=1`, kwantyzacja `int8`/`q4_k_m` |
| **Przekroczenie okna kontekstu** | Halucynacje, ucięte wyniki    | Chunking (Map-Reduce) i pre-processing w Pythonie   |
| **Błędy w formatowaniu JSON**    | Awaria Pydantic / Błąd bazy   | Strict JSON Mode + auto-retry & repair parser       |
| **Długi czas wykonania**         | Blocking HTTP / Timeout       | Asynchroniczny Celery + Redis + streamowanie do S3  |
| **Przerwanie przetwarzania**     | Sierocze pliki / Błędne stany | Idempotentność etapów + retries + cleanup handlers  |
