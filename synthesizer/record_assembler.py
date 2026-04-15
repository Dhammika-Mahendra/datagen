"""
record_assembler.py
-------------------
Orchestrates the synthesis of a single labelled training record by combining:
  1. entity_sampler  – picks PII values for a template's required entities
  2. text_builder    – fills the template and computes character spans

The output format matches the NER training schema:
{
  "text": "<rendered sentence>",
  "entities": [
    { "type": "<ENTITY_TYPE>", "value": "<pii value>", "span": [start, end] },
    ...
  ]
}
"""

from synthesizer.entity_sampler import sample_entities
from synthesizer.text_builder import build_text_with_spans


def assemble_record(template: dict, pii_values: dict[str, list[str]]) -> dict:
    """
    Build one labelled training record from a template definition.

    Args:
        template:   A single template dict loaded from sentences.json.
                    Expected keys: 'template' (str), 'entities' (list[str]).
        pii_values: Full dict of all available PII value lists.

    Returns:
        A dict with 'text' and 'entities' keys ready for JSON serialisation.
    """
    # Step 1: Sample one PII value per entity type the template requires
    entity_values = sample_entities(template["entities"], pii_values)

    # Step 2: Fill placeholders and get spans
    text, entity_spans = build_text_with_spans(template["template"], entity_values)

    return {
        "text": text,
        "entities": entity_spans
    }
