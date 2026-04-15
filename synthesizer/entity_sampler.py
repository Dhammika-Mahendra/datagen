"""
entity_sampler.py
-----------------
Randomly samples PII values for each entity type required by a template.
Sampling is done without replacement within a single record to avoid
repeating the same value for the same entity type (e.g., two identical names).
"""

import random


def sample_entities(entity_types: list[str], pii_values: dict[str, list[str]]) -> dict[str, str]:
    """
    For each entity type in the list, randomly pick a value from pii_values.

    Args:
        entity_types: List of entity type tokens required (e.g., ["NAME", "EMAIL"]).
        pii_values:   Dict mapping entity types to their available value lists.

    Returns:
        Dict mapping each entity type to one sampled value, e.g.:
        { "NAME": "John Perera", "EMAIL": "john@gmail.com" }

    Raises:
        KeyError: If an entity type has no registered value list.
    """
    sampled = {}
    for entity_type in entity_types:
        if entity_type not in pii_values:
            raise KeyError(f"No PII value list found for entity type: '{entity_type}'")
        sampled[entity_type] = random.choice(pii_values[entity_type])
    return sampled
