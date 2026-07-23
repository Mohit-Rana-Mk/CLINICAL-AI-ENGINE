# API Documentation

## Overview

The Clinical AI Engine exposes RESTful APIs built with FastAPI.

These APIs provide access to clinical reasoning, disease information, medicines, laboratory references, medical images, analytics, and clinical knowledge.

---

# Available Endpoints

## System

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Home endpoint |
| /ready | GET | Readiness check |
| /health | GET | Health check |

---

## AI Engine

| Endpoint | Method | Description |
|----------|--------|-------------|
| /ai/test | GET | Test AI engine |
| /ai/analyze | POST | Analyze clinical request |

---

## Disease APIs

- GET /diseases
- GET /diseases/{id}

---

## Medicine APIs

- GET /medicines
- GET /medicines/{id}

---

## Laboratory APIs

- GET /lab-reference

---

## Clinical Guidelines

- GET /guidelines

---

## Medical Images

- GET /medical-images

---

## Analytics

- GET /analytics

---

# Response Format

Successful responses return JSON.

Example:

```json
{
  "status": "success",
  "message": "Request processed successfully"
}
```

Errors return appropriate HTTP status codes.

Examples:

- 400 Bad Request
- 404 Not Found
- 500 Internal Server Error

---

# Technologies

- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- REST Architecture