"""Helper utilities for connecting to PostgreSQL and executing SQL statements."""
from contextlib import contextmanager
from typing import Generator, Iterable, Optional, Sequence

import psycopg2
from psycopg2.extensions import connection as PGConnection

from config import DB_CONFIG


class DatabaseError(Exception):
    """Exception raised when a database operation fails."""


@contextmanager
def get_connection() -> Generator[PGConnection, None, None]:
    """Yield a PostgreSQL connection using the credentials defined in config.py."""
    connection = psycopg2.connect(**DB_CONFIG)
    try:
        yield connection
    finally:
        connection.close()


def execute_query(query: str, params: Optional[Sequence] = None, fetch: bool = False) -> Optional[Iterable]:
    """Execute a SQL query and optionally return fetched rows."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall() if fetch else None
                connection.commit()
                return rows
    except psycopg2.Error as exc:
        raise DatabaseError(f"Database operation failed: {exc}") from exc
