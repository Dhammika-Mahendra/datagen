
import random

SAMPLING_COUNT = 2  # Number of values to sample per entity type (can be >1 for multi-entity templates)

def sample_entities(entity_types: list[str], expose: list[str], pii_values: dict[str, list[str]]) -> list[dict]:
    array = []
    
    #tracking list to avoid repeating same value for same entity type in a single record
    tracked_list={}
    for entity_type in entity_types:
        tracked_list[entity_type] = []
        
    for _ in range(SAMPLING_COUNT):
        sample_obj=[]
        for entity_type in entity_types:
            sampled = {}
            available_values = [v for v in pii_values[entity_type] if v not in tracked_list[entity_type]]
            if not available_values:
                raise ValueError(f"No more unique {entity_type} values available.")
            sampled[entity_type] = random.choice(available_values)
            tracked_list[entity_type].append(sampled[entity_type])
            sample_obj.append(sampled)
        array.append(sample_obj)

        for t in sample_obj:
            t["Expose"] = expose[sample_obj.index(t)]


    return array
 