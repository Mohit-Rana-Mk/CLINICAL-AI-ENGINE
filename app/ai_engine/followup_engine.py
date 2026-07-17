import logging

from app.ai_engine.schemas import FollowUpQuestions

logger = logging.getLogger(__name__)


class FollowUpEngine:
    """
    Production Follow-up Question Engine.

    Generates intelligent follow-up questions using:

    - Symptom specific questions
    - Emergency questions
    - Risk clarification
    - Missing clinical information
    - Priority ordering
    """

    def __init__(self):

        self.question_bank = {

            "chest pain": [
                "On a scale of 1-10, how severe is the chest pain?",
                "Where exactly is the pain located?",
                "Does the pain spread to your left arm, jaw, neck, or back?",
                "Did the pain start suddenly or gradually?",
                "Is the pain constant or intermittent?",
                "Does physical activity worsen the pain?",
                "Do you have sweating, nausea, or dizziness?",
                "Do you have breathing difficulty?",
            ],

            "breathing difficulty": [
                "Did the breathing difficulty begin suddenly?",
                "Does it occur while resting or during activity?",
                "Can you speak full sentences comfortably?",
                "Have you noticed wheezing?",
                "Have your lips or fingertips turned blue?",
                "Have you had asthma or COPD before?",
            ],

            "fever": [
                "What is your highest recorded temperature?",
                "How many days have you had the fever?",
                "Did the fever start suddenly?",
                "Have you experienced chills or shivering?",
                "Have you taken any fever medication?",
                "Have you recently travelled or been around someone who was sick?",
            ],

            "headache": [
                "How severe is the headache on a scale of 1-10?",
                "Did it start suddenly or gradually?",
                "Is it one-sided or across the whole head?",
                "Do you have blurred vision?",
                "Do you have nausea or vomiting?",
                "Do bright lights or loud sounds make it worse?",
                "Is this the worst headache you've ever experienced?",
            ],

            "cough": [
                "Is the cough dry or productive?",
                "How long have you had the cough?",
                "Are you coughing up blood?",
                "Do you have breathing difficulty?",
                "Do you have chest pain while coughing?",
                "Have you recently had a fever?",
            ],

            "abdominal pain": [
                "Where exactly is the abdominal pain located?",
                "Did the pain start suddenly or gradually?",
                "Does eating make the pain better or worse?",
                "Have you experienced vomiting?",
                "Have you noticed blood in stool or vomit?",
                "Do you have diarrhea or constipation?",
            ],

            "vomiting": [
                "How many times have you vomited today?",
                "Is there blood in the vomit?",
                "Can you keep fluids down?",
                "Do you have abdominal pain?",
            ],

            "diarrhea": [
                "How many loose stools have you had today?",
                "Have you noticed blood in the stool?",
                "Do you have fever?",
                "Are you able to stay hydrated?",
            ],
        }

        self.general_questions = [
            "When did your symptoms first begin?",
            "Have your symptoms become better, worse, or stayed the same?",
            "Have you experienced these symptoms before?",
            "Have you taken any medication for these symptoms?",
            "Do you have any chronic medical conditions?",
            "Are you currently taking any prescription medicines?",
            "Do you have any known allergies?",
        ]

    def generate(
        self,
        symptoms: list[str],
        patient_context=None,
        emergency=None,
        risk=None,
        rag_documents=None,
    ) -> FollowUpQuestions:

        logger.info("Generating follow-up questions")

        symptom_set = {
            symptom.lower().strip()
            for symptom in symptoms
            if symptom
        }

        priority_questions = []
        questions = []

        # -----------------------------------------
        # Symptom Questions
        # -----------------------------------------

        for symptom in sorted(symptom_set):

            questions.extend(
                self.question_bank.get(
                    symptom,
                    [],
                )
            )

        # -----------------------------------------
        # Emergency Questions
        # -----------------------------------------

        emergency_flag = False

        if isinstance(emergency, dict):
            emergency_flag = emergency.get(
                "is_emergency",
                False,
            )
        elif emergency is not None:
            emergency_flag = getattr(
                emergency,
                "is_emergency",
                False,
            )

        if emergency_flag:

            priority_questions.extend([
                "Are your symptoms getting worse right now?",
                "Can you safely reach the nearest emergency department?",
                "Is someone with you at the moment?",
            ])

        # -----------------------------------------
        # Risk Questions
        # -----------------------------------------

        risk_score = None

        if isinstance(risk, dict):
            risk_score = risk.get("risk_score")
        elif risk is not None:
            risk_score = getattr(
                risk,
                "risk_score",
                None,
            )

        if risk_score is not None and risk_score >= 70:

            priority_questions.extend([
                "Have you experienced similar symptoms previously?",
                "Have these symptoms rapidly worsened today?",
            ])

        # -----------------------------------------
        # Missing Context
        # -----------------------------------------

        if patient_context:

            if getattr(patient_context, "medical_history", None) == []:

                questions.append(
                    "Do you have any significant past medical history?"
                )

            if getattr(patient_context, "medications", None) == []:

                questions.append(
                    "Are you currently taking any medications?"
                )

            if getattr(patient_context, "allergies", None) == []:

                questions.append(
                    "Do you have any medication or food allergies?"
                )

        # -----------------------------------------
        # Evidence Questions
        # -----------------------------------------

        if rag_documents:

            questions.append(
                "Have these symptoms been evaluated by a healthcare professional before?"
            )

        # -----------------------------------------
        # General Questions
        # -----------------------------------------

        if symptom_set:

            questions.extend(
                self.general_questions
            )

        # -----------------------------------------
        # Remove Duplicates
        # -----------------------------------------

        final_questions = list(
            dict.fromkeys(
                priority_questions + questions
            )
        )

        logger.info(
            "Generated %d follow-up questions",
            len(final_questions),
        )

        return FollowUpQuestions(
            questions=final_questions
        )