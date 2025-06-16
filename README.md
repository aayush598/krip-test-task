

## 🤖 Gemini Chatbot with Prompt Versioning

This is a chatbot application built with **FastAPI** and **Streamlit**, using the **Gemini 2.0 Flash API**. It supports **prompt versioning**, logs every interaction to both a `.txt` file and a SQLite database, and exposes performance metrics.

---

### 🚀 Features

* 🔀 Prompt versioning (`v1`, `v2`, ...)
* 🧠 Gemini 2.0 Flash integration for AI-generated responses
* 📋 Request logging in `log.txt` and `logs.db` (SQLite)
* 📊 Metrics endpoint for monitoring usage
* 🌐 Combined FastAPI backend and Streamlit frontend
* 📁 Modular structure with `utils/` for prompts and logging

---

### 📁 Folder Structure

```
project/
├── main.py                  # Entry point: runs both FastAPI & Streamlit
├── streamlit_app.py         # UI using Streamlit
├── prompts/
│   ├── v1.txt
│   └── v2.txt               # Prompt files for different versions
├── utils/
│   ├── logger.py            # Logs requests to txt & SQLite
│   └── prompt_loader.py     # Loads prompt by version
├── log.txt                  # Request log file
├── logs.db                  # SQLite database of logs
├── .env                     # Contains GEMINI_API_KEY
└── README.md
```

---

### 🧪 Requirements

* Python 3.8+
* `.env` file with your Gemini API Key:

```env
GEMINI_API_KEY=your_api_key_here
```

---

### 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/your-username/gemini-chatbot.git
cd gemini-chatbot
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create `.env` file**

```bash
echo "GEMINI_API_KEY=your_api_key" > .env
```

4. **Add prompt files**
   Place prompt files as `prompts/v1.txt`, `prompts/v2.txt`, etc.

---

### ▶️ Run the App
  
```bash
python app_runner.py
```

* FastAPI runs at: `http://localhost:8000`
* Streamlit UI: `http://localhost:8000/ui`

---

### 📮 API Endpoints

* `POST /chat`
  Accepts:

  ```json
  {
    "message": "Hello!",
    "prompt_version": "v1"
  }
  ```

  Returns:

  ```json
  {
    "response": "Hi there! How can I help you?"
  }
  ```

* `GET /metrics`
  Returns:

  ```json
  {
    "total_requests": 10,
    "requests_per_version": {"v1": 6, "v2": 4},
    "average_response_time": 1.234
  }
  ```

* `GET /ui`
  Loads the embedded Streamlit chatbot UI.

---

### 📊 Logging

Each request is logged to:

* `log.txt` (for human-readable logs)
* `logs.db` SQLite database in `logs` table:

```sql
CREATE TABLE logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT,
  prompt_version TEXT,
  duration REAL,
  message TEXT
);
```

---

### 🛠️ Future Improvements

* Add authentication (optional)
* Display logs and metrics in the UI
* Add support for more prompt versions dynamically

---

### 📬 License

MIT License. Use freely with credit.
