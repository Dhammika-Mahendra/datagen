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

import json
import math
import os

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
    # Step 1: Sample PII values per entity type the template requires
    entity_values = sample_entities(template["entities"], template["expose"], pii_values)

    # Step 2: Fill placeholders and get spans
    array = []
    for entity in entity_values:
      entity_spans = build_text_with_spans(template["template"], entity)
      array.append({"Text": entity_spans["Text"], "Entities": entity_spans["Entities"], "Risk" : calculate_total_severity(entity_spans["Entities"])})

    return array

#
# severity
#

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

#calculate total severity
def calculate_total_severity(entities: list[dict]) -> float:
  
  counts: dict[str, dict[str, int]] = {}
  for entity in entities:
    entity_type = entity.get("Type") or entity.get("Type")
    expose = entity.get("Expose") or entity.get("Expose")
    if entity_type is None or expose is None:
      continue

    if entity_type not in counts:
      counts[entity_type] = {}
    counts[entity_type][expose] = counts[entity_type].get(expose, 0) + 1
  
  alpha = 0.7
  total_severity = 1.0

  #print key valeu pairs in counts
  for entity_type, expose_counts in counts.items():
    entity_severity = 0.0 
    for entity, entity_count in expose_counts.items():
      entity_severity += float(entity) * entity_count
    weight = get_severity(entity_type)
    effective_weight = weight * (1 - math.exp(-alpha * entity_severity))
    total_severity *= (1 - effective_weight)
 
  total_severity = 1 - total_severity

  return round(total_severity, 2)