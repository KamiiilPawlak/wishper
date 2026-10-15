# Contributing

## Setup

Patrz [docs/getting-started.md](docs/getting-started.md) — instalacja, uruchomienie backendu, bramka jakości lokalnie.

## Konwencja commitów

Projekt używa [Conventional Commits](https://www.conventionalcommits.org/), wymuszane przez `commitlint` (hook `commit-msg` oraz CI na każdym PR). Dozwolone typy: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `revert` (patrz `commitlint.config.js`).

```text
<type>: <krótki opis w czasie teraźniejszym>

feat: add upload endpoint for MP3 recordings
fix: handle empty transcript in summarizer
docs: update architecture overview
```

## Pre-commit hooks

`pre-commit` odpala przy każdym commicie: Ruff (lint + fix), Ruff format, mypy (strict), commitlint. Instalacja: `uv run --directory backend pre-commit install` (patrz getting-started). Nie omijaj hooków (`--no-verify`) — jeśli hook się nie zgadza, napraw kod, nie obchodź bramki.

## Bramka jakości

Każdy PR musi przejść CI (`.github/workflows/ci.yml`):

- `ruff check` i `ruff format --check` — lint i formatowanie.
- `mypy` — statyczne typowanie w trybie `strict`.
- `pytest` — testy jednostkowe/integracyjne.
- `commitlint` — konwencja commitów na zakresie PR.

## Pull Requests

- Branch z `main`, nazwa opisowa (np. `feat/upload-endpoint`).
- PR mały i skupiony na jednej zmianie — łatwiejszy do review.
- Opis PR: co i dlaczego (nie tylko "co" — to widać w diffie).
- Nowa funkcjonalność → testy jednostkowe/integracyjne w tym samym PR.
- Zmiana architektoniczna, trudna do odwrócenia → rozważ dodanie [ADR](docs/architecture/decisions/README.md).

## Dokumentacja

Struktura dokumentacji opisana w [docs/README.md](docs/README.md). W skrócie:

- `docs/product/` — co i dla kogo (nietechniczne).
- `docs/architecture/` — jak i dlaczego, w tym `decisions/` (ADR) dla decyzji trudnych do odwrócenia.
- `docs/features/` — specyfikacje zadań per faza roadmapy.
- `docs/internal/` — robocze notatki, nieśledzone w repo (`.gitignore`).

Dokumentację aktualizuj w tym samym PR co kod, którego dotyczy — nie jako osobny "cleanup" później.
