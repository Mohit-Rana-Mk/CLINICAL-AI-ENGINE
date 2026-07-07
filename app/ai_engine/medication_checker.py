from pydantic import BaseModel


class MedicationAlert(BaseModel):
    has_alert: bool
    alerts: list[str]


class MedicationChecker:

    def check(
        self,
        medications: list[str],
        allergies: list[str]
    ) -> MedicationAlert:

        alerts = []

        meds = [m.lower() for m in medications]
        allergies = [a.lower() for a in allergies]

        if "penicillin" in allergies:
            alerts.append(
                "Patient is allergic to Penicillin."
            )

        if "warfarin" in meds and "aspirin" in meds:
            alerts.append(
                "Warfarin + Aspirin increases bleeding risk."
            )

        if "metformin" in meds:
            alerts.append(
                "Monitor kidney function while taking Metformin."
            )

        if "telmisartan" in meds:
            alerts.append(
                "Monitor blood pressure regularly."
            )

        return MedicationAlert(
            has_alert=len(alerts) > 0,
            alerts=alerts
        )