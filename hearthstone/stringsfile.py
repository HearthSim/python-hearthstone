"""
Hearthstone Strings file

File format: TSV. Lines starting with `#` are ignored.
Key is always `TAG`
"""
import csv


def load(fp):
	reader = csv.DictReader(filter(lambda row: not row.startswith("#"), fp), delimiter="\t")
	stripped_rows = [{k: v for k, v in row.items() if v} for row in reader]
	return {stripped_row.pop("TAG"): stripped_row for stripped_row in stripped_rows}


if __name__ == "__main__":
	import json
	import sys

	for path in sys.argv[1:]:
		with open(path, "r") as f:
			print(json.dumps(load(f)))
