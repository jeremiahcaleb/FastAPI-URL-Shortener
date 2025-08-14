# 🔗 FastAPI URL Shortener

A modern, secure, and production-ready URL Shortener API built with **FastAPI**, **JWT authentication**, and **SQLAlchemy**. Includes support for **Docker**, **PostgreSQL**, and an optional test user for development.

---

## 🚀 Features

- 🔐 JWT-based user authentication (login, update, delete)
- 📦 Modular FastAPI architecture (`users`, `urls`, `auth` modules)
- 🔗 Create, update, delete, and redirect short URLs
- 🧑‍💻 Authenticated user access to their URLs
- 🧪 API versioning and optional test user support
- 📊 Scalable structure for monolith or microservices
- 🐳 Docker + PostgreSQL support for production
---

## 🛠️ Getting Started

### 🔧 Prerequisites

- Python 3.11+
- `pip` or `poetry`
- [Docker (optional)](https://www.docker.com/)

---

### 📦 Local Setup (SQLite)

#### 1. Clone the repo
```bash
git clone https://github.com/jeremiahcaleb/FastAPI-URL-Shortener.git
cd FastAPI-URL-Shortener
```
#### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```
#### 3. Install dependencies
```bash
pip install -r requirements.txt
```
#### 4. Run the app
```bash
uvicorn app.main:app --reload
```

> App will be available at:
>
> * [http://127.0.0.1:8000](http://127.0.0.1:8000)
> * Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
> * ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### ⚙️ `.env` Configuration

Create a `.env` file in the root directory:

```env
# API Settings
URL_PREFIX=/api

# JWT Auth
SECRET_KEY=your-very-secure-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SQLite (for development)
DATABASE_PROTOCOL=sqlite
DATABASE_NAME=url_shortner.db
```

Generate a secure `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

## 🏁 Running the App

### 🔐 Authentication

**Token Endpoint**: `POST /auth/token`

**Request Body (form-data):**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

Use the token in headers:

```
Authorization: Bearer <token>
```

---

## 📡 API Endpoints

### 👤 User Endpoints

| Method | Path      | Description           |
| ------ | --------- | --------------------- |
| POST   | /users    | Create a new user     |
| GET    | /users/me | Get current user info |
| PUT    | /users/me | Update current user   |
| DELETE | /users/me | Delete current user   |

---

### 🔗 URL Endpoints

| Method | Path                       | Description                  |
| ------ | -------------------------- | ---------------------------- |
| POST   | /urls/create\_short\_url   | Create a short URL           |
| GET    | /urls/{short\_url}         | Redirect to long URL         |
| GET    | /urls/{short\_url}/details | Get short URL details        |
| GET    | /urls                      | List user’s URLs             |
| PUT    | /urls/{short\_url}         | Update short URL             |
| DELETE | /urls/{short\_url}         | Delete short URL             |

---

## 🛡️ Security Best Practices

* Use **HTTPS** in production
* Rotate your `SECRET_KEY` regularly
* Prefer **PostgreSQL/MySQL** over SQLite for production
* Never commit `.env` or secrets to version control

---

## 🐳 Run with Docker + PostgreSQL (Optional)

### 1. Update `.env` for PostgreSQL:

```env
DATABASE_PROTOCOL=postgresql
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOSTNAME=db
DATABASE_PORT=5432
DATABASE_NAME=url_shortener_db
```

### 2. Build and start services:

```bash
docker-compose up --build
```

### 3. Access the API:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Health Check: `GET /api/health`

---

## 🔐 Authentication Flow

1. **Register** a new user: `POST /api/users`
2. **Login** to get token: `POST /api/auth/token`
3. Use token in header:

```
Authorization: Bearer <token>
```

---
