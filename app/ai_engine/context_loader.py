import logging
from datetime import date

from app.ai_engine.schemas import PatientContext
from app.database.session import SessionLocal
from app.repositories import PatientRepository

logger = logging.getLogger(__name__)


class PatientContextLoader:
    """
    Production Patient Context Loader.

    Responsibilities
    ----------------
    - Load patient demographic information
    - Load medical history
    - Load medications
    - Load allergies
    - Load vitals
    - Load laboratory reports
    - Never crash the AI pipeline
    """

    def load(
        self,
        patient_id: int | None = None,
    ) -> PatientContext:

        if patient_id is None:

            logger.info(
                "Anonymous patient request."
            )

            return PatientContext()

        db = SessionLocal()

        try:

            repository = PatientRepository(db)

            patient = repository.get_patient(
                patient_id
            )

            if (
                patient is None
                or patient.get("user") is None
            ):

                logger.warning(
                    "Patient %s not found.",
                    patient_id,
                )

                return PatientContext(
                    patient_id=patient_id
                )

            user = patient.get("user")
            profile = patient.get("profile")
            vitals = patient.get("vitals")
            labs = patient.get("labs")

            # ----------------------------------
            # Calculate Age
            # ----------------------------------

            age = None

            if (
                profile
                and profile.date_of_birth
            ):

                today = date.today()

                dob = profile.date_of_birth

                age = (
                    today.year
                    - dob.year
                    - (
                        (today.month, today.day)
                        < (dob.month, dob.day)
                    )
                )

            # ----------------------------------
            # Medical History
            # ----------------------------------

            medical_history = sorted(
                list(
                    {
                        item.disease
                        for item in patient.get(
                            "history",
                            []
                        )
                        if getattr(
                            item,
                            "disease",
                            None,
                        )
                    }
                )
            )

            # ----------------------------------
            # Medications
            # ----------------------------------

            medications = sorted(
                list(
                    {
                        item.medicine_name
                        for item in patient.get(
                            "medications",
                            []
                        )
                        if getattr(
                            item,
                            "medicine_name",
                            None,
                        )
                    }
                )
            )

            # ----------------------------------
            # Allergies
            # ----------------------------------

            allergies = sorted(
                list(
                    {
                        item.allergen
                        for item in patient.get(
                            "allergies",
                            []
                        )
                        if getattr(
                            item,
                            "allergen",
                            None,
                        )
                    }
                )
            )

            # ----------------------------------
            # Vitals
            # ----------------------------------

            vitals_data = {

                "temperature": getattr(
                    vitals,
                    "temperature",
                    None,
                ),

                "pulse": getattr(
                    vitals,
                    "pulse",
                    None,
                ),

                "spo2": getattr(
                    vitals,
                    "spo2",
                    None,
                ),

                "blood_pressure": (
                    f"{vitals.systolic_bp}/{vitals.diastolic_bp}"
                    if (
                        vitals
                        and getattr(
                            vitals,
                            "systolic_bp",
                            None,
                        )
                        is not None
                        and getattr(
                            vitals,
                            "diastolic_bp",
                            None,
                        )
                        is not None
                    )
                    else None
                ),
            }

            # ----------------------------------
            # Laboratory Reports
            # ----------------------------------

            laboratory_data = {

                "hba1c": getattr(
                    labs,
                    "hba1c",
                    None,
                ),

                "glucose": getattr(
                    labs,
                    "glucose",
                    None,
                ),

                "hemoglobin": getattr(
                    labs,
                    "hemoglobin",
                    None,
                ),
            }

            context = PatientContext(

    patient_id=getattr(
        user,
        "id",
        patient_id,
    ),

    age=age,

    gender=getattr(
        profile,
        "gender",
        None,
    ),

    bmi=getattr(
        vitals,
        "bmi",
        None,
    ),

    blood_group=getattr(
        profile,
        "blood_group",
        None,
    ),

    lifestyle=getattr(
        profile,
        "lifestyle",
        None,
    ),

    smoking_status=getattr(
        profile,
        "smoking_status",
        None,
    ),

    alcohol_use=getattr(
        profile,
        "alcohol_use",
        None,
    ),

    occupation=getattr(
        profile,
        "occupation",
        None,
    ),

    medical_history=medical_history,

    medications=medications,

    allergies=allergies,

    vitals=vitals_data,

    lab_reports=laboratory_data,
)

            logger.info(
                "Patient context loaded successfully."
            )

            return context

        except Exception:

            logger.exception(
                "Failed to load patient context."
            )

            return PatientContext(
                patient_id=patient_id
            )

        finally:

            db.close()