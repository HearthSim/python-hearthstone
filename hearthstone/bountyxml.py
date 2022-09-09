import tempfile
from typing import Any, Dict, Optional, Tuple

from .enums import Role
from .utils import ElementTree
from .xmlutils import download_to_tempfile_retry


class BountyXML:

	@classmethod
	def from_xml(cls, xml):
		self = cls(int(xml.attrib["ID"]))
		self.is_heroic = xml.attrib["is_heroic"].lower() == "true"
		self.level = int(xml.attrib["level"])

		boss = xml.find("Boss")
		self.boss_dbf_id = int(boss.attrib["CardID"])
		self.boss_role = Role(int(boss.attrib["role"]))

		boss_names = boss.find("Name")
		for loc_element in boss_names:
			self._localized_boss_names[loc_element.tag] = loc_element.text

		region = xml.find("Set")
		self.region_id = int(region.attrib["ID"])
		for loc_element in region:
			self._localized_region_names[loc_element.tag] = loc_element.text

		rewards = xml.findall("Reward")
		for reward in rewards:
			self.reward_mercenary_dbf_ids.add(int(reward.attrib["MercenaryID"]))

		return self

	def __init__(self, bounty_id, locale="enUS"):
		self.id = bounty_id
		self.boss_dbf_id = 0
		self.boss_role = Role.INVALID
		self.is_heroic = False
		self.level = 0
		self.region_id = 0
		self.reward_mercenary_dbf_ids = set()

		self.locale = locale

		self._localized_boss_names = {}
		self._localized_region_names = {}

	@property
	def boss_name(self):
		return self._localized_boss_names.get(self.locale, "")

	@property
	def region_name(self):
		return self._localized_region_names.get(self.locale, "")


bounty_cache: Dict[Tuple[str, str], Tuple[Dict[int, BountyXML], Any]] = {}


XML_URL = "https://api.hearthstonejson.com/v1/latest/BountyDefs.xml"


def _bootstrap_from_web() -> Optional[ElementTree.ElementTree]:
	with tempfile.TemporaryFile(mode="rb+") as fp:
		if download_to_tempfile_retry(XML_URL, fp):
			fp.flush()
			fp.seek(0)

			return ElementTree.parse(fp)
		else:
			return None


def _bootstrap_from_library(path=None) -> ElementTree.ElementTree:
	from hearthstone_data import get_bountydefs_path

	if path is None:
		path = get_bountydefs_path()

	with open(path, "rb") as f:
		return ElementTree.parse(f)


def load(path=None, locale="enUS"):
	cache_key = (path, locale)
	if cache_key not in bounty_cache:
		xml = None
		if path is None:
			xml = _bootstrap_from_web()

		if not xml:
			xml = _bootstrap_from_library(path=path)

		db = {}

		for bountydata in xml.findall("Bounty"):
			bounty = BountyXML.from_xml(bountydata)
			bounty.locale = locale
			db[bounty.id] = bounty

		bounty_cache[cache_key] = (db, xml)

	return bounty_cache[cache_key]
