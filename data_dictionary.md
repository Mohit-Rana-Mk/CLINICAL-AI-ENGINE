# Data Dictionary

## Overview
This document defines the fields, types, and meaning of data stored across the Medical Knowledge Platform's datasets and tables.

---

## Diseases

| Field | Type | Description |
|-------|------|-------------|
| Disease Name | String | Name of the disease |
| Specialty | String | Medical specialty (e.g., Cardiology, Dermatology) |
| Description | Text | Brief overview of the disease |
| Causes | Text | Known causes |
| Risk Factors | Text | Factors that increase likelihood |
| Symptoms | Text | Common symptoms |
| Emergency Signs | Text | Signs requiring urgent care |
| Diagnosis | Text | How the disease is diagnosed |
| Treatment | Text | Standard treatment approach |
| Complications | Text | Possible complications |
| Prevention | Text | Preventive measures |
| References | Text | Source citation |
| Last Updated | Date | Date of last update |

---

## Medicines

| Field | Type | Description |
|-------|------|-------------|
| Medicine Name | String | Name of the medicine |
| Generic Name | String | Generic/chemical name |
| Brand Name | String | Commercial brand name |
| Dose | String | Standard dosage |
| Frequency | String | How often it is taken |
| Route | String | Administration route (oral, IV, etc.) |
| Side Effects | Text | Known side effects |
| Contraindications | Text | Conditions where use is discouraged |
| Drug Interactions | Text | Known interactions with other drugs |
| Pregnancy Safety | String | Safety classification during pregnancy |
| Storage | String | Storage requirements |
| Reference | Text | Source citation |

---

## Lab References

| Field | Type | Description |
|-------|------|-------------|
| Test Name | String | Name of the lab test |
| Normal Range | String | Standard normal range |
| Borderline Range | String | Borderline/at-risk range |
| High Range | String | High/abnormal range |
| Critical Range | String | Critical/emergency range |
| Unit | String | Unit of measurement |
| Age-specific Range | String | Range variation by age |
| Gender-specific Range | String | Range variation by gender |

---

## Medical Images

| Field | Type | Description |
|-------|------|-------------|
| Image ID | String | Unique identifier |
| Disease | String | Associated disease/condition |
| Category | String | Image category (skin, eye, wound, etc.) |
| Body Part | String | Body part depicted |
| Severity | String | Severity level, if applicable |
| Source | String | Origin of the image |
| License | String | Usage license |
| Resolution | String | Image resolution |
| Annotation Status | String | Whether the image has been annotated |

---

## Clinical Guidelines

| Field | Type | Description |
|-------|------|-------------|
| Title | String | Guideline title |
| Specialty | String | Associated medical specialty |
| Language | String | Document language |
| Publication Year | Integer | Year originally published |
| Version Year | Integer | Year of this version |
| Source | String | Publishing organization (WHO, NICE, CDC, etc.) |
| File Path | String | Path to the guideline document |

---

## Governance Metadata

| Field | Type | Description |
|-------|------|-------------|
| Source | String | Data source name |
| Version | String | Version identifier |
| Publication Date | Date | Date the source was published |
| Last Updated | Date | Date the record was last modified |
| Reviewed By | String | Reviewer name/role |
| Approval Status | String | Approval state (approved, pending, rejected) |
