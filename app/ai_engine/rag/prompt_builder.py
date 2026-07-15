from typing import List

from app.ai_engine.rag.schemas import SearchResult


class PromptBuilder:
    """
    Production Clinical Prompt Builder.

    Builds a structured prompt using:

    - Patient Context
    - Emergency Assessment
    - Risk Assessment
    - Retrieved Clinical Evidence

    Compatible with:
    - GPT-5
    - Azure OpenAI
    - Llama
    - LangGraph
    """

    @staticmethod
    def _bullet(items) -> str:

        if not items:
            return "None"

        return "\n".join(
            f"- {item}"
            for item in items
        )

    @staticmethod
    def _dict_block(data: dict) -> str:

        if not data:
            return "Unknown"

        lines = []

        for key, value in data.items():

            lines.append(
                f"{key.replace('_', ' ').title()}: {value}"
            )

        return "\n".join(lines)

    def build(
        self,
        query: str,
        documents: List[SearchResult],
        patient_context: dict | None = None,
        emergency_status: dict | None = None,
        risk_assessment: dict | None = None,
    ) -> str:

        # ==========================================================
        # Clinical Evidence
        # ==========================================================

        if documents:

            evidence = []

            for index, result in enumerate(documents, start=1):

                evidence.append(
                    f"""
Document {index}

Title:
{result.document.title}

Category:
{result.document.category}

Source:
{result.document.source}

Similarity:
{result.similarity_score:.3f}

Evidence:
{result.document.content}
"""
                )

            medical_evidence = "\n".join(evidence)

        else:

            medical_evidence = (
                "No relevant medical evidence retrieved."
            )

        # ==========================================================
        # Patient
        # ==========================================================

        if patient_context:

            patient_information = f"""
Patient ID:
{patient_context.get("patient_id")}

Age:
{patient_context.get("age")}

Gender:
{patient_context.get("gender")}

Medical History:
{self._bullet(patient_context.get("medical_history", []))}

Current Medications:
{self._bullet(patient_context.get("medications", []))}

Known Allergies:
{self._bullet(patient_context.get("allergies", []))}

Vitals:
{self._dict_block(patient_context.get("vitals", {}))}

Laboratory Reports:
{self._dict_block(patient_context.get("lab_reports", {}))}
"""

        else:

            patient_information = (
                "No patient context available."
            )

        # ==========================================================
        # Emergency
        # ==========================================================

        if emergency_status:

            emergency_information = f"""
Emergency:
{emergency_status.get("is_emergency")}

Severity:
{emergency_status.get("level")}

Detected Patterns:
{self._bullet(emergency_status.get("detected_patterns", []))}

Reason:
{emergency_status.get("reason")}

Recommendation:
{emergency_status.get("recommendation")}
"""

        else:

            emergency_information = (
                "Emergency assessment unavailable."
            )

        # ==========================================================
        # Risk
        # ==========================================================

        if risk_assessment:

            risk_lines = []

            for factor in risk_assessment.get(
                "risk_factors",
                [],
            ):

                risk_lines.append(
                    f"- {factor.get('factor')} "
                    f"({factor.get('impact')}, "
                    f"Weight {factor.get('weight')})"
                )

            risk_information = f"""
Overall Risk:
{risk_assessment.get("overall_risk")}

Risk Score:
{risk_assessment.get("risk_score")}

Heart Risk:
{risk_assessment.get("heart_risk")}

Respiratory Risk:
{risk_assessment.get("respiratory_risk")}

Infection Risk:
{risk_assessment.get("infection_risk")}

Neurological Risk:
{risk_assessment.get("neurological_risk")}

Risk Factors:
{chr(10).join(risk_lines) if risk_lines else "None"}
"""

        else:

            risk_information = (
                "Risk assessment unavailable."
            )

        # ==========================================================
        # Final Prompt
        # ==========================================================

        return f"""
You are an advanced Clinical Decision Support AI assisting licensed healthcare professionals.

Use ONLY the supplied patient context and retrieved clinical evidence.

Never fabricate:
- diagnoses
- medications
- laboratory values
- medical history

Clearly distinguish:
- observed evidence
- clinical reasoning
- uncertainty
- recommendations

==================================================
PATIENT INFORMATION
==================================================

{patient_information}

==================================================
PATIENT QUERY
==================================================

{query}

==================================================
EMERGENCY STATUS
==================================================

{emergency_information}

==================================================
RISK ASSESSMENT
==================================================

{risk_information}

==================================================
RETRIEVED CLINICAL EVIDENCE
==================================================

{medical_evidence}

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

{{
  "clinical_summary": "",
  "key_findings": [],
  "risk_level": "",
  "emergency_status": "",
  "possible_conditions": [],
  "recommended_actions": [],
  "medication_considerations": [],
  "recommended_tests": [],
  "patient_education": [],
  "follow_up": [],
  "explanation": ""
}}
""".strip()