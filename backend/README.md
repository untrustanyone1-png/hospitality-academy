# Hospitality Academy — SaaS Backend Foundation

## Local run (Python 3.14.7)
1. Open a terminal in this folder.
2. Create an environment: `py -3.14 -m venv .venv`
3. Activate it and install: `python -m pip install -r requirements.txt`
4. Set a strong `SECRET_KEY` in production.
5. Run: `uvicorn app.main:app --reload`
6. Open `http://127.0.0.1:8000/docs`

## Demo
POST `/api/seed`, then login:
- email: admin@demo-hotel.com
- password: Demo123!

The token contains the user and hotel tenant. Tenant endpoints always derive `hotel_id` from the authenticated user rather than accepting a hotel ID from the client.

## Database
Default: SQLite.
Production-ready connection format: set `DATABASE_URL` to a PostgreSQL SQLAlchemy URL, e.g. `postgresql+psycopg://USER:PASSWORD@HOST:5432/DB`.

This is the SaaS foundation, not the final production release. Remaining work includes migrations, email/invitations, complete permissions, rate limiting, audit logs, billing/payment, storage, background jobs, production deployment and connecting the static frontend to the API.
