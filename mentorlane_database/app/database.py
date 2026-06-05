from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator

import pymysql
from pymysql.cursors import DictCursor


@dataclass(frozen=True)
class MySQLConfig:
    """Configuration needed to connect to the MentorLane MySQL database."""

    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "MentorLane"


DEFAULT_CONFIG = MySQLConfig()


def get_connection(config: MySQLConfig = DEFAULT_CONFIG) -> pymysql.connections.Connection:
    """Create and return a PyMySQL connection using the provided configuration."""

    return pymysql.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        database=config.database,
        cursorclass=DictCursor,
        autocommit=False,
    )


@contextmanager
def mysql_session(
    config: MySQLConfig = DEFAULT_CONFIG,
) -> Generator[pymysql.connections.Connection, None, None]:
    """Context manager yielding a database connection and closing it afterwards."""

    connection = get_connection(config)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
