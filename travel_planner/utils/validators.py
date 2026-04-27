"""
utils/validators.py
───────────────────
Validates user inputs before sending them to the LLM or external APIs.
Returns a list of error messages (empty list = all good).
"""


def validate_inputs(destination: str, num_days: int, travel_style: list) -> list[str]:
    """
    Validates the core user inputs.

    Returns:
        List of error message strings. Empty list means inputs are valid.
    """
    errors = []

    # Check destination
    if not destination or not destination.strip():
        errors.append("❌ Please enter a destination city.")
    elif len(destination.strip()) < 2:
        errors.append("❌ Destination name is too short.")
    elif len(destination.strip()) > 100:
        errors.append("❌ Destination name is too long. Please enter a city name.")
    elif any(char.isdigit() for char in destination):
        errors.append("❌ Destination should be a city name, not a number.")

    # Check days
    if not isinstance(num_days, int) or num_days < 1:
        errors.append("❌ Number of days must be at least 1.")
    elif num_days > 14:
        errors.append("❌ Maximum supported trip length is 14 days.")

    # Check travel style
    if not travel_style:
        errors.append("❌ Please select at least one travel style/interest.")

    return errors
