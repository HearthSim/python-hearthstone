## hearthstone.hslog

hslog is a powerful Hearthstone Power.log deserializer.

### Concepts

The data read from Power.log is deserialized into packets.
The log is read line by line using a regex-based approach, with packets
accumulating data when they span over multiple lines.
The `BLOCK_START` and `BLOCK_END` packets are serialized into a Block packet,
which is nestable.
We call the totality of the packets for a game the "Packet Tree".


### Exporting a PacketTree

The `PacketTree` object makes it easy to recursively iterate over, which in
turn makes it very easy to export into various other formats. The `.export()`
method on `PacketTree` will natively export the entire tree to a `Game` entity,
using the `hearthstone.entities` module by default.

This is achieved through a very flexible class-based Exporter system, which can
be found in `hslog.export`.
The syntax to call an exporter directly is: `MyExporter(packet_tree).export()`.

The base logic for the Exporter is in the `BaseExporter` class.
Calling `export()` will iterate over each packet and call `export_packet(packet)`
on them. That method will look at the packet's type, get the matching method in
the `self.dispatch` dict (populated by `get_dispatch_dict()`) and call it on it.

This is the default dispatch lookup:

* `CreateGame` -> `handle_create_game()`
* `CreateGame.Player`: `handle_player()`
* `Block`: `handle_block`
* `FullEntity`: `handle_full_entity`
* `HideEntity`: `handle_hide_entity`
* `ShowEntity`: `handle_show_entity`
* `ChangeEntity`: `handle_change_entity`
* `TagChange`: `handle_tag_change`
* `MetaData`: `handle_metadata`
* `Choices`: `handle_choices`
* `SendChoices`: `handle_send_choices`
* `ChosenEntities`: `handle_chosen_entities`
* `Options`: `handle_options`
* `Option`: `handle_option`
* `SendOption`: `handle_send_option`

All of the methods in the dispatch dict should be implemented.

The default exporter used by `PacketTree` is the `EntityTreeExporter`. It
creates an "Entity Tree" by simulating each packet in its handler. Choices,
Options and MetaData packets are ignored.
