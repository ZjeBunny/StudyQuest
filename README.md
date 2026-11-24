# StudyQuest

Polskojęzyczna aplikacja desktopowa wspierająca naukę z lokalną sztuczną inteligencją (Ollama).

## Funkcje

- Rozmowa z AI, tworzenie i analiza notatek, kategorie i wyszukiwanie.
- Tworzenie notatek ze zdjęć i PDF, załączniki w rozmowie.
- Quizy i fiszki na podstawie materiałów, punkty XP i odznaki.
- Sześć motywów, własny kolor główny, wysoki kontrast i rozmiar tekstu 10–24 px.
- Tryb Lightweight oraz wybór modeli tekstowych i obrazowych.
- Wspólna blokada operacji AI i wskaźnik pracy.

## Instalacja ze źródeł

Zalecany Python 3.11 lub 3.12, Windows lub Linux z graficznym środowiskiem. Rozpakuj archiwum i otwórz terminal w katalogu projektu.

```bash
python -m venv .venv
```

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```
Linux:
```bash
source .venv/bin/activate
```
Następnie:
```bash
python -m pip install -r requirements.txt
python src/main.py
```
Na Linuxie polecenie `python` może wymagać zastąpienia przez `python3` przed aktywacją środowiska.

## Ollama

Zainstaluj Ollama z https://ollama.com/download. Aplikacja sprawdza dostępność modeli i oferuje pobranie brakujących. Można też pobrać je ręcznie:

```bash
ollama pull qwen3.5:4b
ollama pull gemma3:4b
ollama pull qwen3:1.7b
```
Ostatni model jest przeznaczony dla opcjonalnego trybu Lightweight. Domyślny adres serwera: `http://localhost:11434`. Jeśli serwer nie działa, uruchom `ollama serve`.

Modele zajmują kilka GB miejsca; wydajność zależy od RAM, procesora i GPU. Przy 8 GB RAM warto wypróbować Lightweight. Analiza obrazów nadal wymaga modelu obrazowego.

## Korzystanie

- **Nauka:** zadaj pytanie, opcjonalnie wybierz notatkę lub załącz plik.
- **Notatki:** twórz kategorie, edytuj materiały lub generuj notatki z plików.
- **Quizy:** wybierz materiał oraz quiz albo fiszki.
- **Moja przygoda:** sprawdzaj postępy.
- **Ustawienia:** wybierz motyw, rozmiar tekstu i modele AI.

PDF: maksymalnie 30 stron; streszczanie i rozmowa z PDF mają limit 12 000 znaków materiału. Skanowane strony bez tekstu są analizowane przez model obrazowy. Renderer obsługuje podstawowy Markdown i część zapisów matematycznych, nie pełny LaTeX. Odpowiedzi AI mogą zawierać błędy.

## Struktura

```text
assets/       grafiki, fonty i ikony SVG
src/app/      główne okno
src/pages/    zakładki
src/ai/       komunikacja z AI
src/services/ ustawienia, modele i zapis danych
src/database/ baza notatek
src/themes/   motywy
src/utils/    renderer Markdown
src/widgets/  komponenty Qt
src/main.py   punkt wejścia
```

Notatki i ustawienia są zapisywane w katalogach użytkownika wskazanych przez Qt. Przy lokalnym serwerze Ollama przetwarzanie modeli odbywa się lokalnie; pobieranie modeli wymaga internetu. Nie usuwaj danych aplikacji bez kopii zapasowej.

## Zależności i dystrybucja

`requirements.txt` zawiera zależności uruchamianej aplikacji. `requirements-dev.txt` zawiera dodatkową zależność nieużywanego modułu eksperymentalnego `ai/agent.py`. Python i Ollama są instalowane osobno.

Archiwum zawiera kod źródłowy, nie gotowy plik EXE. Przed dystrybucją należy dołączyć właściwą licencję projektu oraz informacje licencyjne użytych bibliotek, modeli i zasobów. W tym archiwum nie ma pliku LICENSE.
