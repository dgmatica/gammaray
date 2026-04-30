from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AccessLog(SQLModel, table=True):
    __tablename__ = "access_logs"

    id: int | None = Field(default=None, primary_key=True)

    raw_time: str
    timestamp: datetime = Field(index=True)

    ip: str = Field(index=True)
    method: str = Field(index=True)
    path: str = Field(index=True)
    query: str = ""

    status: int = Field(index=True)
    size: int = 0
    duration: float = 0.0

    referer: str | None = None
    user_agent: str | None = None

    raw_hash: str = Field(index=True, unique=True)
    client_fingerprint: str | None = Field(default=None, index=True)

    imported_at: datetime = Field(default_factory=utc_now)


class FailedLog(SQLModel, table=True):
    __tablename__ = "failed_logs"

    id: int | None = Field(default=None, primary_key=True)

    raw_line: str
    error_message: str | None = None
    line_number: int | None = None

    raw_hash: str = Field(index=True, unique=True)

    imported_at: datetime = Field(default_factory=utc_now)
