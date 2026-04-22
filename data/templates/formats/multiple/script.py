import argparse
import json
import re
from pathlib import Path


LABEL_PATTERN = re.compile(r"\{([A-Z][A-Z0-9_]*)\}")
EXPOSE_PATTERN = re.compile(r"^\[\s*([0-9]+(?:\.[0-9]+)?)\s*\]$")


def parse_sentences(text: str) -> list[dict]:
	records: list[dict] = []
	current_expose = 1.0
	for line in text.splitlines():
		sentence = line.strip()
		if not sentence:
			continue
		expose_match = EXPOSE_PATTERN.match(sentence)
		if expose_match:
			current_expose = float(expose_match.group(1))
			continue
		entities = LABEL_PATTERN.findall(sentence)
		expose = [current_expose] * len(entities)
		records.append({
			"template": sentence,
			"entities": entities,
			"expose": expose,
		})
	return records


def main() -> int:
	parser = argparse.ArgumentParser(
		description="Convert a sentence list TXT file to JSON templates."
	)
	script_dir = Path(__file__).resolve().parent
	parser.add_argument(
		"--input",
		type=Path,
		default=script_dir / "list.txt",
		help="Path to the input .txt file (default: list.txt)",
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=script_dir / "output.json",
		help="Path to the output .json file (default: output.json)",
	)
	args = parser.parse_args()

	text = args.input.read_text(encoding="utf-8")
	records = parse_sentences(text)

	args.output.parent.mkdir(parents=True, exist_ok=True)
	args.output.write_text(
		json.dumps(records, indent=2, ensure_ascii=False),
		encoding="utf-8",
	)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

