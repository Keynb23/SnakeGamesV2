import os

HIGHSCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as file:
            content = file.read().strip()
            return int(content) if content else 0
    return 0

def save_high_score(score):
    current_high = load_high_score()
    if score > current_high:
        with open(HIGHSCORE_FILE, "w") as file:
            file.write(str(score))

def get_high_score():
    return load_high_score()