import os
from contextlib import contextmanager

import psycopg


def get_database_url() -> str:
    # Puedes mover esto a variables de entorno después; por ahora es explícito y claro.
    # OJO: puerto 5433 porque Postgres.app está corriendo ahí.
    return os.getenv(
        "DATABASE_URL",
        "postgresql://deathkid@localhost:5433/network_inventory",
    )


@contextmanager
def get_conn():
    conn = psycopg.connect(get_database_url())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()