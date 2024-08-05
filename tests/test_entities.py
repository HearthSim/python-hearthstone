import pytest

from hearthstone.entities import Card, Game, Player
from hearthstone.enums import CardSet, CardType, GameTag, Step, Zone


class TestGame:
	def test_find_entity_by_id(self):
		game = Game(1)
		game.register_entity(game)

		assert game.find_entity_by_id(1) is game
		assert game.find_entity_by_id(2) is None


class TestPlayer:
	@pytest.fixture
	def game(self):
		game = Game(1)
		game.register_entity(game)
		return game

	@pytest.fixture
	def player(self, game):
		player = Player(2, 1, 0, 0, "Test Player")
		game.register_entity(player)
		return player

	def test_starting_hero_does_not_exist(self, player):
		assert player.starting_hero is None

	def test_starting_hero_from_initial_hero_entity_id(self, game, player):
		hero = Card(4, "HERO_02")
		game.register_entity(hero)
		player.initial_hero_entity_id = hero.id

		assert player.starting_hero == hero

	def test_starting_hero_from_hero_entity(self, game, player):
		hero = Card(4, "HERO_02")
		game.register_entity(hero)
		hero.tags.update({
			GameTag.CARDTYPE: CardType.HERO,
			GameTag.CONTROLLER: player.player_id,
		})

		assert player.starting_hero == hero

	def test_starting_hero_maestra(self, game, player):
		# Set by the exporter
		player.initial_hero_entity_id = 3

		# Create original hero
		fake_hero = Card(3, "HERO_07")
		fake_hero.tags = {
			GameTag.CONTROLLER: 1,
			GameTag.CARDTYPE: CardType.HERO,
		}
		game.register_entity(fake_hero)

		# At this point, the starting hero is the fake one (but we don't know that yet!)
		assert player.starting_hero == fake_hero

		# Start the game
		game.tag_change(GameTag.STEP, Step.MAIN_READY)

		# ...we play a Rogue card, which creates the real hero:
		real_hero = Card(4, "HERO_03")
		real_hero.tags = {
			GameTag.CONTROLLER: 1,
			GameTag.CARDTYPE: CardType.HERO,
			GameTag.CREATOR_DBID: 64674,
		}
		game.register_entity(real_hero)

		# At this point, we should have a new starting_hero
		assert player.starting_hero == real_hero

	def test_initial_deck(self, game, player):
		WISP = "CS2_231"

		wisp = Card(5, None)
		wisp.tags.update({
			GameTag.ZONE: Zone.DECK,
		})
		game.register_entity(wisp)
		wisp.reveal(WISP, {
			GameTag.CARDTYPE: CardType.MINION,
			GameTag.CONTROLLER: player.player_id,
		})

		assert list(player.initial_deck) == [wisp]

	def test_initial_deck_unknown(self, game, player):
		WISP = "CS2_231"

		wisp = Card(5, None)
		wisp.tags.update({
			GameTag.ZONE: Zone.DECK,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(wisp)
		wisp.reveal(WISP, {
			GameTag.CARDTYPE: CardType.MINION,
		})

		hidden = Card(6, None)
		hidden.tags.update({
			GameTag.ZONE: Zone.DECK,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(hidden)

		assert list(player.initial_deck) == [wisp, hidden]

	def test_initial_deck_with_souleathers_scythe(self, game, player):
		wisp = Card(5, None)
		wisp.tags.update({
			GameTag.ZONE: Zone.GRAVEYARD,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(wisp)

		scythe = Card(6, None)
		scythe.tags.update({
			GameTag.ZONE: Zone.DECK,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(scythe)

		assert list(player.initial_deck) == [wisp, scythe]

	def test_known_starting_deck_list(self, game, player):
		WISP = "CS2_231"

		wisp = Card(5, None)
		wisp.tags.update({
			GameTag.ZONE: Zone.DECK,
		})
		game.register_entity(wisp)
		wisp.reveal(WISP, {
			GameTag.CARDTYPE: CardType.MINION,
			GameTag.CONTROLLER: player.player_id,
		})

		assert player.known_starting_deck_list == [WISP]

	def test_known_starting_deck_list_duplicates(self, game, player):
		WISP = "CS2_231"

		wisp1 = Card(5, None)
		wisp1.tags.update({
			GameTag.ZONE: Zone.DECK,
		})
		game.register_entity(wisp1)
		wisp1.reveal(WISP, {
			GameTag.CARDTYPE: CardType.MINION,
			GameTag.CONTROLLER: player.player_id,
		})

		wisp2 = Card(5, None)
		wisp2.tags.update({
			GameTag.ZONE: Zone.DECK,
		})
		game.register_entity(wisp2)
		wisp2.reveal(WISP, {
			GameTag.CARDTYPE: CardType.MINION,
			GameTag.CONTROLLER: player.player_id,
		})

		assert player.known_starting_deck_list == [WISP, WISP]

	def test_known_starting_deck_list_with_zerus(self, game, player):
		ZERUS = "OG_123"
		ZERUS_DBF = 38475
		WISP = "CS2_231"

		zerus = Card(5, None)
		zerus.tags.update({
			GameTag.ZONE: Zone.DECK,
		})
		game.register_entity(zerus)
		zerus.reveal(WISP, {
			GameTag.CARDTYPE: CardType.MINION,
			GameTag.CONTROLLER: player.player_id,
			GameTag.TRANSFORMED_FROM_CARD: ZERUS_DBF,
		})

		assert player.known_starting_deck_list == [ZERUS]

	def test_known_starting_deck_list_with_unidentified_cards(self, game, player):
		UNIDENTIFIED_CONTRACT = "DAL_366"
		RECRUITMENT_CONTRACT = "DAL_366t2"

		contract = Card(5, None)
		contract.tags.update({
			GameTag.ZONE: Zone.DECK,
		})
		game.register_entity(contract)
		contract.reveal(RECRUITMENT_CONTRACT, {
			GameTag.CARDTYPE: CardType.SPELL,
			GameTag.CONTROLLER: player.player_id,
		})

		assert player.known_starting_deck_list == [UNIDENTIFIED_CONTRACT]

	def test_known_starting_deck_list_with_galakrond(self, game, player):
		GALAKROND = "DRG_600"
		GALAKROND_UPGRADE_1 = "DRG_600t2"
		GALAKROND_UPGRADE_2 = "DRG_600t3"

		galakrond = Card(13, None)
		galakrond.tags.update({
			GameTag.ZONE: Zone.DECK,
		})
		game.register_entity(galakrond)

		galakrond.reveal(GALAKROND, {
			GameTag.CARDTYPE: CardType.HERO,
			GameTag.CONTROLLER: player.player_id,
		})
		galakrond.change(GALAKROND_UPGRADE_1, {})
		galakrond.hide()

		assert player.known_starting_deck_list == [GALAKROND], \
			"Galakrond should be known after it was upgraded, even if not played"

		galakrond.reveal(GALAKROND_UPGRADE_1, {
			GameTag.CARDTYPE: CardType.HERO,
			GameTag.CONTROLLER: player.player_id,
		})
		galakrond.change(GALAKROND_UPGRADE_2, {})
		galakrond.hide()

		galakrond.tags.update({
			GameTag.ZONE: Zone.HAND,
		})
		galakrond.reveal(GALAKROND_UPGRADE_2, {
			GameTag.CARDTYPE: CardType.HERO,
			GameTag.CONTROLLER: player.player_id,
		})

		assert player.known_starting_deck_list == [GALAKROND]

	def test_known_starting_deck_list_with_maestra(self, game, player):
		MAESTRA = "SW_050"

		game.tag_change(GameTag.STEP, Step.MAIN_READY)

		real_hero = Card(4, "HERO_03")
		real_hero.tags = {
			GameTag.CONTROLLER: 1,
			GameTag.CARDTYPE: CardType.HERO,
			GameTag.CREATOR_DBID: 64674,
		}
		game.register_entity(real_hero)

		assert player.known_starting_deck_list == [MAESTRA]

	def test_known_starting_deck_list_with_souleaters_scythe(self, game, player):
		WISP = "CS2_231"
		SOULEATERS_SCYTHE = "RLK_214"
		BOUND_SOUL = "RLK_214t"

		wisp = Card(5, WISP)
		wisp.tags.update({
			GameTag.ZONE: Zone.GRAVEYARD,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(wisp)

		scythe = Card(6, None)
		scythe.tags.update({
			GameTag.ZONE: Zone.DECK,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(scythe)

		game.tag_change(GameTag.NEXT_STEP, Step.MAIN_READY)

		# Start of game: create souls
		game.tag_change(GameTag.NEXT_STEP, Step.MAIN_READY)

		soul = Card(7, None)
		soul.tags.update({
			GameTag.ZONE: Zone.DECK,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(scythe)
		soul.reveal(BOUND_SOUL, {})
		soul.hide()

		game.tag_change(GameTag.STEP, Step.MAIN_READY)

		# Draw the Scythe
		scythe.reveal(SOULEATERS_SCYTHE, {
			GameTag.CARDTYPE: CardType.SPELL,
			GameTag.CONTROLLER: player.player_id,
			GameTag.ZONE: Zone.HAND,
		})

		# Draw the Soul
		soul.reveal(BOUND_SOUL, {
			GameTag.CARDTYPE: CardType.SPELL,
			GameTag.CONTROLLER: player.player_id,
			GameTag.ZONE: Zone.HAND,
		})

		assert player.known_starting_deck_list == [WISP, SOULEATERS_SCYTHE]

	def test_known_starting_deck_list_with_tourist(self, game, player):
		HAMM = "VAC_340"
		TOURIST_VFX_ENCHANTMENT = "VAC_422e"

		tourist = Card(4, None)
		tourist.tags.update({
			GameTag.ZONE: Zone.DECK,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(tourist)

		vfx = Card(5, None)
		vfx.tags.update({
			GameTag.ZONE: Zone.SETASIDE,
			GameTag.CONTROLLER: player.player_id,
		})
		game.register_entity(vfx)
		vfx.reveal(TOURIST_VFX_ENCHANTMENT, {
			GameTag.CARDTYPE: CardType.ENCHANTMENT,
			GameTag.ATTACHED: player.id,
			GameTag.CREATOR: tourist.id,
		})

		# At some point we play an out-of-class card, and a fake tourist is shown
		fake_tourist = Card(6, HAMM)
		fake_tourist.tags.update({
			GameTag.CONTROLLER: player.player_id,
			GameTag.CREATOR: vfx.id,
			GameTag.ZONE: Zone.REMOVEDFROMGAME,
			GameTag.TOURIST: 2,
			GameTag.DRUID_TOURIST: 1,
		})
		game.register_entity(fake_tourist)

		assert player.known_starting_deck_list == [HAMM]

		tourist.reveal(HAMM, {})

		assert player.known_starting_deck_list == [HAMM]


class TestCard:
	def test_card(self):
		card1 = Card(4, "EX1_001")
		# The following should be instant.
		# If this test hangs, something's wrong in the caching mechanism...
		for i in range(1000):
			assert card1.base_tags.get(GameTag.HEALTH, 0) == 2

	def test_change_entity(self):
		card = Card(4, "EX1_001")
		assert card.card_id == "EX1_001"
		assert card.initial_card_id == "EX1_001"
		assert card.is_original_entity

		card.change("NEW1_030", {})
		assert card.card_id == "NEW1_030"
		assert card.initial_card_id == "EX1_001"
		assert not card.is_original_entity

		weapon = Card(4, None)
		assert not weapon.initial_card_id
		assert weapon.is_original_entity

		weapon.reveal("CS2_091", {GameTag.TRANSFORMED_FROM_CARD: 41420})
		assert weapon.card_id == "CS2_091"
		assert weapon.initial_card_id == "UNG_929"
		assert not weapon.is_original_entity

	def test_can_be_in_deck(self):
		card = Card(31, "HERO_05")
		card.tags.update({
			GameTag.CARD_SET: CardSet.HERO_SKINS,
		})
		assert card.can_be_in_deck

	def test_archthief_rafaam(self):
		card = Card(4, None)
		assert not card.initial_card_id
		assert card.is_original_entity

		card.reveal("CS2_091", {
			GameTag.CREATOR_DBID: 52119
		})
		assert card.card_id == "CS2_091"
		assert not card.initial_card_id
		assert not card.is_original_entity

		card.change("EX1_001", {})
		assert card.card_id == "EX1_001"
		assert not card.initial_card_id
		assert not card.is_original_entity

	def test_unidentified_contract(self):
		card = Card(4, None)
		assert not card.initial_card_id
		assert card.is_original_entity

		card.reveal("DAL_366", {})
		assert card.card_id == "DAL_366"
		assert card.initial_card_id == "DAL_366"

		card.change("DAL_366t3", {})
		assert card.card_id == "DAL_366t3"
		assert card.initial_card_id == "DAL_366"

	def test_shifter_zerus(self):
		card = Card(4, None)
		assert not card.initial_card_id
		assert card.is_original_entity

		card.reveal("GIL_650", {
			GameTag.TRANSFORMED_FROM_CARD: 38475
		})
		assert card.card_id == "GIL_650"
		assert card.initial_card_id == "OG_123"

	def test_swift_messenger(self):
		card = Card(4, None)
		assert not card.initial_card_id
		assert card.is_original_entity

		card.reveal("GIL_528t", {})
		assert card.card_id == "GIL_528t"
		assert card.initial_card_id == "GIL_528t"

	def test_invalid_transformed_from_card(self):
		card = Card(4, None)
		card.reveal("EX1_001", {GameTag.TRANSFORMED_FROM_CARD: 0})
		assert card.initial_card_id == "EX1_001"
