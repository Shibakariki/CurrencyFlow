import json
from pathlib import Path

class Storage:
    def __init__(self):
        self.history_path = Path("data/history.json")
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.history_path.exists():
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            

    def load_history(self):
        with open(self.history_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_history(self, new_record):
        history = self.load_history()
        if not isinstance(history, list):
            raise ValueError("History file is corrupted or not a list.")
        history.append(new_record)
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)