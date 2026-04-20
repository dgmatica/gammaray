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


def get_top_pages_by_avg_size(logs):
    path_stats = {}

    for log in logs:
        path = log.get("path")
        size = log.get("size")
        if not path:
            continue
        if size is None:
            continue
        if path not in path_stats:
            path_stats[path] = {
                "path": path,
                "count": 1,
                "total_size": size,
            }
            continue
        path_stats[path]["count"] += 1
        path_stats[path]["total_size"] += size
    result = []
    for entry in path_stats.values():
        result.append(
            {
                "path": entry["path"],
                "count": entry["count"],
                "total_size": entry["total_size"],
                "avg_size": entry["total_size"] / entry["count"],
            }
        )

    return sorted(result, key=lambda entry: entry["avg_size"], reverse=True)


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


def get_method_status_counts(logs):
    method_status_stats = {}

    for log in logs:
        method = log.get("method") or "unknown"
        status = log.get("status") or "unknown"
        path = log.get("path") or "unknown"
        key = (method, status)

        if key not in method_status_stats:
            method_status_stats[key] = {
                "method": method,
                "status": status,
                "count": 0,
                "path_counts": {},
            }

        method_status_stats[key]["count"] += 1
        path_counts = method_status_stats[key]["path_counts"]
        path_counts[path] = path_counts.get(path, 0) + 1

    result = []

    for entry in method_status_stats.values():
        path_counts = entry["path_counts"]
        top_paths = []

        for path, count in path_counts.items():
            top_paths.append({"path": path, "count": count})

        top_paths = sorted(top_paths, key=lambda item: item["count"], reverse=True)

        result.append(
            {
                "method": entry["method"],
                "status": entry["status"],
                "count": entry["count"],
                "unique_paths_count": len(path_counts),
                "top_paths": top_paths[:3],
            }
        )

    return sorted(result, key=lambda item: item["count"], reverse=True)


@app.get("/stats/method-status-aggregation")
def get_method_status_aggregation():
    logs, _ = split_logs()
    data = get_method_status_counts(logs)

    return {
        "returned_items": len(data),
        "data": data,
    }


def get_overview(logs, failed_logs):
    total_valid_logs = len(logs)
    total_failed_logs = len(failed_logs)

    unique_paths_set = set()
    durations = []
    sizes = []

    for log in logs:
        path = log.get("path")
        duration = log.get("duration")
        size = log.get("size")

        if path:
            unique_paths_set.add(path)

        if duration is not None:
            durations.append(duration)

        if size is not None:
            sizes.append(size)

    unique_paths = len(unique_paths_set)

    status_counts = get_status_counts(logs)
    top_status_code = None
    if status_counts:
        top_status, top_status_count = max(
            status_counts.items(),
            key=lambda item: item[1],
        )
        top_status_code = {
            "status": top_status,
            "count": top_status_count,
        }

    top_pages = get_top_pages(logs)
    top_page = top_pages[0] if top_pages else None

    method_status_data = get_method_status_counts(logs)
    top_method_status = None
    if method_status_data:
        top_method_status = {
            "method": method_status_data[0]["method"],
            "status": method_status_data[0]["status"],
            "count": method_status_data[0]["count"],
        }

    avg_duration = None
    max_duration = None
    if durations:
        avg_duration = sum(durations) / len(durations)
        max_duration = max(durations)

    avg_size = None
    if sizes:
        avg_size = sum(sizes) / len(sizes)

    return {
        "total_valid_logs": total_valid_logs,
        "total_failed_logs": total_failed_logs,
        "unique_paths": unique_paths,
        "top_status_code": top_status_code,
        "top_page": top_page,
        "top_method_status": top_method_status,
        "avg_duration": avg_duration,
        "max_duration": max_duration,
        "avg_size": avg_size,
    }


@app.get("/stats/overview")
def get_overview_stats():
    logs, failed_logs = split_logs()
    return get_overview(logs, failed_logs)
