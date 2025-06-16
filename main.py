from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.prompt_loader import load_prompt
from utils.logger import log_request
import os, time
from dotenv import load_dotenv
from collections import defaultdict
from google import genai

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

@app.get("/")
def read_root():
    return {"message": "Welcome to Gemini Chatbot API"}


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
    avg_time = (
        sum(metrics["response_times"]) / len(metrics["response_times"])
        if metrics["response_times"] else 0
    )
    return {
        "total_requests": metrics["total_requests"],
        "requests_per_version": dict(metrics["requests_per_version"]),
        "average_response_time": round(avg_time, 3)
    }