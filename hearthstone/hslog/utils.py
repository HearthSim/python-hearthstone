from hearthstone.enums import TAG_TYPES, GameTag


def parse_enum(enum, value):
	if value.isdigit():
		value = int(value)
	elif hasattr(enum, value):
		value = getattr(enum, value)
	else:
		raise Exception("Unhandled %s: %r" % (enum, value))
	return value


def parse_tag(tag, value):
	tag = parse_enum(GameTag, tag)
	if tag in TAG_TYPES:
		value = parse_enum(TAG_TYPES[tag], value)
	elif value.isdigit():
		value = int(value)
	else:
		raise NotImplementedError("Invalid string value %r = %r" % (tag, value))
	return tag, value
