import logging


from app.ai_engine.agents.symptom_agent import SymptomAgent
from app.ai_engine.agents.emergency_agent import EmergencyAgent
from app.ai_engine.agents.medication_agent import MedicationAgent
from app.ai_engine.agents.diagnosis_agent import DiagnosisAgent
from app.ai_engine.agents.recommendation_agent import RecommendationAgent


logger = logging.getLogger(__name__)



class AgentCoordinator:


    """
    Coordinates multi-agent clinical reasoning.

    Workflow:

    Symptom Agent
          ↓
    Emergency Agent
          ↓
    Medication Agent
          ↓
    Diagnosis Agent
          ↓
    Recommendation Agent

    """



    def __init__(self):

        self.symptom_agent = SymptomAgent()

        self.emergency_agent = EmergencyAgent()

        self.medication_agent = MedicationAgent()

        self.diagnosis_agent = DiagnosisAgent()

        self.recommendation_agent = RecommendationAgent()



    def run(
        self,
        message,
        patient_context,
        entities,
        rag_result,
    ):


        logger.info(
            "========== Multi Agent Pipeline Started =========="
        )


        result = {}



        # ---------------------------------
        # Symptom Agent
        # ---------------------------------

        try:

            result["symptom_analysis"] = (
                self.symptom_agent.run(
                    message=message,
                    entities=entities
                )
            )

        except Exception as error:

            logger.exception(
                "Symptom Agent Failed"
            )

            result["symptom_analysis"] = {
                "status": "error",
                "message": str(error)
            }



        # ---------------------------------
        # Emergency Agent
        # ---------------------------------

        try:

            result["emergency_analysis"] = (
                self.emergency_agent.run(
                    symptoms=entities.symptoms
                )
            )


        except Exception as error:

            logger.exception(
                "Emergency Agent Failed"
            )

            result["emergency_analysis"] = {
                "status": "error",
                "message": str(error)
            }



        # ---------------------------------
        # Medication Agent
        # ---------------------------------

        try:

            result["medication_analysis"] = (
                self.medication_agent.run(
                    medications=patient_context.medications,
                    allergies=patient_context.allergies
                )
            )


        except Exception as error:

            logger.exception(
                "Medication Agent Failed"
            )

            result["medication_analysis"] = {
                "status": "error",
                "message": str(error)
            }




        # ---------------------------------
        # Diagnosis Agent
        # ---------------------------------

        try:

            result["diagnosis_analysis"] = (
                self.diagnosis_agent.run(

                    symptoms=entities.symptoms,

                    rag_result=rag_result,

                    patient_context=patient_context

                )
            )


        except Exception as error:

            logger.exception(
                "Diagnosis Agent Failed"
            )

            result["diagnosis_analysis"] = {
                "status": "error",
                "message": str(error)
            }




        # ---------------------------------
        # Recommendation Agent
        # ---------------------------------

        try:

            result["recommendation_analysis"] = (
                self.recommendation_agent.run(

                    diagnosis=result.get(
                        "diagnosis_analysis"
                    ),

                    emergency=result.get(
                        "emergency_analysis"
                    ),

                    patient_context=patient_context

                )
            )


        except Exception as error:

            logger.exception(
                "Recommendation Agent Failed"
            )

            result["recommendation_analysis"] = {
                "status": "error",
                "message": str(error)
            }



        logger.info(
            "========== Multi Agent Pipeline Completed =========="
        )


        return result