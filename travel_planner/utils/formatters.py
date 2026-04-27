"""
utils/formatters.py
───────────────────
Helper functions to clean and format LLM output before displaying it.
"""


def format_itinerary_for_display(raw_text: str) -> str:
    """
    Post-process the raw LLM output.
    Currently passes through as-is since Streamlit renders Markdown natively.
    Add transformations here if needed (e.g. inject HTML, strip unwanted chars).
    """
    if not raw_text:
        return "No itinerary was generated. Please try again."

    # Strip leading/trailing whitespace
    cleaned = raw_text.strip()

    return cleaned
