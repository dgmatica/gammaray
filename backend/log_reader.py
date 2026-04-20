import json

from config import LOG_PATH


def split_logs():
    logs = []
    failed_logs = []

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError:
                failed_logs.append(line)

    return logs, failed_logs
