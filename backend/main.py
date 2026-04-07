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
