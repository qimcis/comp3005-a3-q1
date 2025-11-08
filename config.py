"""Configuration values for connecting to the PostgreSQL database."""
from typing import Any, Dict

DB_CONFIG: Dict[str, Any] = {
    "host": "localhost",
    "port": 5432,
    "dbname": "comp3005",
    "user": "postgres",
    "password": "postgres",
}
