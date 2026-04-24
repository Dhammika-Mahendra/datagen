import argparse
import json
import re
from pathlib import Path


ENTITY_PATTERN = re.compile(r"\{([A-Z0-9_]+)\}")
EXPOSE_PATTERN = re.compile(r"\[(.*?)\]")


def parse_expose(line: str) -> list[int]:
	match = EXPOSE_PATTERN.search(line)
	if not match:
		raise ValueError(f"Expose line missing brackets: {line!r}")
	raw_items = [item.strip() for item in match.group(1).split(",") if item.strip()]
	return [int(item) for item in raw_items]


def extract_entities(sentence: str) -> list[str]:
	# Keep entities in first-seen order, unique only once.
	seen: set[str] = set()
	entities: list[str] = []
	for label in ENTITY_PATTERN.findall(sentence):
		if label not in seen:
			seen.add(label)
			entities.append(label)
	return entities


def convert_lines(lines: list[str]) -> list[dict]:
	stripped = [line.strip() for line in lines if line.strip()]
	if len(stripped) % 2 != 0:
		raise ValueError("Input must contain pairs of lines: sentence + expose.")

	records: list[dict] = []
	for index in range(0, len(stripped), 2):
		sentence = stripped[index]
		expose_line = stripped[index + 1]
		record = {
			"template": sentence,
			"entities": extract_entities(sentence),
			"expose": parse_expose(expose_line)
		}
		records.append(record)
	return records


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Convert paired sentence/expose TXT into JSON array."
	)
	parser.add_argument(
		"--input",
		default="list.txt",
		help="Path to input TXT file (default: list.txt)",
	)
	parser.add_argument(
		"--output",
		default="output.json",
		help="Path to output JSON file (default: output.json)",
	)
	args = parser.parse_args()

	base_dir = Path(__file__).resolve().parent
	input_path = (base_dir / args.input).resolve()
	output_path = (base_dir / args.output).resolve()

	lines = input_path.read_text(encoding="utf-8").splitlines()
	records = convert_lines(lines)
	for record in records:
		record["group"] = [1] * len(record.get("expose", []))
	output_path.write_text(
		json.dumps(records, indent=2, ensure_ascii=False),
		encoding="utf-8",
	)


if __name__ == "__main__":
	main()
