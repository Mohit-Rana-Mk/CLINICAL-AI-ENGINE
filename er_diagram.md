# Entity Relationship Diagram (ER Diagram)

## Database Entities

The Clinical AI Engine database consists of the following primary entities:

- Patients
- Diseases
- Medicines
- Lab References
- Medical Images
- Clinical Guidelines

---

## Relationships

Patients
│
├── Medical History
├── Diseases
├── Medicines
└── Lab Reports

Diseases
│
├── Symptoms
├── Treatments
└── Clinical Guidelines

Medicines
│
├── Drug Class
├── Generic Name
└── Side Effects

Lab References
│
├── Test Name
├── Normal Range
└── Units

Medical Images
│
├── Image Metadata
├── Body Part
└── Diagnosis

Clinical Guidelines
│
├── Specialty
├── Version
└── Publication Date

---

## Database Design

The project follows a relational database architecture using:

- MySQL
- SQLAlchemy ORM
- Repository Pattern
- Alembic Database Migrations

The repository layer provides an abstraction between the API routes and database models, ensuring maintainable and scalable database operations.