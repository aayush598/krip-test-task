def load_prompt(version: str) -> str:
    try:
        with open(f'prompts/{version}.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None