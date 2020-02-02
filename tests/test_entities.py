import pytest

from hearthstone.entities import Card, Game, Player
from hearthstone.enums import GameTag


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

	def test_player(self, game):
		player = Player(2, 1, 0, 0, "Test Player")
		player.game = game

		assert player.starting_hero is None


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
