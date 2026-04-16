"""
main.py
-------
Entry point for the PII data synthesizer.

Usage:
    python main.py                    # generate default 100 records
    python main.py --count 500        # generate 500 records
    python main.py --count 200 --output output/my_dataset.json
    python main.py --seed 42          # reproducible run
"""

import argparse
import random
import os

from synthesizer.data_loader import load_templates, load_pii_values, select_template, get_template_count
from synthesizer.record_assembler import assemble_record
from synthesizer.output_writer import write_dataset


DEFAULT_COUNT = 100
DEFAULT_OUTPUT = os.path.join("output", "data.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synthesize labelled PII training data from local templates."
    )
    parser.add_argument(
        "--count", type=int, default=DEFAULT_COUNT,
        help=f"Number of records to generate (default: {DEFAULT_COUNT})"
    )
    parser.add_argument(
        "--output", type=str, default=DEFAULT_OUTPUT,
        help=f"Output JSON file path (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility (default: no fixed seed)"
    )
    return parser.parse_args()


def generate_dataset(seed: int | None = None) -> list[dict]:

    if seed is not None:
        random.seed(seed)
        print(f"[i] Random seed set to {seed}")

    # Load data assets from local files
    templates = load_templates()
    pii_values = load_pii_values()

    print(f"[i] Loaded {len(templates)} templates and {sum(len(v) for v in pii_values.values())} PII values")
    print(f"[i] Generating {get_template_count()} records...")

    records = []
    for _ in range(get_template_count()):
        # Pick a random template for each record
        template = select_template()
        record = assemble_record(template, pii_values)
        #record may be single or multiple elements array, break it and append to records
        if isinstance(record, list):
            records.extend(record)
        else:           
            records.append(record)

    return records


def main():
    args = parse_args()
    records = generate_dataset(seed=args.seed)
    write_dataset(records, args.output)


if __name__ == "__main__":
    main()
