# app_runner.py
import subprocess
import threading
import uvicorn

def run_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

def run_streamlit():
    subprocess.run([
        "streamlit", "run", "streamlit_app.py",
        "--server.port=8501", "--server.enableCORS=false"
    ])

if __name__ == "__main__":
    t1 = threading.Thread(target=run_fastapi)
    t2 = threading.Thread(target=run_streamlit)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
