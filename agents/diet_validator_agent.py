from typing import Dict


class DietValidatorAgent:
    """Validates diet plans for basic nutritional completeness."""

    def validate_plan(self, plan: Dict) -> bool:
        diet = plan.get("diet", {})
        required_meals = {"breakfast", "lunch", "dinner"}
        return required_meals.issubset(diet.keys())


__all__ = ["DietValidatorAgent"]
