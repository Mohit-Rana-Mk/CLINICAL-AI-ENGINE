import logging
from collections import defaultdict
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class PatientMemory:
    """
    Persistent Patient Memory.

    Stores longitudinal clinical information gathered
    during AI conversations.

    Future Storage
    --------------
    - PostgreSQL
    - Redis
    - MongoDB
    """

    def __init__(self):

        self._patients = defaultdict(
            lambda: {
                "symptoms": [],
                "diagnoses": [],
                "medications": [],
                "allergies": [],
                "risk_history": [],
                "recommendations": [],
                "follow_ups": [],
                "visit_history": [],
                "last_updated": None,
            }
        )

    def update(
        self,
        patient_id: int | None,
        *,
        symptoms=None,
        diagnosis=None,
        medications=None,
        allergies=None,
        risk=None,
        recommendation=None,
        follow_up=None,
    ):

        if patient_id is None:
            patient_id = 0

        patient = self._patients[patient_id]

        if symptoms:
            patient["symptoms"].extend(
                symptom.strip()
                for symptom in symptoms
                if symptom and symptom.strip()
        )

        if diagnosis:
            patient["diagnoses"].append(
                diagnosis
            )

        if medications:
            patient["medications"].extend(
                medication.strip()
                for medication in medications
                if medication and medication.strip()
        )

        if allergies:
            patient["allergies"].extend(
                allergy.strip()
                for allergy in allergies
                if allergy and allergy.strip()
        )

        if risk:
            patient["risk_history"].append(
                risk.model_dump()
                if hasattr(risk, "model_dump")
                else risk
            )

        if recommendation:
            patient["recommendations"].append(
                recommendation.model_dump()
                if hasattr(recommendation, "model_dump")
                else recommendation
            )

        if follow_up:
            patient["follow_ups"].append(
                follow_up
            )


        # Remove duplicate values
        patient["symptoms"] = sorted(
            set(patient["symptoms"])
        )

        patient["medications"] = sorted(
            set(patient["medications"])
        )

        patient["allergies"] = sorted(
            set(patient["allergies"])
        )


        # Create longitudinal visit event

        patient["visit_history"].append(
            {
                "visit_date": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "symptoms": symptoms,
                "diagnosis": diagnosis,
                "risk": risk,
                "recommendation": recommendation,
                "medications": medications,
                "follow_up": follow_up,
            }
        )


        patient["last_updated"] = (
            datetime.utcnow().isoformat(timespec="seconds") + "Z"
        )


        logger.info(
            "Patient memory updated | patient=%s",
            patient_id,
        )


    def get(
        self,
        patient_id: int | None,
    ) -> dict[str, Any]:

        if patient_id is None:
            patient_id = 0

        return self._patients[patient_id]


    def clear(
        self,
        patient_id: int | None,
    ):

        if patient_id is None:
            patient_id = 0

        self._patients.pop(
            patient_id,
            None,
        )

        logger.info(
            "Patient memory cleared | patient=%s",
            patient_id,
        )


    def exists(
        self,
        patient_id: int | None,
    ) -> bool:

        if patient_id is None:
            patient_id = 0

        return patient_id in self._patients


    def summary(
        self,
        patient_id: int | None,
    ) -> dict:

        patient = self.get(
            patient_id
        )

        return {
            "symptom_count": len(
                patient["symptoms"]
            ),

            "diagnosis_count": len(
                patient["diagnoses"]
            ),

            "medication_count": len(
                patient["medications"]
            ),

            "allergy_count": len(
                patient["allergies"]
            ),

            "risk_count": len(
                patient["risk_history"]
            ),

            "follow_up_count": len(
                patient["follow_ups"]
            ),

            "visit_count": len(
                patient["visit_history"]
            ),

            "last_updated": patient[
                "last_updated"
            ],
        }