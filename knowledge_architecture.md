# Knowledge Architecture

## Overview
This document describes how the Medical Knowledge Platform is structured and how data flows from trusted sources to the AI Engine.

---

## Architecture Flow

Patient
  |
  v
HealTrack Backend
  |
  v
Medical Knowledge Platform
  |
  +-- Disease Database
  +-- Medicine Database
  +-- Lab Reference Database
  +-- Clinical Guidelines
  +-- Medical Image Dataset
  +-- Medical Documents
  |
  v
Mohit's AI Engine
  |
  v
Clinical Response

---

## Layers

### 1. Knowledge Base Layer
Stores raw structured and unstructured clinical knowledge collected from trusted sources (WHO, CDC, ICMR, NICE, PubMed, FDA, government health portals), organized by medical specialty.

### 2. Dataset Layer
CSV datasets that normalize knowledge base content into structured records: diseases, medicines, lab references, medical images, and clinical guidelines.

### 3. Repository Layer
Python repository classes (DiseaseRepository, MedicineRepository, LabRepository, GuidelineRepository, ImageRepository) that provide CRUD access to the underlying data for the rest of the application.

### 4. API Layer
FastAPI routes (/diseases, /medicines, /lab-reference, /guidelines, /knowledge, /medical-images, /analytics) that expose repository data over REST endpoints.

### 5. Governance Layer
Tracks source, version, and approval status of every piece of knowledge (source_tracker.py, version_manager.py, audit_reports.py), and validates dataset integrity (dataset_validator.py, quality_checker.py).

### 6. Analytics & Monitoring Layer
Tracks dataset health, coverage, and quality over time (dashboard_metrics.py, dataset_monitor.py, knowledge_health.py, update_scheduler.py).

---

## Design Principle

The AI Engine should never rely solely on an LLM or hardcoded rules. Every clinical response is grounded in validated, source-tracked medical knowledge retrieved through the repository layer, ensuring accuracy, traceability, and trust.
