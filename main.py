from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from utils.prompt_loader import load_prompt
from utils.logger import log_request
import os, time
from dotenv import load_dotenv
from collections import defaultdict
from google import genai
import sqlite3

# Load .env and Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Load Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# FastAPI setup
app = FastAPI()

# Metrics tracking
metrics = {
    "total_requests": 0,
    "requests_per_version": defaultdict(int),
    "response_times": []        
}

# Pydantic model
class ChatRequest(BaseModel):
    message: str
    prompt_version: str

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/ui")

@app.get("/ui", include_in_schema=False)
def serve_streamlit_ui():
    streamlit_url = "http://localhost:10000"  # Streamlit runs on this internally
    html_content = f"""
    <html>
        <head>
            <title>Gemini Chatbot UI</title>
        </head>
        <body style="margin:0;padding:0;overflow:hidden">
            <iframe src="{streamlit_url}" style="width:100%; height:100vh; border:none;"></iframe>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat(req: ChatRequest):
    prompt = load_prompt(req.prompt_version)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt version not found")

    full_prompt = f"{prompt}\nUser: {req.message}"

    start_time = time.time()
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt
        )
        answer = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    end_time = time.time()

    duration = end_time - start_time
    metrics["total_requests"] += 1
    metrics["requests_per_version"][req.prompt_version] += 1
    metrics["response_times"].append(duration)

    log_request(req.message, req.prompt_version, duration)
    return {"response": answer}

@app.get("/metrics")
def get_metrics():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    # Get total number of requests
    cursor.execute("SELECT COUNT(*) FROM logs")
    total_requests = cursor.fetchone()[0]

    # Get request count per prompt version
    cursor.execute("SELECT prompt_version, COUNT(*) FROM logs GROUP BY prompt_version")
    requests_per_version = {version: count for version, count in cursor.fetchall()}

    # Get average response time
    cursor.execute("SELECT AVG(duration) FROM logs")
    avg_time = cursor.fetchone()[0] or 0.0

    conn.close()

    return {
        "total_requests": total_requests,
        "requests_per_version": requests_per_version,
        "average_response_time": round(avg_time, 3)
    }