# Deployment Guide

## Requirements

- Python 3.12+
- MySQL 8+
- Git
- Virtual Environment

---

## Installation

Clone the repository:

```bash
git clone <repository_url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Update the `.env` file with:

- MYSQL_HOST
- MYSQL_PORT
- MYSQL_DATABASE
- MYSQL_USER
- MYSQL_PASSWORD

---

## Database Migration

Run Alembic migrations:

```bash
alembic upgrade head
```

---

## Start Server

```bash
uvicorn app.main:app --reload
```

Server runs at:

```
http://localhost:8000
```

Swagger Documentation:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## Project Stack

- FastAPI
- SQLAlchemy
- MySQL
- Alembic
- Pydantic

---

## Monitoring

- Logging enabled
- Health endpoint available
- Ready endpoint available
- Analytics endpoints available