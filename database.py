"""
Database access for the Cashback app - Nology Challenge.

We talk to PostgreSQL directly with psycopg2 and plain SQL.
The connection string comes from the DATABASE_URL environment variable:
  - on Render it is injected automatically (see render.yaml);
  - locally you export it yourself before running the app.
"""

import os

import psycopg2
import psycopg2.extras

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Point it at your PostgreSQL connection string, "
        "e.g. postgresql://user:password@host:5432/dbname"
    )


def get_connection():
    """Open a new PostgreSQL connection."""
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Create the 'queries' table if it doesn't exist yet."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS queries (
                    id SERIAL PRIMARY KEY,
                    ip TEXT NOT NULL,
                    client_type TEXT NOT NULL,
                    purchase_amount DOUBLE PRECISION NOT NULL,
                    cashback DOUBLE PRECISION NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        conn.commit()
    finally:
        conn.close()


def save_query(ip, client_type, purchase_amount, cashback):
    """Insert one cashback query, tagged with the requester's IP."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO queries (ip, client_type, purchase_amount, cashback)
                VALUES (%s, %s, %s, %s)
                """,
                (ip, client_type, purchase_amount, cashback),
            )
        conn.commit()
    finally:
        conn.close()


def get_history(ip):
    """Return all queries made from a given IP, newest first."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT client_type, purchase_amount, cashback, created_at
                FROM queries
                WHERE ip = %s
                ORDER BY created_at DESC
                """,
                (ip,),
            )
            return cur.fetchall()
    finally:
        conn.close()
