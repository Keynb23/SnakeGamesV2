import os
import json

HIGHSCORE_FILE = "highscore.txt"

def load_high_scores():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as file:
                content = file.read().strip()
                return json.loads(content) if content else []
        except (json.JSONDecodeError, FileNotFoundError, PermissionError, Exception) as e:
            print(f"Warning: Could not load high scores due to {type(e).__name__}: {e}. Starting with empty list.")
            return []
    return []

def save_high_score(username, score):
    try:
        # Ensure score is an integer
        score = int(score)
        scores = load_high_scores()
        if not isinstance(scores, list):
            print(f"Warning: High scores data is corrupted (not a list: {type(scores)}). Resetting.")
            scores = []
        scores.append({"username": str(username), "score": score})
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:3]
        with open(HIGHSCORE_FILE, "w") as file:
            json.dump(scores, file)
    except Exception as e:
        print(f"Error: Failed to save high score for {username} with score {score}. Exception: {type(e).__name__}: {e}")

def get_high_scores():
    return load_high_scores()

def get_high_score():
    scores = load_high_scores()
    return scores[0]["score"] if scores else 0