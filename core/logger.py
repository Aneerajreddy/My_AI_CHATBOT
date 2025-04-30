
import json
import os

LOG_FILE = "./data/logs/events_log.jsonl"

def log_event(event):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
