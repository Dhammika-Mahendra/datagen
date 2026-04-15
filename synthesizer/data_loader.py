"""
data_loader.py
--------------
Handles loading of sentence templates and PII value lists from local JSON files.
New entity types can be supported by adding a corresponding JSON file in pii_values/.
"""

import json
import os


# Paths to data directories (relative to project root)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "templates")
PII_VALUES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "pii_values")

# Maps entity type tokens (used in templates) to their value list filenames
ENTITY_FILE_MAP = {
    "NAME":     "names.json",
    "EMAIL":    "emails.json",
    "LOCATION": "locations.json",
}


def load_templates() -> list[dict]:
    """Load all sentence templates from the templates directory."""
    path = os.path.join(TEMPLATES_DIR, "sentences.json")
    with open(path, "r", encoding="utf-8") as f:
        templates = json.load(f)
    return templates


def load_pii_values() -> dict[str, list[str]]:
    """
    Load PII value lists for all registered entity types.
    Returns a dict: { "NAME": [...], "EMAIL": [...], ... }
    """
    pii_values = {}
    for entity_type, filename in ENTITY_FILE_MAP.items():
        path = os.path.join(PII_VALUES_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            pii_values[entity_type] = json.load(f)
    return pii_values
