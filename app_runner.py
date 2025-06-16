# app_runner.py
import subprocess
import threading
import uvicorn
import time

def run_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

def run_streamlit():
    # Delay to allow FastAPI to bind first
    time.sleep(5)
    subprocess.run([
        "streamlit", "run", "streamlit_app.py",
        "--server.port=10000",                  # This will become the public Render port
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false"
    ])

if __name__ == "__main__":
    t1 = threading.Thread(target=run_fastapi)
    t2 = threading.Thread(target=run_streamlit)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
