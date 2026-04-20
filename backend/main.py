from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from analytics import (
    get_method_status_counts,
    get_overview,
    get_status_counts,
    get_top_pages,
    get_top_pages_by_avg_size,
)
from log_reader import split_logs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/stats/status-codes")
def get_status_codes():
    logs, _ = split_logs()
    return {"total": len(logs), "data": get_status_counts(logs)}


@app.get("/stats/top-pages")
def get_top_pages_stats(
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    logs, _ = split_logs()
    return {"total": len(logs), "data": get_top_pages(logs)[:limit]}


@app.get("/stats/top-size-pages")
def get_top_size_pages(
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
):
    logs, _ = split_logs()
    data = get_top_pages_by_avg_size(logs)

    return {
        "returned_items": len(data[:limit]),
        "total_unique_paths": len(data),
        "data": data[:limit],
    }


@app.get("/stats/method-status")
def get_method_status():
    logs, _ = split_logs()
    data = get_method_status_counts(logs)

    return {
        "returned_items": len(data),
        "data": data,
    }


@app.get("/stats/overview")
def get_overview_stats():
    logs, failed_logs = split_logs()
    return get_overview(logs, failed_logs)
