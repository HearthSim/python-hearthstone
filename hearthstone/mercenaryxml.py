from typing import Any, Dict, Tuple

from hearthstone.enums import Rarity

from .utils import ElementTree


class MercenaryXML:

	@classmethod
	def from_xml(cls, xml):
		self = cls(int(xml.attrib["ID"]))
		self.collectible = xml.attrib["collectible"].lower() == "true"
		self.crafting_cost = int(xml.attrib["crafting_cost"])
		self.name = xml.attrib["name"]
		self.rarity = Rarity(int(xml.attrib["rarity"]))

		short_name_elt = xml.find("ShortName")
		if short_name_elt:
			short_name_dict = {}
			for loc_element in short_name_elt:
				short_name_dict[loc_element.tag] = loc_element.text

			self.short_names = short_name_dict

		skins = xml.find("Skins")
		for skin_elt in skins:
			skin_dbf_id = int(skin_elt.attrib["CardID"])
			self.skin_dbf_ids.append(skin_dbf_id)
			if "default" in skin_elt.attrib and skin_elt.attrib["default"].lower() == "true":
				self.default_skin_dbf_id = skin_dbf_id

		specializations = xml.find("Specializations")
		for specialization_elt in specializations:
			ability_list = []
			abilities_elt = specialization_elt.find("Abilities")
			for ability_elt in abilities_elt:
				name_elt = ability_elt.find("Name")
				ability_name_dict = {}
				for loc_element in name_elt:
					ability_name_dict[loc_element.tag] = loc_element.text

				tiers_elt = ability_elt.find("Tiers")
				tier_list = []
				for tier_elt in tiers_elt:
					tier_list.append({
						"crafting_cost": int(tier_elt.attrib["crafting_cost"]),
						"dbf_id": int(tier_elt.attrib["CardID"]),
						"tier": int(tier_elt.attrib["tier"])
					})

				ability_list.append({
					"id": int(ability_elt.attrib["ID"]),
					"name": ability_name_dict,
					"tiers": tier_list
				})

			specialization_name_dict = {}
			specialization_names = specialization_elt.find("Name")
			for loc_element in specialization_names:
				specialization_name_dict[loc_element.tag] = loc_element.text

			self.specializations.append({
				"id": int(specialization_elt.attrib["ID"]),
				"name": specialization_name_dict,
				"abilities": ability_list
			})

		equipments = xml.find("Equipments")
		for equipment_elt in equipments:
			tiers_elt = equipment_elt.find("Tiers")
			tier_list = []
			for tier_elt in tiers_elt:
				tier_list.append({
					"crafting_cost": int(tier_elt.attrib["crafting_cost"]),
					"dbf_id": int(tier_elt.attrib["CardID"]),
					"tier": int(tier_elt.attrib["tier"])
				})

			self.equipment.append({
				"id": int(equipment_elt.attrib["ID"]),
				"tiers": tier_list,
			})

		return self

	def __init__(self, mercenary_id, locale="enUS"):
		self.id = mercenary_id
		self.collectible = False
		self.crafting_cost = 0
		self.name = ""
		self.rarity = Rarity.INVALID

		self.default_skin_dbf_id = 0
		self.skin_dbf_ids = []

		self.equipment = []
		self.specializations = []

		self.short_names = {}

		self.locale = locale

	def to_xml(self):
		ret = ElementTree.Element(
			"Mercenary",
			ID=str(self.id),
			collectible=str(self.collectible),
			crafting_cost=str(self.crafting_cost),
			name=self.name,
			rarity=str(int(self.rarity))
		)

		skins_elt = ElementTree.SubElement(ret, "Skins")
		for skin_dbf_id in self.skin_dbf_ids:
			skin_elt = ElementTree.SubElement(skins_elt, "Skin", CardID=str(skin_dbf_id))
			if skin_dbf_id == self.default_skin_dbf_id:
				skin_elt.attrib["default"] = str(True)

		if len(self.short_names):
			short_names_elt = ElementTree.SubElement(ret, "ShortName")
			for locale, localized_value in sorted(self.short_names.items()):
					if localized_value:
						loc_element = ElementTree.SubElement(short_names_elt, locale)
						loc_element.text = str(localized_value)

		specializations_elt = ElementTree.SubElement(ret, "Specializations")
		for specialization in self.specializations:
			spec_elt = ElementTree.SubElement(
				specializations_elt,
				"Specialization",
				ID=str(specialization["id"])
			)
			spec_name = ElementTree.SubElement(spec_elt, "Name")

			for locale, localized_value in sorted(specialization["name"].items()):
				if localized_value:
					loc_element = ElementTree.SubElement(spec_name, locale)
					loc_element.text = str(localized_value)

			abilities_elt = ElementTree.SubElement(spec_elt, "Abilities")
			for ability in specialization["abilities"]:
				ability_elt = ElementTree.SubElement(
					abilities_elt,
					"Ability",
					ID=str(ability["id"]),
				)

				name_elt = ElementTree.SubElement(ability_elt, "Name")
				for locale, localized_value in sorted(ability["name"].items()):
					if localized_value:
						loc_element = ElementTree.SubElement(name_elt, locale)
						loc_element.text = str(localized_value)

				tiers_elt = ElementTree.SubElement(ability_elt, "Tiers")
				for tier_dict in sorted(ability["tiers"], key=lambda t: t["tier"]):
					ElementTree.SubElement(
						tiers_elt,
						"Tier",
						CardID=str(tier_dict["dbf_id"]),
						crafting_cost=str(tier_dict["crafting_cost"]),
						tier=str(tier_dict["tier"])
					)

		equipments_elt = ElementTree.SubElement(ret, "Equipments")
		for equipment in self.equipment:
			equipment_elt = ElementTree.SubElement(
				equipments_elt,
				"Equipment",
				ID=str(equipment["id"]),
			)

			tiers_elt = ElementTree.SubElement(equipment_elt, "Tiers")
			for tier_dict in sorted(equipment["tiers"], key=lambda t: t["tier"]):
				ElementTree.SubElement(
					tiers_elt,
					"Tier",
					CardID=str(tier_dict["dbf_id"]),
					crafting_cost=str(tier_dict["crafting_cost"]),
					tier=str(tier_dict["tier"])
				)

		return ret


mercenary_cache: Dict[Tuple[str, str], Tuple[Dict[int, MercenaryXML], Any]] = {}


def load(path=None, locale="enUS"):
	cache_key = (path, locale)
	if cache_key not in mercenary_cache:
		from hearthstone_data import get_mercenarydefs_path

		if path is None:
			path = get_mercenarydefs_path()

		db = {}

		with open(path, "rb") as f:
			xml = ElementTree.parse(f)
			for mercenarydata in xml.findall("Mercenary"):
				bounty = MercenaryXML.from_xml(mercenarydata)
				bounty.locale = locale
				db[bounty.id] = bounty

		mercenary_cache[cache_key] = (db, xml)

	return mercenary_cache[cache_key]
