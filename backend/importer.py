import json
from pathlib import Path

from sqlmodel import Session, select

from config import LOG_PATH
from database import create_db_and_tables, engine
from log_parser import make_raw_hash, parse_log_line
from models import AccessLog, FailedLog


def raw_hash_exists(session: Session, raw_hash: str) -> bool:
    access_log = session.exec(
        select(AccessLog).where(AccessLog.raw_hash == raw_hash)
    ).first()

    if access_log is not None:
        return True

    failed_log = session.exec(
        select(FailedLog).where(FailedLog.raw_hash == raw_hash)
    ).first()

    return failed_log is not None


def import_logs(log_path: Path = LOG_PATH) -> dict:
    create_db_and_tables()

    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")

    imported_count = 0
    failed_count = 0
    skipped_count = 0

    seen_hashes = set()

    with Session(engine) as session:
        with log_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                raw_line = line.strip()

                if not raw_line:
                    continue

                raw_hash = make_raw_hash(raw_line)

                if raw_hash in seen_hashes:
                    skipped_count += 1
                    continue

                seen_hashes.add(raw_hash)

                if raw_hash_exists(session, raw_hash):
                    skipped_count += 1
                    continue

                try:
                    parsed_data = parse_log_line(raw_line)
                    access_log = AccessLog(**parsed_data)

                    session.add(access_log)
                    imported_count += 1

                except (json.JSONDecodeError, KeyError, ValueError, TypeError) as error:
                    failed_log = FailedLog(
                        raw_line=raw_line,
                        error_message=str(error),
                        line_number=line_number,
                        raw_hash=raw_hash,
                    )

                    session.add(failed_log)
                    failed_count += 1

        session.commit()

    return {
        "log_path": str(log_path),
        "imported": imported_count,
        "failed": failed_count,
        "skipped": skipped_count,
    }


if __name__ == "__main__":
    result = import_logs()

    print("Import finished:")
    print(f"[PATH] Log path:   {result['log_path']}")
    print(f"[IMPT] Imported:   {result['imported']}")
    print(f"[FAIL] Failed:     {result['failed']}")
    print(f"[SKIP] Skipped:    {result['skipped']}")
