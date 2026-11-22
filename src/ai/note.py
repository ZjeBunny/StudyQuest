import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class NoteAI:
    def __init__(self, base_url="http://localhost:11434", model="qwen3.5:4b", vision_model="gemma3:4b"):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.vision_model = vision_model

    def _chat(self, messages, images=None, model=None, timeout=180, json_mode=False, num_predict=2200):
        payload = {
            "model": model or self.model,
            "messages": messages,
            "stream": False,
            "think": False,
            "keep_alive": "5m",
            "options": {"num_ctx": 3072, "num_predict": num_predict, "temperature": 0.25}
        }
        if json_mode:
            payload["format"] = "json"
        if images:
            payload["messages"][-1]["images"] = images
        request = Request(
            self.base_url + "/api/chat",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            if error.code == 404:
                raise RuntimeError(f"Nie znaleziono modelu {model or self.model}. Pobierz go poleceniem ollama pull {model or self.model}.") from error
            raise RuntimeError(f"Ollama HTTP {error.code}: {detail[:350]}") from error
        except (URLError, OSError) as error:
            raise RuntimeError(f"Nie można połączyć się z Ollama ({self.base_url}): {error}") from error
        content = result.get("message", {}).get("content", "")
        if not content:
            raise ValueError("Model zwrócił pustą odpowiedź. Spróbuj ponownie.")
        return content

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

    def _plan_material(self, title, text, kind):
        words = len(text.split())
        if words < 12:
            raise ValueError("Za mało materiału do generowania. Dodaj co najmniej kilkanaście słów.")
        upper = 18 if kind == "quiz" else 30
        estimated = max(2, min(upper, round(words / (65 if kind == "quiz" else 35))))
        prompt = (
            "Oceń zakres materiału edukacyjnego. Zdecyduj, ile "
            + ("pytań testowych" if kind == "quiz" else "fiszek")
            + " potrzeba, by pokryć wszystkie WAŻNE niezależne fakty bez powtórzeń. "
            + f"Zwróć tylko JSON: {{\"count\": liczba całkowita od 1 do {upper}}}. "
            + f"Orientacyjna liczba to {estimated}, ale dostosuj ją do liczby pojęć. "
            + "Nie twórz więcej pozycji niż faktycznie uzasadnia treść. "
            + f"Tytuł: {title}\nMATERIAŁ:\n{text[:9500]}"
        )
        try:
            raw = self._chat([{"role": "user", "content": prompt}], json_mode=True, timeout=90)
            parsed = json.loads(raw)
            count = int(parsed.get("count", estimated))
            return max(1, min(upper, count))
        except (ValueError, TypeError, KeyError):
            return estimated

    def generate_quiz(self, title, text, count=None):
        count = max(2, min(18, round(len(text.split()) / 65))) if count is None else max(1, min(int(count), 18))
        prompt = (
            'Na podstawie materiału przygotuj test po polsku. Zwróć WYŁĄCZNIE '
            'JSON: {"questions":[{"question":"tekst",'
            '"answers":["A","B","C","D"],"correct":0,"explanation":"krótko"}]}. '
            'Dokładnie cztery sensowne różne odpowiedzi; indeks correct od 0 do 3. '
            'Nie wymyślaj faktów spoza materiału. Bez powtórzeń. '
            f'Wygeneruj {count} pytań, o ile materiał na to pozwala. '
            f'Tytuł: {title}\nMATERIAŁ:\n{text[:12000]}'
        )
        raw = self._chat([{"role": "user", "content": prompt}], json_mode=True, num_predict=min(5500, 300 + count * 170))
        return self._validate_questions(self._parse_json(raw, "questions"))

    def generate_flashcards(self, title, text, count=None):
        count = max(2, min(30, round(len(text.split()) / 35))) if count is None else max(1, min(int(count), 30))
        prompt = (
            'Utwórz fiszki z materiału. Zwróć WYŁĄCZNIE JSON: '
            '{"cards":[{"front":"pytanie lub hasło","back":"krótka odpowiedź"}]}. '
            'Każda fiszka dotyczy jednego faktu. Nie wymyślaj informacji. '
            f'Wygeneruj {count} fiszek, o ile materiał na to pozwala. '
            f'Tytuł: {title}\nMATERIAŁ:\n{text[:12000]}'
        )
        raw = self._chat([{"role": "user", "content": prompt}], json_mode=True, num_predict=min(4500, 200 + count * 90))
        return self._validate_cards(self._parse_json(raw, "cards"))

    def study_answer(self, history, question):
        messages = [{"role": "system", "content": (
            "Jesteś polskim korepetytorem StudyQuest. Odpowiadaj rzeczowo, "
            "zrozumiale i dydaktycznie. Uwzględnij historię rozmowy. "
            "Gdy nie masz pewności, zaznacz to. Nie udawaj dostępu do internetu.") }]
        messages.extend(history[-12:])
        messages.append({"role": "user", "content": question})
        return self._chat(messages, timeout=180)

    def propose_study_note(self, history, material):
        transcript = "\n".join(f"{m['role']}: {m['content']}" for m in history[-16:])
        prompt = (
            'Na podstawie rozmowy ucznia i dostarczonego materiału stwórz użyteczną '
            'notatkę do nauki po polsku. Zwróć TYLKO JSON: '
            '{"title":"krótki tytuł","category":"nazwa przedmiotu",'
            '"html":"<h1>...</h1><p>...</p>"}. '
            'Kategoria powinna być krótką nazwą przedmiotu (np. Matematyka). '
            'Nie dopowiadaj niepotwierdzonych faktów, uporządkuj najważniejsze '
            'pojęcia i przykłady. Bez skryptów i zewnętrznych linków. '
            f'ROZMOWA:\n{transcript[:10000]}\nMATERIAŁ:\n{material[:9000]}'
        )
        raw = self._chat([{"role": "user", "content": prompt}], json_mode=True)
        data = json.loads(raw)
        for key in ("title", "category", "html"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                raise ValueError("AI nie zwróciło kompletnej notatki.")
        return {key: data[key].strip() for key in ("title", "category", "html")}

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

    @staticmethod
    def _validate_questions(items):
        valid = []
        for item in items:
            if not isinstance(item, dict):
                continue
            answers = item.get("answers")
            correct = item.get("correct")
            if isinstance(correct, str) and correct.strip().isdigit():
                correct = int(correct)
            if (isinstance(item.get("question"), str) and item["question"].strip()
                    and isinstance(answers, list) and len(answers) == 4
                    and all(isinstance(answer, str) and answer.strip() for answer in answers)
                    and type(correct) is int and 0 <= correct < 4):
                valid.append({"question": item["question"].strip(),
                              "answers": [a.strip() for a in answers],
                              "correct": correct,
                              "explanation": str(item.get("explanation") or "")})
        if not valid:
            raise ValueError("Model nie zwrócił poprawnych pytań. Spróbuj ponownie lub wybierz większy model.")
        return valid

    @staticmethod
    def _validate_cards(items):
        valid = []
        for item in items:
            if isinstance(item, dict) and isinstance(item.get("front"), str) and isinstance(item.get("back"), str):
                if item["front"].strip() and item["back"].strip():
                    valid.append({"front": item["front"].strip(), "back": item["back"].strip()})
        if not valid:
            raise ValueError("Model nie zwrócił poprawnych fiszek.")
        return valid

    def read_image(self, path):
        import base64
        with open(path, "rb") as file:
            encoded = base64.b64encode(file.read()).decode("ascii")
        return self._chat(
            [{"role": "user", "content": "Odczytaj zawartość obrazu. Zachowaj wzory, tabele i kolejność. Nie zgaduj nieczytelnych fragmentów."}],
            images=[encoded],
            model=self.vision_model,
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
