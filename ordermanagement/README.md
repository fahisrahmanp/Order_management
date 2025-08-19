# Order Management API (Django + DRF + TokenAuth)

## Setup
- Python 3.13.2
- `pip install -r requirements.txt` (or use the commands in the guide)
- `python manage.py migrate`
- `python manage.py createsuperuser`
- Start: `python manage.py runserver`

## Auth
- Obtain token: POST `/api/auth/token/` with `{username, password}`
- Use header: `Authorization: Token <token>`

## Endpoints
- POST `/api/customers/`  -> create customer
- GET  `/api/products/`   -> list products
- POST `/api/orders/`     -> create order (nested items)
- GET  `/api/orders/<id>/`-> order detail with `total_amount`
- PATCH `/api/orders/<id>/`-> update status
- GET  `/api/orders/?status=Delivered` -> filter by status
