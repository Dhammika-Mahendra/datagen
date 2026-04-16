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
    array = []
    
    #tracking list to avoid repeating same value for same entity type in a single record
    tracked_list={}
    for entity_type in entity_types:
        tracked_list[entity_type] = []
        
    for _ in range(SAMPLING_COUNT):
        sampled = {}
        for entity_type in entity_types:
            available_values = [v for v in pii_values[entity_type] if v not in tracked_list[entity_type]]
            if not available_values:
                raise ValueError(f"No more unique {entity_type} values available.")
            sampled[entity_type] = random.choice(available_values)
            tracked_list[entity_type].append(sampled[entity_type])
        array.append(sampled)
    
    return array
 