# Hospitality Academy V8.4 — Commercial SaaS + Payments + Multi-Tenant

## What is new
- Hotel tenant isolation is preserved across the existing hotel_id data model.
- Commercial subscription plans: Starter / Professional / Enterprise.
- Seat limits enforced for active employees.
- Billing dashboard with current plan, active seats, payment history and upgrade flow.
- PaymentTransaction ledger with hotel-scoped references and audit events.
- Local Demo Checkout for sales demos and end-to-end QA.
- Payment provider configuration prepared for production gateway rollout.
- `PAYMENT_PROVIDER=demo` is the safe local default.

## Local run
1. Run `run.bat` on Windows.
2. Open http://127.0.0.1:8000/login
3. Demo manager: `manager@demo-hotel.com` / `Manager123!`
4. Open Subscription and choose Professional to test checkout.

## Production billing
The application is intentionally configured to use `demo` locally. For production, set provider credentials in `.env` and replace the demo completion flow with the selected hosted-checkout adapter. Paymob's current API flow uses a payment intention, hosted/embedded checkout, and webhooks/HMAC for final payment confirmation; do not mark a subscription paid from a browser redirect alone.

## Production checklist
- PostgreSQL
- HTTPS + secure cookies
- Strong SECRET_KEY
- Real payment provider credentials
- Webhook HMAC verification
- Email provider
- Backups/object storage
- Rate limiting + CSRF protection
- Terms/privacy/refund policy

## Commercial pricing & trial
- Starter: 999 EGP/month — up to 50 employees
- Professional: 3,499 EGP/month — up to 150 employees
- Enterprise: 5,999 EGP/month — up to 500 employees
- Every paid checkout starts a 7-day free trial immediately after payment confirmation.
- The selected paid plan starts automatically on day 8; the first paid renewal is scheduled 30 days after the paid start date.


### Additional payment methods
- Paymob: cards/mobile wallets/other methods enabled on the merchant account, via production hosted checkout + webhook/HMAC.
- InstaPay: manual transfer workflow with configurable InstaPay address/IPA and transfer reference. The app intentionally does not auto-confirm a payment from a typed reference; connect verification/reconciliation before production.

Configure: `INSTAPAY_ADDRESS` and `INSTAPAY_ACCOUNT_NAME` in `.env`.


### InstaPay payment confirmation
Mobile checkout now includes an Open InstaPay button, IPA copy button, optional official InstaPay payment link, transfer reference, and receipt image upload (JPG/PNG/WEBP up to 5MB). Uploaded receipts are stored under `instance/payment_proofs/` and transactions enter `awaiting_confirmation`; they are not auto-marked paid. Set `INSTAPAY_LINK` to the exact official `https://ipn.eg/S/...` link generated/shared by your InstaPay app if you want the direct payment-link button.
