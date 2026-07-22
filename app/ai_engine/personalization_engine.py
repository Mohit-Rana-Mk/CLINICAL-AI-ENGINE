import logging

logger = logging.getLogger(__name__)


class PersonalizationEngine:
    """
    Generates personalized clinical response
    using patient profile and memory.
    """

    def generate(
        self,
        patient_context=None,
        patient_memory=None,
    ) -> dict:
        """
        Generate personalization signals.

        Inputs:
        - patient_context
        - patient_memory

        Output:
        personalization preferences
        """

        personalization = {
            "patient_summary": None,
            "communication_style": "simple",
            "consider_previous_history": True,
            "risk_awareness": False,
            "recommendation_focus": [],
            "memory_available": False,
        }


        # Context based personalization

        if patient_context:

            personalization[
                "patient_summary"
            ] = getattr(
                patient_context,
                "summary",
                None,
            )


            diagnoses = getattr(
                patient_context,
                "diagnoses",
                []
            )

            if diagnoses:
                personalization[
                    "recommendation_focus"
                ] = diagnoses



            risk_history = getattr(
                patient_context,
                "risk_history",
                []
            )

            if risk_history:

                personalization[
                    "risk_awareness"
                ] = True



        # Memory based personalization

        if patient_memory:

            personalization[
                "memory_available"
            ] = True


            previous_diagnosis = (
                patient_memory.get(
                    "diagnoses",
                    []
                )
            )


            if previous_diagnosis:

                personalization[
                    "recommendation_focus"
                ].extend(
                    previous_diagnosis
                )


            previous_risk = (
                patient_memory.get(
                    "risk_history",
                    []
                )
            )


            if previous_risk:

                personalization[
                    "risk_awareness"
                ] = True



        logger.info(
            "Personalization generated"
        )


        return personalization