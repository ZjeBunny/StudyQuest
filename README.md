# StudyQuest

### AI-powered learning and note-taking application

StudyQuest is an AI-powered learning application designed to make studying, organizing knowledge, and revising notes easier and more effective.

Create and organize your notes, use AI to improve your understanding of complex topics, and automatically turn your learning materials into flashcards. StudyQuest brings your study tools together in one place, helping you spend less time organizing and more time learning.

---

## ✨ Features

- **AI-Assisted Note-Taking** – Create, organize, and improve your notes with the help of AI.
- **AI Note Revision** – Summarize, explain, rewrite, and revise your existing notes.
- **Automatic Flashcard Generation** – Turn your notes into flashcards using AI, making knowledge revision easier.
- **Active Learning** – Reinforce your knowledge through question-and-answer practice.
- **Local AI Integration** – Use locally running AI models through Ollama.
- **Privacy-Focused** – Keep your learning materials and AI processing local when using local models.
- **User-Friendly Interface** – A clean desktop interface designed to provide a comfortable learning experience.

## 🧠 AI Integration

StudyQuest uses [Ollama](https://ollama.com/) to run AI models locally.

This allows the application to provide AI-powered learning assistance without relying on external AI APIs.

Supported capabilities include:
- Understanding and processing notes.
- Generating summaries and explanations.
- Creating flashcards from learning materials.
- Helping users revise and understand difficult topics.

Model availability and performance depend on your hardware and installed Ollama models.

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| PySide6 | Desktop graphical interface |
| Ollama | Local AI model integration |
| SQLite | Local data storage |

## 🚀 Getting Started

### Prerequisites

Before running StudyQuest, make sure you have:

- Python installed.
- Ollama installed and running.
- At least one compatible AI model downloaded.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ZjeBunny/StudyQuest.git
   cd StudyQuest
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it:

   **Windows:**
   ```powershell
   .venv\Scripts\activate
   ```

   **Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Download an AI model using Ollama:

   ```bash
   ollama pull qwen3:4b
   ```

6. Run the application:

   ```bash
   python src/main.py
   ```

## 📁 Project Structure

```text
StudyQuest/
├── assets/
├── src/
│   ├── pages/
│   ├── widgets/
│   ├── main.py
│   └── theme.py
├── requirements.txt
├── README.md
└── LICENSE
```

*The project structure may change as development continues.*

## 🗺️ Roadmap

- [x] Initial desktop application setup
- [x] Light and dark themes
- [x] Main application interface
- [ ] AI-powered note assistance
- [ ] AI note revision and summarization
- [ ] Automatic flashcard generation
- [ ] Flashcard revision system
- [ ] Note organization and management
- [ ] Improved AI model management
- [ ] Application packaging and distribution

## 🔒 Privacy

StudyQuest is designed with local AI processing in mind. When using locally hosted Ollama models, prompts and learning materials are processed on your own machine rather than sent to an external AI API.

Other network-dependent features, if introduced, may have separate data requirements.

## 🤝 Contributing

Contributions, ideas, bug reports, and suggestions are welcome!

If you would like to contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## 📄 License

This project is licensed under the terms of the license specified in the `LICENSE` file.

---

<p align="center">
  <b>StudyQuest</b><br>
  Learn smarter. Stay organized. Remember more.
</p>