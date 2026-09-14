# Hospitality Academy — Online Deployment

This build is prepared for deployment as a FastAPI web service.

## Fastest deployment path
1. Push this folder to a Git repository.
2. Create a PostgreSQL database.
3. Deploy the web service with:
   `pip install -r requirements-prod.txt`
   and start with:
   `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables from `.env.example`.
5. Verify `/health`, `/sales`, and `/demo`.

## Important production settings
- `APP_ENV=production`
- `SECRET_KEY` must be a long random secret.
- `DATABASE_URL` should point to PostgreSQL.
- `SESSION_HTTPS_ONLY=true` behind HTTPS.
- Keep `PAYMENT_PROVIDER=demo` until a real Paymob hosted-checkout + webhook/HMAC integration is configured.
- Configure `INSTAPAY_ADDRESS` and the exact official `INSTAPAY_LINK` if used.

## Commercial flow
Landing `/sales` → Demo `/demo` → Register `/register` → Billing `/billing` → Payment → 7-day trial.

## Data/storage note
The app currently stores uploaded payment proofs and imports under `instance/`. For production, put this directory on persistent storage or migrate uploads to object storage before relying on receipt retention.

## Demo credentials
Manager: `manager@demo-hotel.com`
Password: `Manager123!`
