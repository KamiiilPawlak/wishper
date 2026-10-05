# Research: Aplikacje Transkrypcji i Analizy Audio (Speech-to-Text + LLM)

Aplikacje wykorzystujące silniki **Speech-to-Text (STT)** — w tym w szczególności OpenAI Whisper — połączone z modelami językowymi (LLM) stały się kluczowym elementem nowoczesnego ekosystemu tworzenia treści, notatek i zarządzania wiedzą.

Poniżej znajduje się analiza rynku, istniejących rozwiązań, ich zalet, wad oraz luk funkcjonalnych.

---

## 1. Przegląd i Kategorie Konkurencyjnych Aplikacji

### A. Podsumowywanie Podcastów i Treści Audio

_Przykłady:_ **Podwise, Snipd, BibiGPT**

- **Zastosowanie:** Pobieranie nagrań z kanałów RSS, YouTube, Spotify lub plików MP3 w celu automatycznej transkrypcji i generowania skrótów.
- **Mocne strony:**
  - **Snipd:** Funkcja _Highlighting on the go_ — wycinanie ostatnich 30 sekund nagrania przyciskiem na słuchawkach z automatyczną transkrypcją i kontekstem.
  - **Podwise / BibiGPT:** Generowanie interaktywnych map myśli (Mind Maps), fiszek oraz bezpośrednia integracja z narzędziami do zarządzania wiedzą (Notion, Obsidian, Readwise).
  - **Chat z nagraniem:** Możliwość zadawania pytań do treści odcinka na podstawie wygenerowanej transkrypcji (RAG).

### B. Asystenci Spotkań i Notatniki Audio

_Przykłady:_ **MacWhisper, Otter.ai, Fireflies.ai, Granola**

- **Zastosowanie:** Nagrywanie spotkań biznesowych (Zoom/Teams/Google Meet) lub dźwięku z mikrofonu/systemu.
- **Mocne strony:**
  - **MacWhisper:** Lokalna aplikacja na macOS wykonująca transkrypcję modelem Whisper bezpośrednio na procesorze użytkownika (100% prywatności, praca offline, brak subskrypcji).
  - **Otter / Fireflies:** Wykrywanie i podział na spikerów (Diarization), automatyczne wyciąganie listy zadań (Action Items) oraz analiza sentymentu.
  - **Granola:** Hybrydowe podejście łączące ręczne notatki użytkownika z pełną transkrypcją AI w celu uzupełnienia luk w notatkach.

### C. Recykling Treści dla Twórców (Content Repurposing)

_Przykłady:_ **Castmagic, Podsqueeze**

- **Zastosowanie:** Przekształcanie jednego pliku audio/video w komplet materiałów marketingowych.
- **Mocne strony:**
  - Dedykowane szablony promptów do generowania postów na LinkedIn, wątków na X (Twitter), newsletterów i wpisów blogowych.
  - Automatyczne wyliczanie dokładnych znaczników czasu (Timestamps) i propozycji nagłówków/tytułów pod SEO.

---

## 2. Kluczowe Zalety i Najlepsze Funkcje (Do Wdrożenia)

1. **Różnorodność Formatów Wyjściowych:**
   - Zamiana surowego tekstu na strukturyzowane formaty: krótkie podsumowanie w punktach, lista zadań do wykonania, mapa myśli, fiszki czy artykuł.
2. **Synchronizacja Tekstu z Odtwarzaczem Audio:**
   - Interaktywny edytor — kliknięcie w dowolne słowo lub zdanie w transkrypcji przenosi odtwarzacz dźwięku bezpośrednio do wybranego momentu.
3. **Prywatność i Przetwarzanie Lokalne (On-Device):**
   - Wykorzystanie zoptymalizowanych silników (`faster-whisper`, `whisper.cpp`) pozwalających na szybką transkrypcję bez wysyłania danych na zewnętrzne serwery.
4. **Interaktywny Chat z Dokumentem Audio:**
   - Zadawanie pytań w czasie rzeczywistym do długich nagrań z automatycznym odsyłaczem do sekundy nagrania (np. _"O której minucie omawiano budżet?"_).
5. **Płynny Eksport do Ekosystemów Notatek:**
   - Jedno-klikowe przesyłanie wygenerowanych materiałów do Notion, Obsidian, Slacka czy Google Docs.

---

## 3. Wady Istniejących Aplikacji i Luki Rynkowe

### A. Główne Wady Obecnych Rozwiązań

- **Wysokie i Powtarzalne Koszty Subskrypcyjne:**
  - Większość rozwiązań chmurowych rozlicza się za minuty nagrań lub wymaga drogich abonamentów ($15–$50/miesięcznie).
- **Halucynacje LLM i Błędy w Żargonie Branżowym:**
  - Sam Whisper radzi sobie dobrze, ale przy specyficznym żargonie (np. nazwy technologii, imiona, terminologia medyczna/prawna) popełnia błędy, które następnie LLM powiela w podsumowaniach.
- **Problemy z Nakładaniem się Głosów (Diarization):**
  - Niska dokładność rozpoznawania spikerów w momencie, gdy uczestnicy rozmowy mówią jednocześnie.
- **Utrata Kontekstu Emocjonalnego:**
  - Transkrypcja konwertuje słowa, ale traci ton wypowiedzi (ironia, priorytet, wahanie, ekspresja).

### B. Luki Rynkowe i Szanse na Wyróżnienie się

1. **Inteligentny Dyktandowy Scribe do Pracy Kreatywnej:**
   - Brak dedykowanych narzędzi radzących sobie z "chaotycznym myśleniem na głos" — przekształcania wielominutowego, niespójnego wywodu w uporządkowaną specyfikację biznesową lub tekst bez utraty intencji.
2. **Lepsza Obsługa Języka Polskiego i Języków Mieszanych (Code-Switching):**
   - Większość globalnych aplikacji słabo radzi sobie z mieszaniem języka polskiego z angielskim żargonem branżowym (np. _"Zrobiliśmy refactor tego endpointu i czekamy na deploy"_).
3. **Personalizowane Szablony Podsumowań (Custom Prompts):**
   - Powszechne jest serwowanie sztywnych, generycznych skrótów. Użytkownicy oczekują możliwości zdefiniowania własnych reguł (np. _"Zawsze wyciągaj tylko decyzje, daty i kwoty"_).
4. **Lokalny i Tani Stack dla Małych Twórców:**
   - Brak otwartych, łatwych w uruchomieniu rozwiązań opartych na lokalnej Ollamie i Whisperze, które pozwalają przetwarzać nieograniczoną liczbę godzin audio bez płacenia dostawcom API.
