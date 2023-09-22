from collections import OrderedDict, defaultdict

from hearthstone.cardxml import load
from hearthstone.enums import CardSet, GameTag


def dump_reprints():
	db, _ = load()
	dbf_db = {v.dbf_id: v for k, v in db.items()}
	pointers = {}  # dbfId -> dict

	# First, assemble a list of mappings from card -> copies
	for card in db.values():
		copy_of_dbf_id = card.tags.get(GameTag.DECK_RULE_COUNT_AS_COPY_OF_CARD_ID)

		if not copy_of_dbf_id:
			continue

		if copy_of_dbf_id not in dbf_db:
			continue

		copy_card = dbf_db[copy_of_dbf_id]
		if not card.is_functional_duplicate_of(copy_card):
			continue

		pointers[card.dbf_id] = copy_of_dbf_id

	# At this point we have a mapping of dbfId -> dbfId
	# Now, try to merge these into sets

	chains = defaultdict(set)
	for k, v in pointers.items():
		chains[k].add(k)
		chains[k].add(v)

	# Now, keep merging
	while True:
		# Start over

		modified = False
		for parent, targets in chains.items():
			new_targets = set(targets)

			# check if any children own lists
			for child in targets:
				if child == parent:
					continue
				if child in chains:
					new_targets.update(chains[child])
					del chains[child]
					modified = True
				for k, chain in list(chains.items()):
					if child in chain and k != parent:
						new_targets.update(chain)
						del chains[k]
						modified = True

			# Find the smallest
			smallest = min(targets)

			# If the parent is the smallest, nothing to do - children will turn up
			if smallest == parent:
				targets.update(new_targets)
				if modified:
					break
				else:
					continue

			chains[smallest] = new_targets
			del chains[parent]

			modified = True
			break

		if not modified:
			break

	the_map = {}

	for chain in chains.values():
		# Map to cards
		the_chain = [dbf_db[c] for c in chain]
		the_chain = [c for c in the_chain if c.collectible]
		if len(the_chain) < 2:
			continue

		# Get rid of chains without WONDERS cards
		if not any([c for c in the_chain if c.card_set == CardSet.WONDERS]):
			continue

		# Find the best owner
		bad_sets = [
			CardSet.CORE,
			CardSet.PLACEHOLDER_202204,
			CardSet.EXPERT1,
			CardSet.BASIC,
			CardSet.LEGACY,
			CardSet.VANILLA
		]
		owners_from_good_sets = [c for c in the_chain if c.card_set not in bad_sets]

		winner = None

		assert len(owners_from_good_sets) in (1, 2)

		if len(owners_from_good_sets) == 1:
			# WONDERS is the only good set, map all others to it
			assert owners_from_good_sets[0].card_set == CardSet.WONDERS
			winner = owners_from_good_sets[0]
		elif len(owners_from_good_sets) == 2:
			# Probably one is from WON
			old_cards = [c for c in owners_from_good_sets if c.card_set != CardSet.WONDERS]
			assert len(old_cards) == 1
			winner = old_cards[0]

		for c in the_chain:
			if c.id == winner.id:
				continue
			the_map[c.id] = winner.id

	print(dict(OrderedDict(sorted(the_map.items()))))


if __name__ == "__main__":
	dump_reprints()
