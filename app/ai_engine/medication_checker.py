from app.ai_engine.schemas import (
    MedicationAlert,
    MedicationAlertItem,
)


class MedicationChecker:


    def check(
        self,
        medications: list[str],
        allergies: list[str]
    ) -> MedicationAlert:


        alerts: list[MedicationAlertItem] = []


        meds = [
            medication.lower()
            for medication in medications
        ]


        allergy_list = [
            allergy.lower()
            for allergy in allergies
        ]


        # -------------------------------
        # Allergy Check
        # -------------------------------

        if "penicillin" in allergy_list:

            alerts.append(

                MedicationAlertItem(

                    medication="Penicillin",

                    alert_type="Allergy",

                    severity="HIGH",

                    message=(
                        "Patient has documented "
                        "Penicillin allergy."
                    ),

                    source="Patient Allergy Records"

                )

            )


        # -------------------------------
        # Drug Interaction Check
        # -------------------------------

        if (
            "warfarin" in meds
            and "aspirin" in meds
        ):

            alerts.append(

                MedicationAlertItem(

                    medication=(
                        "Warfarin + Aspirin"
                    ),

                    alert_type="Drug Interaction",

                    severity="HIGH",

                    message=(
                        "Combined use may increase "
                        "bleeding risk."
                    ),

                    source="Clinical Medication Rules"

                )

            )


        # -------------------------------
        # Metformin Monitoring
        # -------------------------------

        if "metformin" in meds:

            alerts.append(

                MedicationAlertItem(

                    medication="Metformin",

                    alert_type="Monitoring",

                    severity="MEDIUM",

                    message=(
                        "Renal function monitoring "
                        "should be considered."
                    ),

                    source="Clinical Medication Rules"

                )

            )


        # -------------------------------
        # Telmisartan Monitoring
        # -------------------------------

        if "telmisartan" in meds:

            alerts.append(

                MedicationAlertItem(

                    medication="Telmisartan",

                    alert_type="Monitoring",

                    severity="MEDIUM",

                    message=(
                        "Blood pressure monitoring "
                        "is recommended."
                    ),

                    source="Clinical Medication Rules"

                )

            )


        return MedicationAlert(

            has_alert=len(alerts) > 0,

            alerts=alerts

        )