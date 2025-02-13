"""
Hearthstone Strings file

File format: TSV. Lines starting with `#` are ignored.
Key is always `TAG`
"""
import csv
import json
import sys
import tempfile
from typing import Dict, Optional, Tuple

from hearthstone.xmlutils import download_to_tempfile_retry


StringsRow = Dict[str, str]
StringsDict = Dict[str, StringsRow]

_cache: Dict[Tuple[str, str], StringsDict] = {}


def load_json(fp) -> StringsDict:
	hsjson_strings = json.loads(fp.read())
	return {k: {"TEXT": v} for k, v in hsjson_strings.items()}


def load_txt(fp) -> StringsDict:
	fp = map(lambda x: x.replace("\0", ""), fp)
	reader = csv.DictReader(
		filter(lambda row: row.strip() and not row.startswith("#"), fp),
		delimiter="\t"
	)
	stripped_rows = [{k: v for k, v in row.items() if k and v} for row in reader]
	return {
		stripped_row.pop("TAG"): stripped_row for stripped_row in stripped_rows
		if stripped_row
	}


def _load_globalstrings_from_web(locale="enUS") -> Optional[StringsDict]:
	with tempfile.TemporaryFile() as fp:
		json_url = "https://api.hearthstonejson.com/v1/strings/%s/GLOBAL.json" % locale
		if download_to_tempfile_retry(json_url, fp):
			fp.flush()
			fp.seek(0)

			return load_json(fp)
		else:
			return None


def _load_globalstrings_from_library(locale="enUS") -> StringsDict:
	from hearthstone_data import get_strings_file

	path: str = get_strings_file(locale, filename="GLOBAL.txt")
	with open(path, "r", encoding="utf-8-sig") as f:
		return load_txt(f)


def load_globalstrings(locale="enUS") -> StringsDict:
	key = (locale, "GLOBAL.txt")
	if key not in _cache:
		sd = _load_globalstrings_from_web(locale=locale)

		if not sd:
			sd = _load_globalstrings_from_library(locale=locale)

		_cache[key] = sd

	return _cache[key]


if __name__ == "__main__":
	for path in sys.argv[1:]:
		with open(path, "r") as f:
			print(json.dumps(load_txt(f)))
