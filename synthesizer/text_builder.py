"""
text_builder.py
---------------
Fills a sentence template with sampled PII values and calculates the
exact character span [start, end] of each inserted entity in the final text.

Span convention: start is inclusive, end is exclusive (Python slice style).
Example: text[start:end] == entity_value
"""
import json
import os

def build_text_with_spans(template: str, entity_values: dict[str, str]) -> tuple[str, list[dict]]:
    """
    Replace each {ENTITY_TYPE} placeholder in the template with its sampled value,
    then record the character span of every replaced entity.

    Args:
        template:      Raw template string, e.g. "Hi, I'm {NAME}. Email: {EMAIL}."
        entity_values: Mapping of entity type to its chosen value.

    Returns:
        A tuple of:
          - text (str): The fully rendered sentence.
          - spans (list[dict]): Each entry has keys 'type', 'value', 'span'.
    """
    text = template
    spans = []

    # Process placeholders in the order they appear left-to-right in the template.
    # We search for the next placeholder, replace it, and advance through the string.
    for entity_type, value in _ordered_placeholders(template, entity_values):
        placeholder = f"{{{entity_type}}}"

        # Find the placeholder in the *current* (partially filled) text
        start = text.find(placeholder)
        if start == -1:
            # Should not happen if template and entity_values are consistent
            continue

        # Replace only the first occurrence so repeated types don't collide
        text = text[:start] + value + text[start + len(placeholder):]

        end = start + len(value)
        spans.append({
            "type":  entity_type,
            "value": value,
            "span":  [start, end],
            "severity": get_severity(entity_type)  # Add severity to the span dict
        })

    return text, spans


def _ordered_placeholders(template: str, entity_values: dict[str, str]) -> list[tuple[str, str]]:
    """
    Return (entity_type, value) pairs sorted by the position of their placeholder
    in the template string, so replacements are applied left-to-right.
    """
    positions = []
    for entity_type in entity_values:
        placeholder = f"{{{entity_type}}}"
        idx = template.find(placeholder)
        if idx != -1:
            positions.append((idx, entity_type, entity_values[entity_type]))

    # Sort by position so we fill left-to-right
    positions.sort(key=lambda x: x[0])
    return [(entity_type, value) for _, entity_type, value in positions]

#severity.json file loading
def load_severity() -> dict[str, int]:
    path = os.path.join(os.path.dirname(__file__), "..", "data", "severity.json")
    with open(path, "r", encoding="utf-8") as f:
        severity = json.load(f)
    return severity

#get the severity value for each entity type frm severity.json file
def get_severity(entity_type: str) -> int:
    severity = load_severity()
    return severity.get(entity_type, 0)  # Default to 0 if not found