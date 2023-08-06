from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, MutableMapping

from .config import create_kolo_directory


@contextmanager
def db_cursor(db_path, wal_mode=True):
    """
    Wrap sqlite's cursor for use as a context manager

    Commits all changes if no exception is raised.
    Always closes the cursor/connection after the context manager exits.
    """
    if wal_mode:
        connection = sqlite3.connect(str(db_path), isolation_level=None)
        connection.execute("pragma journal_mode=wal")
    else:
        connection = sqlite3.connect(str(db_path))  # pragma: no cover
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def get_db_path() -> Path:
    return create_kolo_directory() / "db.sqlite3"


def create_invocations_table(cursor) -> None:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS invocations (
        id text PRIMARY KEY NOT NULL,
        created_at TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')) NOT NULL,
        data text NOT NULL
    );
    """
    create_timestamp_index_query = """
        CREATE INDEX IF NOT EXISTS
        idx_invocations_created_at
        ON invocations (created_at);
        """

    cursor.execute(create_table_query)
    cursor.execute(create_timestamp_index_query)


def setup_db(config: MutableMapping[str, Any] | None = None) -> Path:
    if config is None:
        config = {}
    db_path = get_db_path()

    wal_mode = config.get("wal_mode", True)

    with db_cursor(db_path, wal_mode) as cursor:
        create_invocations_table(cursor)

    return db_path


def save_invocation_in_sqlite(
    db_path: Path,
    trace_id: str,
    json_string: str,
    wal_mode: bool = True,
    ignore_errors: bool = True,
    created_at: datetime | None = None,
) -> None:
    ignore = " OR IGNORE" if ignore_errors else ""
    _columns = ["id", "data"]
    values: list[object] = [trace_id, json_string]
    if created_at is not None:
        _columns.append("created_at")
        values.append(created_at)
    columns = ", ".join(_columns)
    params = ",".join(["?" for _ in _columns])

    insert_sql = f"INSERT{ignore} INTO invocations({columns}) VALUES({params})"

    # We can't reuse a connection
    # because we're in a new thread
    with db_cursor(db_path, wal_mode) as cursor:
        cursor.execute(insert_sql, values)


def load_trace_from_db(db_path: Path, trace_id: str, wal_mode: bool = True) -> str:
    fetch_sql = "SELECT data FROM invocations WHERE id = ?"

    with db_cursor(db_path, wal_mode) as cursor:
        cursor.execute(fetch_sql, (trace_id,))
        row = cursor.fetchone()
    return row[0]


def list_traces_from_db(db_path: Path, wal_mode: bool = True):
    list_sql = "SELECT id, created_at FROM invocations"

    with db_cursor(db_path, wal_mode) as cursor:
        cursor.execute(list_sql)
        rows = cursor.fetchall()
    return rows


def delete_traces_from_db(
    db_path: Path, before: datetime, vacuum: bool = False, wal_mode: bool = True
):
    delete_sql = "DELETE FROM invocations WHERE (created_at < ?)"

    with db_cursor(db_path, wal_mode) as cursor:
        cursor.execute(delete_sql, (before,))
        cursor.execute("SELECT changes()")
        data = cursor.fetchone()

    if vacuum:
        with db_cursor(db_path, wal_mode=False) as cursor:
            cursor.execute("VACUUM")
    return data[0]
