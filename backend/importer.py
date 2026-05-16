import json
from pathlib import Path

from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from config import LOG_PATH
from database import create_db_and_tables, engine
from log_parser import make_raw_hash, parse_log_line
from models import AccessLog, FailedLog


def insert_access_log(session: Session, parsed_data: dict) -> bool:
    statement = (
        insert(AccessLog)
        .values(**parsed_data)
        .on_conflict_do_nothing(index_elements=["raw_hash"])
    )

    result = session.execute(statement)

    return result.rowcount == 1


def insert_failed_log(
    session: Session,
    raw_line: str,
    error: Exception,
    line_number: int,
    raw_hash: str,
) -> bool:
    failed_log_data = {
        "raw_line": raw_line,
        "error_message": str(error),
        "line_number": line_number,
        "raw_hash": raw_hash,
    }

    statement = (
        insert(FailedLog)
        .values(**failed_log_data)
        .on_conflict_do_nothing(index_elements=["raw_hash"])
    )

    result = session.execute(statement)

    return result.rowcount == 1


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

                try:
                    parsed_data = parse_log_line(raw_line)
                    was_inserted = insert_access_log(session, parsed_data)

                    if was_inserted:
                        imported_count += 1
                    else:
                        skipped_count += 1

                except (json.JSONDecodeError, KeyError, ValueError, TypeError) as error:
                    was_inserted = insert_failed_log(
                        session=session,
                        raw_line=raw_line,
                        error=error,
                        line_number=line_number,
                        raw_hash=raw_hash,
                    )

                    if was_inserted:
                        failed_count += 1
                    else:
                        skipped_count += 1

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
