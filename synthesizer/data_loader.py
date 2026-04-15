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

#Load all sentence templates from the templates directory
def load_templates() -> list[dict]:
    path = os.path.join(TEMPLATES_DIR, "sentences.json")
    with open(path, "r", encoding="utf-8") as f:
        templates = json.load(f)
    global _templates_cache
    _templates_cache = templates
    return templates

# Load PII values dict from pii.json file in the pii_values directory
def load_pii_values() -> dict[str, list[str]]:
    path = os.path.join(PII_VALUES_DIR, "pii.json")
    with open(path, "r", encoding="utf-8") as f:
        pii_values = json.load(f)
    return pii_values

# template selector in not random
_template_index = 0
_templates_cache: list[dict] | None = None

def select_template() -> dict:
    global _template_index, _templates_cache
    if _templates_cache is None:
        _templates_cache = load_templates()
    if not _templates_cache:
        raise ValueError("templates list is empty")
    template = _templates_cache[_template_index % len(_templates_cache)]
    _template_index += 1
    return template

#return template elements length
def get_template_count() -> int:
    global _templates_cache
    if _templates_cache is None:
        _templates_cache = load_templates()
    return len(_templates_cache)
