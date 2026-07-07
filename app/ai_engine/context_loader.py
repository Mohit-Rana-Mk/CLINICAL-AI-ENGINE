from datetime import date

from app.ai_engine.schemas import PatientContext
from app.database.session import SessionLocal
from app.repositories import PatientRepository


class PatientContextLoader:

    def load(self, patient_id: int | None = None):

        if patient_id is None:

            return PatientContext(
                patient_id=None,
                age=None,
                gender=None,
                medical_history=[],
                medications=[],
                allergies=[],
                vitals={},
                lab_reports={}
            )

        db = SessionLocal()

        try:

            repo = PatientRepository(db)

            patient = repo.get_patient(patient_id)

            if patient["user"] is None:

                return PatientContext(
                    patient_id=patient_id,
                    age=None,
                    gender=None,
                    medical_history=[],
                    medications=[],
                    allergies=[],
                    vitals={},
                    lab_reports={}
                )

            dob = patient["profile"].date_of_birth

            today = date.today()

            age = (
                today.year
                - dob.year
                - ((today.month, today.day) < (dob.month, dob.day))
            )

            return PatientContext(

                patient_id=patient["user"].id,

                age=age,

                gender=patient["profile"].gender,

                medical_history=[
                    h.disease
                    for h in patient["history"]
                ],

                medications=[
                    m.medicine_name
                    for m in patient["medications"]
                ],

                allergies=[
                    a.allergen
                    for a in patient["allergies"]
                ],

                vitals={
                    "temperature": patient["vitals"].temperature if patient["vitals"] else None,
                    "pulse": patient["vitals"].pulse if patient["vitals"] else None,
                    "spo2": patient["vitals"].spo2 if patient["vitals"] else None,
                    "blood_pressure":
                        f"{patient['vitals'].systolic_bp}/{patient['vitals'].diastolic_bp}"
                        if patient["vitals"] else None
                },

                lab_reports={
                    "hba1c": patient["labs"].hba1c if patient["labs"] else None,
                    "glucose": patient["labs"].glucose if patient["labs"] else None,
                    "hemoglobin": patient["labs"].hemoglobin if patient["labs"] else None
                }

            )

        finally:

            db.close()