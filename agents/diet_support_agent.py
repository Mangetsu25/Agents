from typing import Dict


class DietSupportAgent:
    """Answers questions about a given diet plan."""

    def answer_question(self, question: str, plan: Dict) -> str:
        # Very naive logic. A real implementation would call a language model.
        question_lower = question.lower()
        if "breakfast" in question_lower:
            return f"Breakfast suggestion: {plan['diet'].get('breakfast')}"
        if "lunch" in question_lower:
            return f"Lunch suggestion: {plan['diet'].get('lunch')}"
        if "dinner" in question_lower:
            return f"Dinner suggestion: {plan['diet'].get('dinner')}"
        return "Please refer to your diet plan for details."


__all__ = ["DietSupportAgent"]
