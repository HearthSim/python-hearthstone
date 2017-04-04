from __future__ import unicode_literals


EMPTY_GAME = """
D 02:59:14.6088620 GameState.DebugPrintPower() - CREATE_GAME
D 02:59:14.6149420 GameState.DebugPrintPower() -     GameEntity EntityID=1
D 02:59:14.6446530 GameState.DebugPrintPower() -     Player EntityID=2 PlayerID=1 GameAccountId=[hi=1 lo=0]
D 02:59:14.6481950 GameState.DebugPrintPower() -     Player EntityID=3 PlayerID=2 GameAccountId=[hi=3 lo=2]
""".strip()

INITIAL_GAME = """
D 02:59:14.6088620 GameState.DebugPrintPower() - CREATE_GAME
D 02:59:14.6149420 GameState.DebugPrintPower() -     GameEntity EntityID=1
D 02:59:14.6420450 GameState.DebugPrintPower() -         tag=TURN value=1
D 02:59:14.6428100 GameState.DebugPrintPower() -         tag=ZONE value=PLAY
D 02:59:14.6430430 GameState.DebugPrintPower() -         tag=ENTITY_ID value=1
D 02:59:14.6436240 GameState.DebugPrintPower() -         tag=NEXT_STEP value=BEGIN_MULLIGAN
D 02:59:14.6438920 GameState.DebugPrintPower() -         tag=CARDTYPE value=GAME
D 02:59:14.6442880 GameState.DebugPrintPower() -         tag=STATE value=RUNNING
D 02:59:14.6446530 GameState.DebugPrintPower() -     Player EntityID=2 PlayerID=1 GameAccountId=[hi=1 lo=0]
D 02:59:14.6450220 GameState.DebugPrintPower() -         tag=PLAYSTATE value=PLAYING
D 02:59:14.6463220 GameState.DebugPrintPower() -         tag=PLAYER_ID value=1
D 02:59:14.6466060 GameState.DebugPrintPower() -         tag=TEAM_ID value=1
D 02:59:14.6469080 GameState.DebugPrintPower() -         tag=ZONE value=PLAY
D 02:59:14.6470710 GameState.DebugPrintPower() -         tag=CONTROLLER value=1
D 02:59:14.6472580 GameState.DebugPrintPower() -         tag=ENTITY_ID value=2
D 02:59:14.6476340 GameState.DebugPrintPower() -         tag=CARDTYPE value=PLAYER
D 02:59:14.6481950 GameState.DebugPrintPower() -     Player EntityID=3 PlayerID=2 GameAccountId=[hi=3 lo=2]
D 02:59:14.6483770 GameState.DebugPrintPower() -         tag=PLAYSTATE value=PLAYING
D 02:59:14.6485530 GameState.DebugPrintPower() -         tag=CURRENT_PLAYER value=1
D 02:59:14.6486970 GameState.DebugPrintPower() -         tag=FIRST_PLAYER value=1
D 02:59:14.6492590 GameState.DebugPrintPower() -         tag=PLAYER_ID value=2
D 02:59:14.6493880 GameState.DebugPrintPower() -         tag=TEAM_ID value=2
D 02:59:14.6495200 GameState.DebugPrintPower() -         tag=ZONE value=PLAY
D 02:59:14.6496470 GameState.DebugPrintPower() -         tag=CONTROLLER value=2
D 02:59:14.6497780 GameState.DebugPrintPower() -         tag=ENTITY_ID value=3
D 02:59:14.6500380 GameState.DebugPrintPower() -         tag=CARDTYPE value=PLAYER
""".strip()

FULL_ENTITY = """D 22:25:48.0678873 GameState.DebugPrintPower() - FULL_ENTITY - Creating ID=4 CardID=
D 22:25:48.0678873 GameState.DebugPrintPower() -     tag=ZONE value=DECK
D 22:25:48.0678873 GameState.DebugPrintPower() -     tag=CONTROLLER value=1
D 22:25:48.0678873 GameState.DebugPrintPower() -     tag=ENTITY_ID value=4
""".strip()

INVALID_GAME = """
D 02:59:14.6088620 GameState.DebugPrintPower() - CREATE_GAME
D 02:59:14.6149420 GameState.DebugPrintPower() -     GameEntity EntityID=1
D 02:59:14.6428100 GameState.DebugPrintPower() -         tag=ZONE value=PLAY
D 02:59:14.6481950 GameState.DebugPrintPower() -     Player EntityID=3 PlayerID=2 GameAccountId=[hi=3 lo=2]
D 02:59:14.6483770 GameState.DebugPrintPower() -         tag=PLAYSTATE value=PLAYING
D 02:59:14.6492590 GameState.DebugPrintPower() -         tag=PLAYER_ID value=2
""".strip() + "\n" + FULL_ENTITY

CONTROLLER_CHANGE = """
D 22:25:48.0708939 GameState.DebugPrintPower() - TAG_CHANGE Entity=4 tag=CONTROLLER value=2
""".strip()
