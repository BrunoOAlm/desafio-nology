"""
Cashback API - Nology Challenge.

A small FastAPI backend that:
  - calculates the cashback (business rules live in cashback.py),
  - logs every query in the database, tagged by the requester's IP,
  - returns the query history for that IP only,
  - serves the static frontend (plain HTML + JavaScript).

This is the ONLY backend: the frontend is static and talks to it over HTTP.
"""

import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from cashback import calculate_cashback
from database import get_history, init_db, save_query

app = FastAPI(title="Cashback API - Nology")

# Create the "queries" table on startup if it doesn't exist yet.
init_db()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


def get_client_ip(request: Request) -> str:
    """
    Return the real client IP.

    In production the app runs behind Render's proxy, so the real client IP
    arrives in the "X-Forwarded-For" header (the first entry is the client).
    Locally there is no proxy, so we use the direct connection IP.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host


@app.get("/api/health")
def health():
    """Simple health check, handy to confirm the API is up."""
    return {"status": "ok", "message": "Cashback API is running"}


@app.get("/api/cashback")
def cashback(client_type: str, purchase_amount: float, request: Request):
    """Calculate the cashback, log the query by IP, and return the result."""
    result = calculate_cashback(client_type, purchase_amount)
    ip = get_client_ip(request)
    save_query(ip, client_type, purchase_amount, result)

    return {
        "client_type": client_type,
        "purchase_amount": purchase_amount,
        "cashback": result,
    }


@app.get("/api/history")
def history(request: Request):
    """Return the query history for the requester's IP only."""
    ip = get_client_ip(request)
    return get_history(ip)


# Serve the static frontend (plain HTML + JS) at the root.
# Defined last so the /api/* routes above take precedence.
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
