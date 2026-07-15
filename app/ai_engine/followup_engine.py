from app.ai_engine.schemas import FollowUpQuestions


class FollowUpEngine:
    """
    Production Follow-up Question Engine.

    Generates clinically relevant follow-up questions
    based on detected symptoms while avoiding duplicates.
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

    def generate(self, symptoms: list[str]) -> FollowUpQuestions:

        symptom_set = {
            symptom.lower().strip()
            for symptom in symptoms
        }

        questions = []

        # -----------------------------------------
        # Symptom-specific Questions
        # -----------------------------------------

        for symptom in sorted(symptom_set):

            questions.extend(
                self.question_bank.get(symptom, [])
            )

        # -----------------------------------------
        # Generic Clinical Questions
        # -----------------------------------------

        if symptom_set:

            questions.extend([
                "When did your symptoms first begin?",
                "Have your symptoms become better, worse, or stayed the same?",
                "Have you experienced these symptoms before?",
                "Have you taken any medication for these symptoms?",
            ])

        # -----------------------------------------
        # Remove Duplicates
        # -----------------------------------------

        unique_questions = list(
            dict.fromkeys(questions)
        )

        return FollowUpQuestions(
            questions=unique_questions
        )