import json
import pathlib


SENTENCES_PATH = pathlib.Path(__file__).with_name("sentences.json")

# TODO: Add your JSON file paths here (relative to this script).
SOURCE_JSONS = [
	"formats/single/output.json",
	"formats/multiple/output.json",
	"formats/multi group/output.json",
	"formats/mix/output.json",
]


def load_json_from_source(source: str):
	path = (pathlib.Path(__file__).parent / source).resolve()
	with open(path, "r", encoding="utf-8") as handle:
		return json.load(handle)


def main() -> None:
	combined = []

	for source in SOURCE_JSONS:
		data = load_json_from_source(source)
		if isinstance(data, list):
			combined.extend(data)
		else:
			raise ValueError(f"Expected a JSON array in {source}")

	with open(SENTENCES_PATH, "w", encoding="utf-8") as handle:
		json.dump(combined, handle, ensure_ascii=False, indent=2)


if __name__ == "__main__":
	main()
