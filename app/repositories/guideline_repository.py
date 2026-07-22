from sqlalchemy.orm import Session

class GuidelineRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_guidelines(self):
        return []

    def get_guideline_by_specialty(self, specialty: str):
        return []

    def get_latest_guidelines(self):
        return []