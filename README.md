# 🚗 RentMe — Cab Rental Platform API

A production-ready REST API backend for a cab/car rental platform built with **Django 6** and **Django REST Framework**. Features a two-role system (Owner & Customer), real-time availability search, conflict-aware booking, Redis caching, and full Docker support.

---

## ✨ Features

- 🔐 **JWT Authentication** — secure login with access & refresh tokens
- 👥 **Two User Roles** — Owners list vehicles; Customers book them
- 🚗 **Vehicle Management** — full CRUD with multi-image support
- 🔍 **Smart Availability Search** — filter by city and date range, excludes already-booked vehicles
- 📅 **Booking System** — overlap conflict prevention, auto price calculation
- ✅ **Owner Booking Controls** — accept or reject incoming bookings
- ❌ **Booking Cancellation** — customers can cancel pending bookings
- ⚡ **Redis Caching** — vehicle list and search results cached per query
- 📄 **Pagination** — page-based results (5 per page)
- 🐳 **Docker + PostgreSQL** — fully containerized with docker-compose
- 📖 **Swagger Docs** — interactive API docs via `drf-spectacular`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 6.0.3 + Django REST Framework 3.16.1 |
| Auth | JWT via `djangorestframework-simplejwt` |
| Database | PostgreSQL 15 (SQLite for dev) |
| Cache | Redis 7 via `django-redis` |
| Containerization | Docker + Docker Compose |
| API Docs | `drf-spectacular` (Swagger UI) |
| Image Handling | Pillow |
| WSGI Server | Gunicorn |

---

## 📁 Project Structure

```
cab-rental-platform/
├── rentme/                  # Core Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── common/              # Shared base model (created_at, updated_at)
│   ├── users/               # Registration, login, user profiles & roles
│   ├── vehicles/            # Vehicle CRUD, search, image management
│   └── bookings/            # Booking creation, cancellation, owner controls
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

## 🚀 Getting Started

### Option A — Docker (Recommended)

**Prerequisites:** Docker and Docker Compose installed.

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/cab-rental-platform.git
   cd cab-rental-platform
   ```

2. **Create a `.env` file** in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=rentme
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432
   REDIS_URL=redis://redis:6379/1
   ```

3. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations** (in a new terminal)
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a superuser** (optional)
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

The API will be live at `http://localhost:8000`.

---

### Option B — Local Setup

1. **Clone & create a virtual environment**
   ```bash
   git clone https://github.com/your-username/cab-rental-platform.git
   cd cab-rental-platform
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Redis locally**
   ```bash
   sudo apt install redis-server   # Ubuntu/Debian
   redis-server
   ```

4. **Configure the database** in `rentme/settings.py` (use SQLite for quick dev or point to a local PostgreSQL instance).

5. **Apply migrations and run**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 🔑 Authentication

The API uses **JWT (JSON Web Tokens)**.

| Token | Lifetime |
|---|---|
| Access Token | 60 minutes |
| Refresh Token | 1 day |

Include the access token in every protected request:

```
Authorization: Bearer <access_token>
```

---

## 📡 API Endpoints

### Base URL: `http://localhost:8000`

---

### 👤 Users — `/api/users/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `register/` | No | Register a new user |
| `POST` | `login/` | No | Login and receive JWT tokens |
| `POST` | `refresh/` | No | Refresh access token |

#### Register — `POST /api/users/register/`

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass",
  "role": "CUSTOMER",
  "phone": "9876543210"
}
```

> `role` must be either `"OWNER"` or `"CUSTOMER"`.

#### Login — `POST /api/users/login/`

```json
{
  "username": "john_doe",
  "password": "securepass"
}
```

Response:
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

---

### 🚗 Vehicles — `/api/vehicles/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `list/` | No | List all active vehicles (paginated + cached) |
| `GET` | `<id>/` | No | Get vehicle details |
| `POST` | `create/` | ✅ Owner | Create a new vehicle |
| `PUT` | `update/<id>/` | ✅ Owner | Update vehicle details |
| `DELETE` | `delete/<id>/` | ✅ Owner | Delete a vehicle |
| `POST` | `search/` | No | Search available vehicles by city & dates |

#### Create Vehicle — `POST /api/vehicles/create/`

```json
{
  "title": "Swift Dzire",
  "model": "2023",
  "city": "Pune",
  "daily_rate": "1500.00"
}
```

#### Search Vehicles — `POST /api/vehicles/search/?page=1`

Returns vehicles in the given city that are **not** already booked for the requested dates.

```json
{
  "city": "Pune",
  "start_date": "2026-06-10",
  "end_date": "2026-06-13"
}
```

> Search results are **Redis-cached** per unique `city + start_date + end_date + page` combination for 5 minutes.

---

### 📅 Bookings — `/api/bookings/`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `bookvehicle/` | ✅ Customer | Create a new booking |
| `GET` | `mybookings/` | ✅ Customer | View your bookings |
| `POST` | `<id>/cancel/` | ✅ Customer | Cancel a pending booking |
| `GET` | `ownerbookings/` | ✅ Owner | View all bookings for your vehicles |
| `POST` | `acceptbooking/<id>/` | ✅ Owner | Confirm a pending booking |

#### Create Booking — `POST /api/bookings/bookvehicle/`

```json
{
  "vehicle": 3,
  "start_date": "2026-06-10",
  "end_date": "2026-06-13"
}
```

Response includes automatically calculated `total_price`:

```json
{
  "id": 7,
  "vehicle": 3,
  "start_date": "2026-06-10",
  "end_date": "2026-06-13",
  "total_price": "4500.00"
}
```

> Price = `daily_rate × number of days` (minimum 1 day).

---

## 🧠 Booking Logic

### Conflict Prevention

A booking is rejected if any existing `PENDING` or `CONFIRMED` booking for the same vehicle overlaps the requested dates:

```
existing.start_date < requested.end_date
AND
existing.end_date > requested.start_date
```

### Business Rules

- An owner **cannot book their own vehicle**
- Only `PENDING` bookings can be cancelled
- Only the vehicle's owner can accept a booking
- `end_date` must be after `start_date`

### Booking Status Flow

```
PENDING  →  CONFIRMED  (owner accepts)
PENDING  →  CANCELLED  (customer cancels)
```

---

## ⚡ Redis Caching

Two endpoints are cached to reduce database load:

| Endpoint | Cache Key Pattern | TTL |
|---|---|---|
| `GET /api/vehicles/list/` | `vehicle_list_{page}` | 5 minutes |
| `POST /api/vehicles/search/` | `search_{city}_{start}_{end}_page_{page}` | 5 minutes |

Cache is **automatically cleared** whenever a vehicle is updated or deleted.

---

## 🔒 Permissions Summary

| Action | Who Can Do It |
|---|---|
| Browse / search vehicles | Anyone |
| Register / login | Anyone |
| Create vehicle | Authenticated **Owner** only |
| Update / delete vehicle | The vehicle's **Owner** only |
| Create booking | Authenticated **Customer** only |
| Cancel booking | The **Customer** who made the booking |
| View own bookings | Authenticated Customer |
| View & accept incoming bookings | Authenticated Owner |

---

## 🐳 Docker Services

The `docker-compose.yml` spins up three services:

| Service | Image | Port |
|---|---|---|
| `web` | Built from Dockerfile (Python 3.11) | `8000` |
| `db` | `postgres:15` | `5432` |
| `redis` | `redis:7` | `6379` |

---

## 📖 API Documentation

Interactive Swagger UI:

```
http://localhost:8000/docs/
```

OpenAPI schema (JSON):

```
http://localhost:8000/schema/
```

---

## ⚙️ Key Configuration

```python
# Pagination
PAGE_SIZE = 5

# JWT Lifetimes
ACCESS_TOKEN_LIFETIME  = 60 minutes
REFRESH_TOKEN_LIFETIME = 1 day

# Redis Cache
LOCATION = "redis://6379/1"
```

> **Before deploying to production:** replace `SECRET_KEY` with a secure value, set `DEBUG=False`, configure `ALLOWED_HOSTS`, and use environment variables for all credentials.

---

## 🚀 Future Enhancements

- 💳 Payment gateway integration
- ⭐ Ratings & reviews for vehicles
- 📍 Location-based search (GPS / maps)
- 📧 Email notifications for booking updates
- 📊 Admin analytics dashboard

---

## 👨‍💻 Author

**Abhijit Magar**
