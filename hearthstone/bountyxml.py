import os
import pickle
import sqlite3
import tempfile
import uuid
from typing import Any, Callable, Dict, Iterator, Tuple

from sqlitedict import SqliteDict

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


def _bootstrap_from_web(parse: Callable[[Iterator[tuple[str, Any]]], None]):
	with tempfile.TemporaryFile(mode="rb+") as fp:
		if download_to_tempfile_retry(XML_URL, fp):
			fp.flush()
			fp.seek(0)

			parse(ElementTree.iterparse(fp, events=("start", "end",)))


def _bootstrap_from_library(parse: Callable[[Iterator[tuple[str, Any]]], None], path=None):
	from hearthstone_data import get_bountydefs_path

	if path is None:
		path = get_bountydefs_path()

	with open(path, "rb") as f:
		parse(ElementTree.iterparse(f, events=("start", "end",)))


def load(path=None, locale="enUS"):
	cache_key = (path, locale)
	if cache_key not in bounty_cache:
		card_count = 0
		filename = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
		conn = sqlite3.connect(filename)
		conn.execute(
			'CREATE TABLE IF NOT EXISTS "unnamed" (key INT PRIMARY KEY, value BLOB)'
		)

		def parse(context: Iterator[tuple[str, Any]]):
			nonlocal card_count
			nonlocal conn

			root = None
			for action, elem in context:
				if action == "start" and elem.tag == "BountyDefs":
					root = elem
					continue

				if action == "end" and elem.tag == "Bounty":
					bounty = BountyXML.from_xml(elem)
					bounty.locale = locale

					conn.execute(
						'REPLACE INTO "unnamed" (key, value) VALUES (?,?)',
						(
							bounty.id,
							sqlite3.Binary(
								pickle.dumps(bounty, protocol=pickle.HIGHEST_PROTOCOL)
							)
						)
					)

					card_count += 1

					elem.clear()  # type: ignore
					root.clear()  # type: ignore

		if path is None:
			# Check if the hearthstone_data package exists locally
			has_lib = True
			try:
				import hearthstone_data  # noqa: F401
			except ImportError:
				has_lib = False

			if not has_lib:
				_bootstrap_from_web(parse)

		if not card_count:
			_bootstrap_from_library(parse, path=path)

		conn.commit()
		conn.close()

		db = SqliteDict(filename)
		bounty_cache[cache_key] = (db, None)  # type: ignore

	return bounty_cache[cache_key]
