from typing import Annotated
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_PATH = Path("../data/access.log")


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


@app.get("/")
def root():
    return {"status": "ok", "message": "Synthropy Dashboard API is Online"}


@app.get("/logs")
def get_logs(
    limit: Annotated[int, Query(ge=1, le=15000)] = 5000,
):
    logs, failed_logs = split_logs()
    return {"total": len(logs), "data": logs[-limit:]}


@app.get("/failed-logs")
def get_failed_logs(
    limit: Annotated[int, Query(ge=1, le=15000)] = 5000,
):
    logs, failed_logs = split_logs()
    return {"total": len(failed_logs), "data": failed_logs[-limit:]}


def get_status_counts(logs):
    status_counts = {}
    for log in logs:
        status = log.get("status")
        if status is None:
            status_counts["unknown"] = status_counts.get("unknown", 0) + 1
            continue
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1
    return status_counts


@app.get("/stats/status-codes")
def status_counts():
    logs, _ = split_logs()
    return {"total": len(logs), "data": get_status_counts(logs)}


def get_top_pages(logs):
    path_counts = {}
    for log in logs:
        path = log.get("path")
        if not path:
            continue
        path_counts[path] = path_counts.get(path, 0) + 1
    page_count = []

    for page, count in path_counts.items():
        page_count.append({"path": page, "count": count})

    return sorted(page_count, key=lambda entry: entry["count"], reverse=True)


@app.get("/stats/top-pages")
def top_pages(
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    logs, _ = split_logs()
    return {"total": len(logs), "data": get_top_pages(logs)[:limit]}
