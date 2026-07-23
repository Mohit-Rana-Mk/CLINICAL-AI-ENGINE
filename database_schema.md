# Database Schema

## Overview

The Clinical AI Engine uses a MySQL relational database managed through SQLAlchemy ORM and Alembic migrations.

The database stores structured clinical knowledge, patient information, and reference datasets required by the AI engine.

---

# Core Tables

## Patients

Stores patient demographic and medical information.

| Column | Type |
|---------|------|
| id | Integer |
| full_name | String |
| age | Integer |
| gender | String |
| blood_group | String |
| allergies | Text |
| medical_history | Text |

---

## Diseases

Stores disease reference information.

| Column | Type |
|---------|------|
| id | Integer |
| name | String |
| category | String |
| severity_level | String |
| symptoms | Text |
| causes | Text |
| treatment | Text |

---

## Medicines

Stores medicine information.

| Column | Type |
|---------|------|
| id | Integer |
| name | String |
| generic_name | String |
| drug_class | String |
| dosage | String |
| side_effects | Text |
| contraindications | Text |

---

## Lab References

Stores laboratory reference ranges.

| Column | Type |
|---------|------|
| id | Integer |
| test_name | String |
| normal_range | String |
| unit | String |
| gender_specific | String |

---

## Medical Images

Stores metadata for medical imaging resources.

| Column | Type |
|---------|------|
| id | Integer |
| image_name | String |
| modality | String |
| body_part | String |
| diagnosis | String |
| file_path | String |

---

## Clinical Guidelines

Stores guideline information for clinical decision support.

| Column | Type |
|---------|------|
| id | Integer |
| title | String |
| specialty | String |
| version | String |
| publication_date | Date |

---

# Relationships

- Patients are linked to medical history.
- Diseases are referenced during clinical reasoning.
- Medicines support medication safety analysis.
- Lab references assist interpretation of laboratory results.
- Medical images support multimodal clinical reasoning.
- Clinical guidelines provide evidence-based recommendations.

---

# Database Technologies

- MySQL
- SQLAlchemy ORM
- Alembic Migrations
- Repository Pattern