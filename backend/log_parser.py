import hashlib
import json
from datetime import datetime


def make_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def make_raw_hash(raw_line: str) -> str:
    return make_hash(raw_line)


def make_client_fingerprint(ip: str, user_agent: str | None) -> str:
    fingerprint_source = "|".join(
        [
            ip or "",
            user_agent or "",
        ]
    )

    return make_hash(fingerprint_source)


def parse_gunicorn_time(raw_time: str) -> datetime:
    return datetime.strptime(raw_time, "[%d/%b/%Y:%H:%M:%S %z]")


def parse_log_line(raw_line: str) -> dict:
    data = json.loads(raw_line)

    raw_time = data["time"]
    ip = data.get("ip", "")
    user_agent = data.get("user_agent")

    return {
        "raw_time": raw_time,
        "timestamp": parse_gunicorn_time(raw_time),
        "ip": ip,
        "method": data.get("method", ""),
        "path": data.get("path", ""),
        "query": data.get("query", ""),
        "status": int(data.get("status", 0)),
        "size": int(data.get("size", 0)),
        "duration": float(data.get("duration", 0.0)),
        "referer": data.get("referer"),
        "user_agent": user_agent,
        "raw_hash": make_raw_hash(raw_line),
        "client_fingerprint": make_client_fingerprint(
            ip=ip,
            user_agent=user_agent,
        ),
    }
