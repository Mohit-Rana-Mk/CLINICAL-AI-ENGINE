from app.ai_engine.schemas import FollowUpQuestions


class FollowUpEngine:

    def generate(self, symptoms: list[str]) -> FollowUpQuestions:

        questions = []

        symptom_set = {s.lower() for s in symptoms}

        if "chest pain" in symptom_set:
            questions.extend([
                "On a scale of 1-10, how severe is the chest pain?",
                "Where exactly is the pain located?",
                "Does the pain spread to your left arm, jaw, neck, or back?",
                "Did the pain start suddenly or gradually?",
                "Are you sweating?",
                "Do you have breathing difficulty?"
            ])

        if "fever" in symptom_set:
            questions.extend([
                "What is your temperature?",
                "How many days have you had the fever?",
                "Have you taken any medicine?",
                "Do you have chills?"
            ])

        if "headache" in symptom_set:
            questions.extend([
                "How severe is the headache?",
                "Is it one-sided or all over your head?",
                "Do you have blurred vision?",
                "Do you have nausea or vomiting?"
            ])

        if "cough" in symptom_set:
            questions.extend([
                "Is the cough dry or productive?",
                "Are you coughing up blood?",
                "Do you have breathing difficulty?"
            ])

        return FollowUpQuestions(
            questions=list(dict.fromkeys(questions))
        )