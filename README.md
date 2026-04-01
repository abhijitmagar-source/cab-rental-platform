# 🚗 RentMe — Car Rental Backend API

A production-style backend system for a car rental platform built using **Django** and **Django REST Framework**.
This project demonstrates clean architecture, authentication, booking logic, and performance optimization using Redis.

---

## ✨ Highlights

* 🔐 JWT Authentication (Login / Logout with token blacklisting)
* 👥 User Roles (Owner & Customer)
* 🚗 Vehicle CRUD (Create, Update, Delete, List)
* 🔍 Smart Vehicle Search (City + Date Availability)
* 📅 Booking System with Conflict Prevention
* ❌ Cancel Booking Feature
* 🖼️ Multiple Vehicle Images Support
* ⚡ Redis Caching (List & Search APIs)
* 📄 Pagination for scalable responses

---

## 🏗️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Auth:** SimpleJWT
* **Cache:** Redis
* **Database:** SQLite (dev) / PostgreSQL (production-ready)

---

## 📁 Project Structure

```
rentme/
│
├── rentme/                # Core project settings
│   ├── settings.py
│   ├── urls.py
│
├── apps/
│   ├── users/             # Authentication & user profiles
│   ├── vehicles/          # Vehicle management APIs
│   ├── bookings/          # Booking system APIs
│
├── manage.py
```

---

## 🔐 Authentication APIs

| Method | Endpoint               | Description                      |
| ------ | ---------------------- | -------------------------------- |
| POST   | `/api/users/register/` | Register new user                |
| POST   | `/api/users/login/`    | Get JWT tokens                   |
| POST   | `/api/users/logout/`   | Logout (blacklist refresh token) |

---

## 🚗 Vehicle APIs

| Method | Endpoint                     | Description                            |
| ------ | ---------------------------- | -------------------------------------- |
| POST   | `/api/vehicles/create/`      | Create vehicle (Owner only)            |
| GET    | `/api/vehicles/list/`        | List all vehicles (paginated + cached) |
| GET    | `/api/vehicles/<id>/`        | Vehicle details                        |
| PUT    | `/api/vehicles/<id>/update/` | Update vehicle                         |
| DELETE | `/api/vehicles/<id>/delete/` | Delete vehicle                         |
| GET    | `/api/vehicles/my/`          | Owner’s vehicles                       |

---

## 🔍 Vehicle Search API

| Method | Endpoint                       | Description                   |
| ------ | ------------------------------ | ----------------------------- |
| POST   | `/api/vehicles/search/?page=1` | Search by city & availability |

### Example Request

```json
{
  "city": "Pune",
  "start_date": "2026-06-10",
  "end_date": "2026-06-12"
}
```

---

## 📅 Booking APIs

| Method | Endpoint                     | Description       |
| ------ | ---------------------------- | ----------------- |
| POST   | `/api/bookings/create/`      | Create booking    |
| GET    | `/api/bookings/my/`          | Get user bookings |
| POST   | `/api/bookings/<id>/cancel/` | Cancel booking    |

---

## 🧠 Booking Logic (Core Feature)

Prevents double booking using overlap logic:

```
start_date < existing_end_date AND end_date > existing_start_date
```

Ensures a vehicle cannot be booked for overlapping time periods.

---

## ⚡ Redis Caching

* Vehicle list API cached per page
* Search API cached using query-based keys
* Reduces database load and improves response time

### Example Cache Keys

```
vehicle_list_1
search_pune_2026-06-10_2026-06-12_page_1
```

---

## 🛠️ Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-url>
cd rentme
```

---

### 2. Create Virtual Environment

```
python -m venv env
source env/bin/activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Apply Migrations

```
python manage.py migrate
```

---

### 5. Run Development Server

```
python manage.py runserver
```

---

## ⚡ Redis Setup

### Install Redis

```
sudo apt install redis-server
```

### Start Redis

```
redis-server
```

### Django Configuration (`settings.py`)

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

---

## 🧪 API Testing

Use Postman or similar tools.

### Add Authorization Header

```
Authorization: Bearer <access_token>
```

---

## 🔒 Permissions Overview

* Only **authenticated users** can create bookings
* Only **owners** can create/update/delete vehicles
* All users can view vehicles

---

## 🚀 Future Enhancements

* 💳 Payment Integration
* ⭐ Ratings & Reviews
* 📍 Location-based filtering (maps)
* 📧 Email notifications
* 📊 Admin dashboard

---

## 👨‍💻 Author

**Abhijit Magar**

---

## 🎯 Project Purpose

This project is designed to demonstrate:

* REST API design
* Authentication & authorization
* Scalable backend architecture
* Performance optimization using caching
* Real-world booking logic

---
