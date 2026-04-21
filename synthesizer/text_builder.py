
import os
import json

def build_text_with_spans(template: str, assigned_values: list[dict]) -> dict:

    import re
    
    # Count occurrences of each entity type in template order
    entities_metadata = []
    
    # Group assigned values by type, maintaining order
    values_by_type = {}
    for item in assigned_values:
        for key, value in item.items():
            if key not in values_by_type:
                values_by_type[key] = []
            values_by_type[key].append(value)
    
    # Track usage index per type
    usage_index = {}
    
    # Find all placeholders in order of appearance
    placeholder_pattern = re.compile(r'\{(\w+)\}')
    
    # Build the final text by replacing placeholders one by one
    offset = 0  # Track character offset as we replace
    count=0

    for match in placeholder_pattern.finditer(template):
        entity_type = match.group(1)
        
        # Get the next value for this entity type
        if entity_type not in usage_index:
            usage_index[entity_type] = 0
        
        idx = usage_index[entity_type]
        if entity_type in values_by_type and idx < len(values_by_type[entity_type]):
            value = values_by_type[entity_type][idx]
        else:
            value = match.group(0)  # Keep original placeholder if no value
        
        usage_index[entity_type] += 1
        
        # Calculate position in the growing result string
        placeholder = match.group(0)  # e.g., {NAME}
        start_in_original = match.start()
        
        # Adjusted start considering previous replacements
        adjusted_start = start_in_original + offset
        adjusted_end = adjusted_start + len(value)
        
        entities_metadata.append({
            "Type": entity_type,
            "Value": value,
            "Span": [adjusted_start, adjusted_end],
            "Severity": round(get_severity(entity_type)*assigned_values[count].get("Expose", 0), 2), 
            "Expose": assigned_values[count].get("Expose", 0)
        })
        count+=1
        # Update offset: difference between replacement length and placeholder length
        offset += len(value) - len(placeholder)

    # Now build the actual replaced text
    usage_index_reset = {}
    def replace_match(m):
        etype = m.group(1)
        if etype not in usage_index_reset:
            usage_index_reset[etype] = 0
        idx = usage_index_reset[etype]
        usage_index_reset[etype] += 1
        if etype in values_by_type and idx < len(values_by_type[etype]):
            return values_by_type[etype][idx]
        return m.group(0)
    
    final_text = placeholder_pattern.sub(replace_match, template)
    
    return {
        "Text": final_text,
        "Entities": entities_metadata
    }


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