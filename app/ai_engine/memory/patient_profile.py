import logging
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PatientProfile(BaseModel):
    """
    Longitudinal patient profile used for
    personalization across the Clinical AI Engine.
    """

    patient_id: int | None = None

    age: int | None = None

    gender: str | None = None

    bmi: float | None = None

    blood_group: str | None = None

    lifestyle: str | None = None

    smoking_status: str | None = None

    alcohol_use: str | None = None

    occupation: str | None = None

    family_history: list[str] = Field(default_factory=list)

    medical_history: list[str] = Field(default_factory=list)

    medications: list[str] = Field(default_factory=list)

    allergies: list[str] = Field(default_factory=list)

    previous_risk_scores: list[dict[str, Any]] = Field(
        default_factory=list
    )

    previous_reports: list[dict[str, Any]] = Field(
        default_factory=list
    )

    previous_diagnoses: list[str] = Field(
        default_factory=list
    )

    previous_symptoms: list[str] = Field(
        default_factory=list
    )

    def build_summary(self) -> dict[str, Any]:

        return {

            "patient_id": self.patient_id,

            "age": self.age,

            "gender": self.gender,

            "medical_history": self.medical_history,

            "family_history": self.family_history,

            "allergies": self.allergies,

            "medications": self.medications,

            "bmi": self.bmi,

            "blood_group": self.blood_group,

            "lifestyle": self.lifestyle,

            "smoking_status": self.smoking_status,

            "alcohol_use": self.alcohol_use,

            "occupation": self.occupation,

            "risk_records": len(
                self.previous_risk_scores
            ),

            "reports": len(
                self.previous_reports
            ),

            "diagnoses": len(
                self.previous_diagnoses
            ),
        }

    def update_from_context(
        self,
        patient_context,
    ):

        if patient_context is None:
            return

        self.patient_id = getattr(
            patient_context,
            "patient_id",
            self.patient_id,
        )

        self.age = getattr(
            patient_context,
            "age",
            self.age,
        )

        self.gender = getattr(
            patient_context,
            "gender",
            self.gender,
        )

        self.bmi = getattr(
            patient_context,
            "bmi",
            self.bmi,
        )

        self.blood_group = getattr(
            patient_context,
            "blood_group",
            self.blood_group,
        )

        self.lifestyle = getattr(
            patient_context,
            "lifestyle",
            self.lifestyle,
        )

        self.smoking_status = getattr(
            patient_context,
            "smoking_status",
            self.smoking_status,
        )

        self.alcohol_use = getattr(
            patient_context,
            "alcohol_use",
            self.alcohol_use,
        )

        self.occupation = getattr(
            patient_context,
            "occupation",
            self.occupation,
        )       

        self.medical_history = sorted(
            set(
                self.medical_history
                + getattr(
                    patient_context,
                    "medical_history",
                    [],
                )
            )
        )

        self.medications = sorted(
            set(
                self.medications
                + getattr(
                    patient_context,
                    "medications",
                    [],
                )
            )
        )

        self.allergies = sorted(
            set(
                self.allergies
                + getattr(
                    patient_context,
                    "allergies",
                    [],
                )
            )
        )

        logger.info(
            "Patient profile updated | patient=%s",
            self.patient_id,
        )