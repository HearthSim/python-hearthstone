try:
	from importlib.metadata import version

	__version__ = version("hearthstone")
except ImportError:
	import pkg_resources

	__version__ = pkg_resources.require("hearthstone")[0].version
