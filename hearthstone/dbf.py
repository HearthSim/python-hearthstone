import re
from collections import OrderedDict

from .enums import Locale
from .utils import ElementTree


class Dbf:
	@classmethod
	def load(cls, filename):
		ret = cls()
		with open(filename, "r") as f:
			ret.populate(f)
		return ret

	def __init__(self):
		self.name = None
		self.records = []
		self.columns = OrderedDict()
		self.source_fingerprint = None

	def __repr__(self):
		return "<%s: %s>" % (self.__class__.__name__, self.name)

	def _deserialize_record(self, element):
		ret = {}
		for field in element.findall("Field"):
			colname = field.attrib["column"]
			coltype = self.columns[colname]
			ret[colname] = self._deserialize_value(field, coltype)

		return ret

	def _deserialize_value(self, element, coltype):
		if element.text is None:
			return
		if coltype in ("Int", "Long", "ULong"):
			return int(element.text)
		elif coltype == "Float":
			return float(element.text)
		elif coltype == "Bool":
			return element.text == "True"
		elif coltype in ("String", "AssetPath"):
			return element.text
		elif coltype == "LocString":
			return {e.tag: e.text for e in element}
		raise NotImplementedError("Unknown DBF Data Type: %r" % (coltype))

	def populate(self, file):
		_xml = ElementTree.parse(file)
		self.name = _xml.getroot().attrib.get("name", "")
		for fingerprint in _xml.findall("SourceFingerprint"):
			self.source_fingerprint = fingerprint.text

		for column in _xml.findall("Column"):
			self.columns[column.attrib["name"]] = column.attrib["type"]

		self.records = [self._deserialize_record(e) for e in _xml.findall("Record")]

	def object_to_xml_column_name(self, name):
		if name.startswith("m_"):
			name = name[2:]
		name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
		return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).upper()

	def populate_from_unity_object(self, obj):
		d = obj.read()
		self.name = d["m_Name"]
		colnames = {}
		coltypes = {}

		# m_Records > Array > data
		record_tree = obj.type_tree.children[4].children[0].children[1]
		for field in record_tree.children:
			coltype = {
				"SInt64": "Long",
				"UInt64": "ULong",
				"int": "Int",
				"double": "Float",
				"float": "Float",
				"string": "String",
				"DbfLocValue": "LocString",
				"UInt8": "Bool"
			}[field.type]
			colname = field.name
			if colname.startswith("m_"):
				colname = colname[2:]
			colname = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", colname)
			colname = re.sub("([a-z0-9])([A-Z])", r"\1_\2", colname).upper()
			colnames[field.name] = colname
			coltypes[field.name] = coltype
			self.columns[colname] = coltype

		records = d["Records"]
		for record in records:
			r = {}
			for name, val in record.items():
				colname = colnames[name]
				coltype = coltypes[name]
				if coltype == "LocString":
					locStrings = zip(val["m_locales"], val["m_locValues"])
					r[colname] = dict((Locale(loc).name, s) for loc, s in locStrings)
				elif coltype == "Bool":
					r[colname] = val != 0
				else:
					r[colname] = val
			self.records.append(r)

	def _to_xml(self):
		root = ElementTree.Element("Dbf")

		if self.name is not None:
			root.attrib["name"] = self.name

		if self.source_fingerprint is not None:
			e = ElementTree.Element("SourceFingerprint")
			root.append(e)
			e.text = self.source_fingerprint

		for column, type in self.columns.items():
			e = ElementTree.Element("Column")
			root.append(e)
			e.attrib["name"] = column
			e.attrib["type"] = type

		for record in self.records:
			e = ElementTree.Element("Record")
			root.append(e)
			for column, type in self.columns.items():
				field = ElementTree.Element("Field")
				e.append(field)
				field.attrib["column"] = column
				value = record[column]
				if value is None:
					continue

				if type == "LocString":
					locales = sorted(value.keys())
					# Always have enUS as first item
					if "enUS" in locales:
						locales.insert(0, locales.pop(locales.index("enUS")))
					for locale in locales:
						eloc = ElementTree.Element(locale)
						field.append(eloc)
						eloc.text = value[locale]
				else:
					field.text = str(record[column])

		return root

	def to_xml(self, encoding="utf-8"):
		root = self._to_xml()
		return ElementTree.tostring(root, encoding=encoding)
