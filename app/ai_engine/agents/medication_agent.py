import logging

logger = logging.getLogger(__name__)


class MedicationAgent:
    """
    Production Medication Safety Agent.

    Responsibilities
    ----------------
    - Allergy checking
    - Drug interaction detection
    - Medication monitoring
    - Safety alerts
    """

    MONITORING_RULES = {
        "metformin": {
            "severity": "MEDIUM",
            "message": "Monitor renal function and vitamin B12 during long-term therapy.",
        },
        "telmisartan": {
            "severity": "MEDIUM",
            "message": "Monitor blood pressure, renal function and serum potassium.",
        },
        "insulin": {
            "severity": "HIGH",
            "message": "Monitor blood glucose closely to reduce hypoglycemia risk.",
        },
        "warfarin": {
            "severity": "HIGH",
            "message": "Regular INR monitoring is recommended.",
        },
        "prednisolone": {
            "severity": "MEDIUM",
            "message": "Long-term corticosteroid therapy requires monitoring.",
        },
    }

    INTERACTION_RULES = [
        {
            "drugs": {"warfarin", "aspirin"},
            "severity": "HIGH",
            "message": "Concurrent use may significantly increase bleeding risk.",
        },
        {
            "drugs": {"warfarin", "ibuprofen"},
            "severity": "HIGH",
            "message": "Concurrent use increases gastrointestinal bleeding risk.",
        },
        {
            "drugs": {"metformin", "contrast dye"},
            "severity": "MEDIUM",
            "message": "Temporary discontinuation may be required before contrast imaging.",
        },
    ]

    def run(
        self,
        medications: list[str],
        allergies: list[str],
    ):

        logger.info("Running Medication Agent")

        alerts = []

        normalized_meds = {
            med.lower().strip()
            for med in medications
        }

        normalized_allergies = {
            allergy.lower().strip()
            for allergy in allergies
        }

        # ======================================
        # Allergy Alerts
        # ======================================

        for allergy in sorted(normalized_allergies):

            alerts.append(
                {
                    "medication": allergy.title(),
                    "alert_type": "Allergy",
                    "severity": "HIGH",
                    "message": f"Patient has documented allergy to {allergy.title()}.",
                    "source": "Patient Allergy Records",
                }
            )

        # ======================================
        # Medication Monitoring
        # ======================================

        for medicine in normalized_meds:

            if medicine in self.MONITORING_RULES:

                rule = self.MONITORING_RULES[medicine]

                alerts.append(
                    {
                        "medication": medicine.title(),
                        "alert_type": "Monitoring",
                        "severity": rule["severity"],
                        "message": rule["message"],
                        "source": "Clinical Medication Rules",
                    }
                )

        # ======================================
        # Drug Interactions
        # ======================================

        for interaction in self.INTERACTION_RULES:

            if interaction["drugs"].issubset(normalized_meds):

                alerts.append(
                    {
                        "medication": " + ".join(
                            sorted(
                                drug.title()
                                for drug in interaction["drugs"]
                            )
                        ),
                        "alert_type": "Drug Interaction",
                        "severity": interaction["severity"],
                        "message": interaction["message"],
                        "source": "Clinical Medication Rules",
                    }
                )

        # ======================================
        # Remove Duplicate Alerts
        # ======================================

        unique = []

        seen = set()

        for alert in alerts:

            key = (
                alert["medication"],
                alert["alert_type"],
                alert["message"],
            )

            if key not in seen:
                seen.add(key)
                unique.append(alert)

        return {
            "has_alert": len(unique) > 0,
            "alert_count": len(unique),
            "alerts": unique,
            "summary": self._generate_summary(unique),
        }

    def _generate_summary(
        self,
        alerts,
    ):

        if not alerts:
            return "No medication safety alerts detected."

        high = sum(
            1
            for alert in alerts
            if alert["severity"] == "HIGH"
        )

        medium = sum(
            1
            for alert in alerts
            if alert["severity"] == "MEDIUM"
        )

        return (
            f"{len(alerts)} medication alert(s) detected "
            f"({high} HIGH, {medium} MEDIUM). "
            "Clinical review is recommended before prescribing."
        )