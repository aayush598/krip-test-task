# Gemini Chatbot with FastAPI

## Description
A FastAPI-based chatbot powered by Gemini with support for prompt versioning, logging, metrics, and deployment.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env  # Replace with your GEMINI_API_KEY
uvicorn main:app --reload
```

## API Usage
### POST /chat
```json
{
  "message": "Tell me about AI",
  "prompt_version": "v1"
}
```
### GET /metrics
Returns total request count, average response time, and per-version usage.

## Prompt Versioning
Prompts are stored in `prompts/` folder with filenames like `v1.txt`, `v2.txt`, etc.

## Logging
All request logs are saved to `log.txt` with:
- Timestamp
- Prompt Version
- Response Time
- Message

## Deployment
Deploy on Render/Railway:
- Use Python 3.9
- Start command: `uvicorn main:app --host=0.0.0.0 --port=10000`
- Add `GEMINI_API_KEY` as environment variable

