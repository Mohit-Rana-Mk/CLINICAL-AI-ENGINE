import logging
import time
import uuid


from app.ai_engine.pipeline import ClinicalPipeline



logger = logging.getLogger(__name__)




class ClinicalAIEngine:


    """
    Main orchestration layer for Clinical AI Engine.

    Responsibilities:
    - Receive clinical requests
    - Manage pipeline execution
    - Track execution metadata
    - Handle failures safely
    """



    def __init__(self):

        logger.info(
            "Initializing Clinical AI Orchestrator"
        )


        self.pipeline = ClinicalPipeline()





    def process(
        self,
        message: str,
        patient_id: int | None = None,
    ):


        request_id = str(
            uuid.uuid4()
        )


        start_time = time.time()



        logger.info(
            f"[{request_id}] Clinical analysis started"
        )



        try:


            result = self.pipeline.run(

                message=message,

                patient_id=patient_id

            )



            execution_time = round(

                time.time() - start_time,

                3

            )



            logger.info(

                f"[{request_id}] "
                f"Pipeline completed in {execution_time}s"

            )



            allowed_response_fields = {

    "status",

    "patient_context",

    "entities",

    "rag_documents",

    "rag_citations",

    "emergency",

    "follow_up_questions",

    "risk_assessment",

    "recommendation",

    "medication_alerts",

    "explanation",

    "clinical_summary",

    "confidence"

}


            safe_result = {

                key: value

                for key, value in result.items()

                if key in allowed_response_fields

            }



            return {

                "request_id": request_id,

                "execution_time_seconds": execution_time,

                **safe_result

            }


        except Exception as error:



            execution_time = round(

                time.time() - start_time,

                3

            )



            logger.exception(

                f"[{request_id}] "
                "Clinical AI execution failed"

            )



            return {


                "status": "error",


                "request_id": request_id,


                "execution_time_seconds":
                    execution_time,


                "message":
                    str(error)

            }