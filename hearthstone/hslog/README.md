## hearthstone.hslog

hslog is a library for parsing and streaming Hearthstone logs.


### Usage

```python
from hearthstone.hslog import LogWatcher
watcher = LogWatcher()

with open("Power.log", "r") as f:
	watcher.read(f)

for packet_tree in watcher.games:
	print(packet_tree.game, packet_tree.game.players)

	for packet in packet_tree.packets:
		print(packet)
```

You can subclass the `LogWatcher` class to register callbacks.

The following methods are available:

* `on_entity_update(entity)`: An entity has been updated.
* `on_block(action)`: An action has completed (`ACTION_END`)
* `on_metadata(metadata)`: Action metadata is ready.
* `on_tag_change(entity, tag, value)`: A tag's value has changed on an entity.
* `on_zone_change(entity, old, new)`: An entity moved between two zones.
