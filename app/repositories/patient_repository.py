from sqlalchemy.orm import Session

from app.models.user import User
from app.models.patient_profile import PatientProfile
from app.models.medical_history import MedicalHistory
from app.models.medication import Medication
from app.models.allergy import Allergy
from app.models.vital import Vital
from app.models.lab_report import LabReport


class PatientRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_patient(self, patient_id: int):

        user = (
            self.db.query(User)
            .filter(User.id == patient_id)
            .first()
        )

        profile = (
            self.db.query(PatientProfile)
            .filter(PatientProfile.user_id == patient_id)
            .first()
        )

        history = (
            self.db.query(MedicalHistory)
            .filter(MedicalHistory.patient_id == patient_id)
            .all()
        )

        medications = (
            self.db.query(Medication)
            .filter(Medication.patient_id == patient_id)
            .all()
        )

        allergies = (
            self.db.query(Allergy)
            .filter(Allergy.patient_id == patient_id)
            .all()
        )

        vitals = (
            self.db.query(Vital)
            .filter(Vital.patient_id == patient_id)
            .first()
        )

        labs = (
            self.db.query(LabReport)
            .filter(LabReport.patient_id == patient_id)
            .first()
        )

        return {
            "user": user,
            "profile": profile,
            "history": history,
            "medications": medications,
            "allergies": allergies,
            "vitals": vitals,
            "labs": labs
        }