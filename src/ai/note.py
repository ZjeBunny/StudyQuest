import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class NoteAI:
    def __init__(self, base_url="http://localhost:11434", model="qwen3.5:4b"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def _chat(self, messages, images=None, model=None, timeout=180):
        payload = {
            "model": model or self.model,
            "messages": messages,
            "stream": False
        }
        if images:
            payload["messages"][-1]["images"] = images
        request = Request(
            self.base_url + "/api/chat",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result.get("message", {}).get("content", "")

    def analyze_note(self, title, text):
        prompt = (
            "Przeanalizuj notatkę ucznia po polsku. Wykryj błędy językowe, "
            "niejasności i możliwe błędy merytoryczne. Nie wymyślaj faktów. "
            "Oddziel: BŁĘDY JĘZYKOWE, UWAGI MERYTORYCZNE, PROPOZYCJE. "
            "Na końcu podaj poprawioną wersję tekstu, ale wyraźnie zaznacz, "
            "że użytkownik sam decyduje, czy ją zastosować. Jeśli nie ma błędów, "
            "napisz to wprost. Tytuł: " + title + "\n\nNOTATKA:\n" + text
        )
        return self._chat([{"role": "user", "content": prompt}])

    def generate_quiz(self, title, text, count=8):
        prompt = (
            'Na podstawie materiału przygotuj quiz po polsku. Zwróć WYŁĄCZNIE '
            'JSON w formacie: {"questions":[{"question":"tekst",'
            '"answers":["A","B","C","D"],"correct":0,"explanation":"wyjaśnienie"}]}. '
            'Indeks correct jest od 0 do 3. Każde pytanie ma mieć dokładnie '
            '4 odpowiedzi i jedną poprawną. Nie twórz pytań spoza materiału. '
            'Liczba pytań: ' + str(max(1, min(int(count), 20)))
            + '. Tytuł: ' + title + '\nMATERIAŁ:\n' + text
        )
        raw = self._chat([{"role": "user", "content": prompt}])
        return self._parse_json(raw, "questions")

    def generate_flashcards(self, title, text, count=12):
        prompt = (
            'Utwórz fiszki językowe/pojęciowe na podstawie materiału. Zwróć '
            'WYŁĄCZNIE JSON: {"cards":[{"front":"hasło lub pytanie",'
            '"back":"odpowiedź"}]}. Jedna konkretna informacja na fiszkę. '
            'Nie dopowiadaj faktów spoza materiału. Liczba: '
            + str(max(1, min(int(count), 30))) + '. Tytuł: ' + title
            + '\nMATERIAŁ:\n' + text
        )
        raw = self._chat([{"role": "user", "content": prompt}])
        return self._parse_json(raw, "cards")

    @staticmethod
    def _parse_json(raw, key):
        cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.I).strip()
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end < start:
            raise ValueError("Model nie zwrócił poprawnego JSON.")
        data = json.loads(cleaned[start:end + 1])
        items = data.get(key)
        if not isinstance(items, list) or not items:
            raise ValueError("Model nie wygenerował elementów.")
        return items

    def read_image(self, path):
        import base64
        with open(path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode("ascii")
        return self._chat(
            [{"role": "user", "content": "Odczytaj zawartość obrazu. Zachowaj wzory, tabele i kolejność. Nie zgaduj nieczytelnych fragmentów."}],
            images=[encoded],
            model="gemma3:4b",
            timeout=240
        )

    def read_pdf(self, path):
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("Do odczytu PDF zainstaluj pakiet pypdf.") from exc
        reader = PdfReader(path)
        pages = [(page.extract_text() or "") for page in reader.pages]
        text = "\n\n".join(
            f"[Strona {index + 1}]\n{content}"
            for index, content in enumerate(pages)
        ).strip()
        if not text:
            raise RuntimeError("PDF nie zawiera warstwy tekstowej. Dla skanów użyj importu jako obrazu/OCR.")
        return text

    def search_web(self, query):
        from urllib.parse import quote
        url = "https://html.duckduckgo.com/html/?q=" + quote(query)
        request = Request(url, headers={"User-Agent": "StudyQuest/1.0"})
        with urlopen(request, timeout=20) as response:
            html = response.read().decode("utf-8", errors="replace")
        from html.parser import HTMLParser

        class ResultParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.results = []
                self.capture = False
                self.current = ""
                self.href = ""

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "a" and "result__a" in attrs.get("class", ""):
                    self.capture = True
                    self.current = ""
                    self.href = attrs.get("href", "")

            def handle_data(self, data):
                if self.capture:
                    self.current += data

            def handle_endtag(self, tag):
                if tag == "a" and self.capture:
                    self.results.append((self.current.strip(), self.href))
                    self.capture = False

        parser = ResultParser()
        parser.feed(html)
        return parser.results[:8]
