"""
entity_sampler.py
-----------------
Randomly samples PII values for each entity type required by a template.
Sampling is done without replacement within a single record to avoid
repeating the same value for the same entity type (e.g., two identical names).
"""

import random

SAMPLING_COUNT = 3  # Number of values to sample per entity type (can be >1 for multi-entity templates)

def sample_entities(entity_types: list[str], pii_values: dict[str, list[str]]) -> list[dict]:
    """
    For each entity type in the list, randomly pick a value from pii_values.

    Args:
        entity_types: List of entity type tokens required (e.g., ["NAME", "EMAIL"]).
        pii_values:   Dict mapping entity types to their available value lists.

    Returns:
        List of dicts, each containing an entity type and its sampled value, e.g.:
        [{"type": "NAME", "value": "John Perera"}, {"type": "EMAIL", "value": "john@gmail.com"}]

    Raises:
        KeyError: If an entity type has no registered value list.
    """
    array = []
    pools: dict[str, list[str]] = {}
    for entity_type in entity_types:
        values = pii_values[entity_type]
        if len(values) < SAMPLING_COUNT:
            raise ValueError(
                f"Not enough unique values for {entity_type}: "
                f"need {SAMPLING_COUNT}, have {len(values)}"
            )
        shuffled = values[:]
        random.shuffle(shuffled)
        pools[entity_type] = shuffled
    for _ in range(SAMPLING_COUNT):
        sampled = {}
        for entity_type in entity_types:
            sampled[entity_type] = pools[entity_type].pop()
        array.append(sampled)
    
    return array
 