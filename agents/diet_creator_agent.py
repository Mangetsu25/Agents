from typing import Dict


class DietCreatorAgent:
    """Generates diet plans based on user profile."""

    def create_diet(self, profile: Dict) -> Dict:
        # Placeholder implementation. In a real scenario, this would query an LLM
        # or external service to build a personalized diet plan.
        age = profile.get("age")
        goal = profile.get("goal", "maintenance")
        plan = {
            "profile": profile,
            "diet": {
                "breakfast": "Oatmeal with fruit",
                "lunch": "Grilled chicken salad",
                "dinner": "Baked salmon with vegetables",
            },
            "goal": goal,
        }
        if age and age < 12:
            plan["diet"]["snack"] = "Fruit yogurt"
        return plan


__all__ = ["DietCreatorAgent"]
