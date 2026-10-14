# Backend Challenges & Architecture Solutions

Przetwarzanie audio i analiza przy użyciu lokalnych modeli AI (`faster-whisper` + heurystyki NLP: `sumy`, `KeyBERT`, `sentence-transformers`) niesie ze sobą konkretne wyzwania inżynieryjne — mimo braku LLM i pracy w pełni na CPU. Poniżej znajduje się zestawienie najważniejszych problemów architektonicznych w backendzie oraz rozwiązań zastosowanych w projekcie.

---

## 1. Zarządzanie Zasobami i Wydajnością (CPU / RAM, brak GPU)

> **Problem Statement:** _Aplikacja musi działać na słabszym sprzęcie bez karty graficznej (np. laptop z CPU Intel i5 8. generacji). Równoległe przetwarzanie kilku plików audio modelem `faster-whisper` oraz liczenie embeddingów (`sentence-transformers`) w tym samym czasie stwarza ryzyko nadmiernego obciążenia CPU/RAM i bardzo długiego czasu przetwarzania._

### Rozwiązanie:

- **Kolejkowanie i limitowanie współbieżności:** Ustawienie `worker_concurrency = 1` w Celery dla workerów obsługujących zadania AI, co wymusza sekwencyjne przetwarzanie zasobożernych kroków.
- **Optymalizacja kwantyzacji:** Wykorzystanie wariantu `int8` dla `faster-whisper` oraz lekkiego modelu `all-MiniLM-L6-v2` dla `sentence-transformers`, co drastycznie zmniejsza zapotrzebowanie na pamięć RAM i czas obliczeń na CPU.
- **Sekwencyjne zwalnianie zasobów:** Pipeline najpierw kończy etap Speech-to-Text, a dopiero po zwolnieniu zasobów przechodzi do etapu analizy NLP.

---

## 2. Długo Trwające Zadania w Tle i Przetwarzanie Dużych Plików

> **Problem Statement:** _Procesowanie 1–2 godzinnych plików MP3 powoduje ryzyko zerwania połączeń HTTP (timeout), zablokowania głównego wątku API oraz nadmiernego obciążenia pamięci RAM serwera przy uploadzie._

### Rozwiązanie:

- **Streamowanie do S3 (MinIO):** Odbieranie pliku w FastAPI poprzez strumień (`UploadFile`) i bezpośredni zapis w MinIO bez ładowania całego nagrania do pamięci RAM.
- **Architektura Asynchroniczna:** Endpoint API rejestruje plik, natychmiast zwraca `task_id` ze statusem `ACCEPTED` (202), a całą ciężką pracę przekazuje do Celery.
- **Granularne statusy (Polling):** Przechowywanie postępu prac w Redis (`UPLOADED` $\rightarrow$ `TRANSCRIBING` $\rightarrow$ `SUMMARIZING` $\rightarrow$ `COMPLETED` / `FAILED`), co umożliwia frontendowi precyzyjne informowanie użytkownika o etapie przetwarzania.

---

## 3. Wydajność Analizy NLP przy Długich Transkrypcjach

> **Problem Statement:** _Transkrypcja wielogodzinnego podcastu to tysiące zdań. Liczenie embeddingów (`sentence-transformers`) dla każdego zdania z osobna oraz ekstrakcyjne streszczanie (`sumy`) całego tekstu na raz jest nieefektywne na CPU i zużywa dużo RAM._

### Rozwiązanie:

- **Chunking czasowy:** Dzielenie transkrypcji na logiczne bloki czasowe (np. 10–15 minutowe) z wykorzystaniem timestampów z Whishpera, co pozwala przetwarzać embeddingi i streszczenie blokami w batchach, a nie dla całego tekstu naraz.
- **Detekcja rozdziałów przez spadek podobieństwa:** Porównywanie embeddingów sąsiednich bloków (cosine similarity) — lokalne minimum podobieństwa oznacza granicę rozdziału, bez potrzeby analizy całego dokumentu jednocześnie.

---

## 4. Jakość Ekstrakcyjnych Heurystyk NLP (brak halucynacji, ale ryzyko złej ekstrakcji)

> **Problem Statement:** _W przeciwieństwie do LLM, metody ekstrakcyjne (`sumy`, `KeyBERT`) nie halucynują, ale mogą wybrać nietrafione zdania do streszczenia lub nieistotne słowa kluczowe, zwłaszcza przy krótkich lub silnie potocznych nagraniach._

### Rozwiązanie:

- **Walidacja Pydantic v2:** Każdy wynik analizy (streszczenie, lista rozdziałów, słowa kluczowe) przechodzi przez ścisłą walidację schematu przed zapisem do bazy.
- **Progi i limity konfigurowalne:** Minimalna/maksymalna liczba zdań w streszczeniu oraz liczba słów kluczowych są parametrami konfiguracyjnymi, dostrajanymi pod typ nagrania.
- **Stoplisty językowe:** Zastosowanie list stopwords i słowników specyficznych dla języka polskiego oraz mieszanego (code-switching PL/EN) w `KeyBERT`, aby uniknąć ekstrakcji nieistotnych fragmentów.

---

## 5. Idempotentność i Obsługa Awarii (Fault Tolerance)

> **Problem Statement:** _Awaria workera w trakcie wieloetapowego procesu (np. niespodziewany restart kontenera `celery_worker`) może prowadzić do pozostawienia sierocych plików tymczasowych i niespójności danych w bazie._

### Rozwiazanie:

- **Wznowienie od punktu awarii:** Zapisywanie pośrednich wyników (np. surowej transkrypcji) w bazie/MinIO, co pozwala powtórzyć tylko nieudany krok (np. ponowić analizę NLP bez ponownego uruchamiania transkrypcji Whisperem).
- **Cleanup Handlers:** Automatyczne czyszczenie plików tymczasowych z dysku lokalnego workera w bloku `finally` po zakończeniu zadania.

---

## 📊 Podsumowanie Wyzwań i Rozwiązań

| Challenge                        | Potencjalne ryzyko            | Rozwiązanie w backendzie                             |
| :------------------------------- | :----------------------------- | :---------------------------------------------------- |
| **Brak GPU, słabe CPU**          | Bardzo długi czas przetwarzania | `worker_concurrency=1`, kwantyzacja `int8`, lekki `MiniLM` |
| **Długie transkrypcje**          | Wysokie zużycie RAM na embeddingi | Chunking czasowy i batchowanie NLP w Pythonie        |
| **Słaba jakość ekstrakcji**      | Nietrafione streszczenie/słowa kluczowe | Konfigurowalne progi + stoplisty językowe PL/EN |
| **Długi czas wykonania**         | Blocking HTTP / Timeout        | Asynchroniczny Celery + Redis + streamowanie do S3    |
| **Przerwanie przetwarzania**     | Sierocze pliki / Błędne stany  | Idempotentność etapów + retries + cleanup handlers    |
