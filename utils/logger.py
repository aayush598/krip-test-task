from datetime import datetime

def log_request(message, prompt_version, duration):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} | {prompt_version} | {duration:.2f}s | {message}\n")
