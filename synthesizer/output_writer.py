"""
output_writer.py
----------------
Handles writing the final synthesized dataset to disk as a JSON file.
"""

import json
import os


def write_dataset(records: list[dict], output_path: str) -> None:
    """
    Serialise the list of training records to a JSON file.

    Args:
        records:     List of assembled record dicts.
        output_path: Full path (including filename) for the output JSON file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"[✓] Wrote {len(records)} records → {output_path}")
