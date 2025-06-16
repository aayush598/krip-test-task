import subprocess
import threading

def run_streamlit():
    subprocess.run(["streamlit", "run", "streamlit_app.py", "--server.port", "10000"])

def run_fastapi():
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

# Run Streamlit in a background thread
threading.Thread(target=run_streamlit).start()

# Run FastAPI (main server)
run_fastapi()
