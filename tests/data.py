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

OPTIONS_WITH_ERRORS = """
D 23:16:30.5267690 GameState.DebugPrintOptions() - id=38
D 23:16:30.5274350 GameState.DebugPrintOptions() -   option 0 type=END_TURN mainEntity= error=INVALID errorParam=
D 23:16:30.5292340 GameState.DebugPrintOptions() -   option 1 type=POWER mainEntity=[name=Shadow Word: Pain id=33 zone=HAND zonePos=1 cardId=CS2_234 player=1] error=NONE errorParam=
D 23:16:30.5304620 GameState.DebugPrintOptions() -     target 0 entity=[name=Friendly Bartender id=9 zone=PLAY zonePos=3 cardId=CFM_654 player=1] error=NONE errorParam=
D 23:16:30.5315490 GameState.DebugPrintOptions() -     target 1 entity=[name=Flame Juggler id=26 zone=PLAY zonePos=4 cardId=AT_094 player=1] error=NONE errorParam=
D 23:16:30.5326920 GameState.DebugPrintOptions() -     target 2 entity=[name=Friendly Bartender id=15 zone=PLAY zonePos=5 cardId=CFM_654 player=1] error=NONE errorParam=
D 23:16:30.5335050 GameState.DebugPrintOptions() -     target 3 entity=[name=UNKNOWN ENTITY [cardType=INVALID] id=44 zone=HAND zonePos=1 cardId= player=2] error=NONE errorParam=
D 23:16:30.5343760 GameState.DebugPrintOptions() -     target 4 entity=GameEntity error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5350590 GameState.DebugPrintOptions() -     target 5 entity=BehEh error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5357980 GameState.DebugPrintOptions() -     target 6 entity=The Innkeeper error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5365690 GameState.DebugPrintOptions() -     target 7 entity=[name=Tyrande Whisperwind id=64 zone=PLAY zonePos=0 cardId=HERO_09a player=1] error=REQ_MINION_TARGET errorParam=
D 23:16:30.5378770 GameState.DebugPrintOptions() -     target 8 entity=[name=Lesser Heal id=65 zone=PLAY zonePos=0 cardId=CS1h_001_H1 player=1] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5387770 GameState.DebugPrintOptions() -     target 9 entity=[name=Anduin Wrynn id=66 zone=PLAY zonePos=0 cardId=HERO_09 player=2] error=REQ_MINION_TARGET errorParam=
D 23:16:30.5396470 GameState.DebugPrintOptions() -     target 10 entity=[name=Lesser Heal id=67 zone=PLAY zonePos=0 cardId=CS1h_001 player=2] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5405690 GameState.DebugPrintOptions() -     target 11 entity=[name=Chillwind Yeti id=37 zone=PLAY zonePos=1 cardId=CS2_182 player=2] error=REQ_TARGET_MAX_ATTACK errorParam=3
D 23:16:30.5413980 GameState.DebugPrintOptions() -   option 2 type=POWER mainEntity=[name=The Coin id=68 zone=HAND zonePos=3 cardId=GAME_005 player=1] error=NONE errorParam=
D 23:16:30.5422920 GameState.DebugPrintOptions() -   option 3 type=POWER mainEntity=[name=Shadow Madness id=13 zone=HAND zonePos=4 cardId=EX1_334 player=1] error=NONE errorParam=
D 23:16:30.5431510 GameState.DebugPrintOptions() -     target 0 entity=[name=UNKNOWN ENTITY [cardType=INVALID] id=44 zone=HAND zonePos=1 cardId= player=2] error=NONE errorParam=
D 23:16:30.5454830 GameState.DebugPrintOptions() -     target 1 entity=GameEntity error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5477520 GameState.DebugPrintOptions() -     target 2 entity=BehEh error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5485390 GameState.DebugPrintOptions() -     target 3 entity=The Innkeeper error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5493210 GameState.DebugPrintOptions() -     target 4 entity=[name=Tyrande Whisperwind id=64 zone=PLAY zonePos=0 cardId=HERO_09a player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.5507390 GameState.DebugPrintOptions() -     target 5 entity=[name=Lesser Heal id=65 zone=PLAY zonePos=0 cardId=CS1h_001_H1 player=1] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5517260 GameState.DebugPrintOptions() -     target 6 entity=[name=Anduin Wrynn id=66 zone=PLAY zonePos=0 cardId=HERO_09 player=2] error=REQ_MINION_TARGET errorParam=
D 23:16:30.5527880 GameState.DebugPrintOptions() -     target 7 entity=[name=Lesser Heal id=67 zone=PLAY zonePos=0 cardId=CS1h_001 player=2] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5537070 GameState.DebugPrintOptions() -     target 8 entity=[name=Friendly Bartender id=9 zone=PLAY zonePos=3 cardId=CFM_654 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.5545530 GameState.DebugPrintOptions() -     target 9 entity=[name=Flame Juggler id=26 zone=PLAY zonePos=4 cardId=AT_094 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.5554740 GameState.DebugPrintOptions() -     target 10 entity=[name=Friendly Bartender id=15 zone=PLAY zonePos=5 cardId=CFM_654 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.5563420 GameState.DebugPrintOptions() -     target 11 entity=[name=Chillwind Yeti id=37 zone=PLAY zonePos=1 cardId=CS2_182 player=2] error=REQ_TARGET_MAX_ATTACK errorParam=3
D 23:16:30.5571950 GameState.DebugPrintOptions() -   option 4 type=POWER mainEntity=[name=Prophet Velen id=22 zone=DECK zonePos=0 cardId= player=1] error=NONE errorParam=
D 23:16:30.5581040 GameState.DebugPrintOptions() -   option 5 type=POWER mainEntity=[name=Lesser Heal id=65 zone=PLAY zonePos=0 cardId=CS1h_001_H1 player=1] error=NONE errorParam=
D 23:16:30.5590640 GameState.DebugPrintOptions() -     target 0 entity=[name=Tyrande Whisperwind id=64 zone=PLAY zonePos=0 cardId=HERO_09a player=1] error=NONE errorParam=
D 23:16:30.5599700 GameState.DebugPrintOptions() -     target 1 entity=[name=Anduin Wrynn id=66 zone=PLAY zonePos=0 cardId=HERO_09 player=2] error=NONE errorParam=
D 23:16:30.5609780 GameState.DebugPrintOptions() -     target 2 entity=[name=Friendly Bartender id=9 zone=PLAY zonePos=3 cardId=CFM_654 player=1] error=NONE errorParam=
D 23:16:30.5617920 GameState.DebugPrintOptions() -     target 3 entity=[name=Flame Juggler id=26 zone=PLAY zonePos=4 cardId=AT_094 player=1] error=NONE errorParam=
D 23:16:30.5626230 GameState.DebugPrintOptions() -     target 4 entity=[name=Friendly Bartender id=15 zone=PLAY zonePos=5 cardId=CFM_654 player=1] error=NONE errorParam=
D 23:16:30.5634360 GameState.DebugPrintOptions() -     target 5 entity=[name=Chillwind Yeti id=37 zone=PLAY zonePos=1 cardId=CS2_182 player=2] error=NONE errorParam=
D 23:16:30.5642140 GameState.DebugPrintOptions() -     target 6 entity=[name=UNKNOWN ENTITY [cardType=INVALID] id=44 zone=HAND zonePos=1 cardId= player=2] error=NONE errorParam=
D 23:16:30.5649970 GameState.DebugPrintOptions() -     target 7 entity=GameEntity error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5657040 GameState.DebugPrintOptions() -     target 8 entity=BehEh error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5663840 GameState.DebugPrintOptions() -     target 9 entity=The Innkeeper error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5853710 GameState.DebugPrintOptions() -     target 10 entity=[name=Lesser Heal id=65 zone=PLAY zonePos=0 cardId=CS1h_001_H1 player=1] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5866110 GameState.DebugPrintOptions() -     target 11 entity=[name=Lesser Heal id=67 zone=PLAY zonePos=0 cardId=CS1h_001 player=2] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5879360 GameState.DebugPrintOptions() -   option 6 type=POWER mainEntity=[name=Friendly Bartender id=9 zone=PLAY zonePos=3 cardId=CFM_654 player=1] error=NONE errorParam=
D 23:16:30.5888760 GameState.DebugPrintOptions() -     target 0 entity=[name=UNKNOWN ENTITY [cardType=INVALID] id=44 zone=HAND zonePos=1 cardId= player=2] error=NONE errorParam=
D 23:16:30.5899630 GameState.DebugPrintOptions() -     target 1 entity=GameEntity error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5906880 GameState.DebugPrintOptions() -     target 2 entity=BehEh error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5913550 GameState.DebugPrintOptions() -     target 3 entity=The Innkeeper error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5922220 GameState.DebugPrintOptions() -     target 4 entity=[name=Tyrande Whisperwind id=64 zone=PLAY zonePos=0 cardId=HERO_09a player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.5930550 GameState.DebugPrintOptions() -     target 5 entity=[name=Lesser Heal id=65 zone=PLAY zonePos=0 cardId=CS1h_001_H1 player=1] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5939620 GameState.DebugPrintOptions() -     target 6 entity=[name=Lesser Heal id=67 zone=PLAY zonePos=0 cardId=CS1h_001 player=2] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.5948320 GameState.DebugPrintOptions() -     target 7 entity=[name=Friendly Bartender id=9 zone=PLAY zonePos=3 cardId=CFM_654 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.5961510 GameState.DebugPrintOptions() -     target 8 entity=[name=Flame Juggler id=26 zone=PLAY zonePos=4 cardId=AT_094 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.5986050 GameState.DebugPrintOptions() -     target 9 entity=[name=Friendly Bartender id=15 zone=PLAY zonePos=5 cardId=CFM_654 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.5994940 GameState.DebugPrintOptions() -     target 10 entity=[name=Chillwind Yeti id=37 zone=PLAY zonePos=1 cardId=CS2_182 player=2] error=REQ_TARGET_TAUNTER errorParam=
D 23:16:30.6003150 GameState.DebugPrintOptions() -     target 11 entity=[name=Anduin Wrynn id=66 zone=PLAY zonePos=0 cardId=HERO_09 player=2] error=REQ_TARGET_TAUNTER errorParam=
D 23:16:30.6011520 GameState.DebugPrintOptions() -   option 7 type=POWER mainEntity=[name=Flame Juggler id=26 zone=PLAY zonePos=4 cardId=AT_094 player=1] error=NONE errorParam=
D 23:16:30.6019770 GameState.DebugPrintOptions() -     target 0 entity=[name=UNKNOWN ENTITY [cardType=INVALID] id=44 zone=HAND zonePos=1 cardId= player=2] error=NONE errorParam=
D 23:16:30.6027890 GameState.DebugPrintOptions() -     target 1 entity=GameEntity error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6034650 GameState.DebugPrintOptions() -     target 2 entity=BehEh error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6041340 GameState.DebugPrintOptions() -     target 3 entity=The Innkeeper error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6048310 GameState.DebugPrintOptions() -     target 4 entity=[name=Tyrande Whisperwind id=64 zone=PLAY zonePos=0 cardId=HERO_09a player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.6057680 GameState.DebugPrintOptions() -     target 5 entity=[name=Lesser Heal id=65 zone=PLAY zonePos=0 cardId=CS1h_001_H1 player=1] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6066080 GameState.DebugPrintOptions() -     target 6 entity=[name=Lesser Heal id=67 zone=PLAY zonePos=0 cardId=CS1h_001 player=2] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6074100 GameState.DebugPrintOptions() -     target 7 entity=[name=Friendly Bartender id=9 zone=PLAY zonePos=3 cardId=CFM_654 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.6082410 GameState.DebugPrintOptions() -     target 8 entity=[name=Flame Juggler id=26 zone=PLAY zonePos=4 cardId=AT_094 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.6090360 GameState.DebugPrintOptions() -     target 9 entity=[name=Friendly Bartender id=15 zone=PLAY zonePos=5 cardId=CFM_654 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.6098350 GameState.DebugPrintOptions() -     target 10 entity=[name=Chillwind Yeti id=37 zone=PLAY zonePos=1 cardId=CS2_182 player=2] error=REQ_TARGET_TAUNTER errorParam=
D 23:16:30.6106390 GameState.DebugPrintOptions() -     target 11 entity=[name=Anduin Wrynn id=66 zone=PLAY zonePos=0 cardId=HERO_09 player=2] error=REQ_TARGET_TAUNTER errorParam=
D 23:16:30.6114800 GameState.DebugPrintOptions() -   option 8 type=POWER mainEntity=[name=Friendly Bartender id=15 zone=PLAY zonePos=5 cardId=CFM_654 player=1] error=NONE errorParam=
D 23:16:30.6123260 GameState.DebugPrintOptions() -     target 0 entity=[name=UNKNOWN ENTITY [cardType=INVALID] id=44 zone=HAND zonePos=1 cardId= player=2] error=NONE errorParam=
D 23:16:30.6130940 GameState.DebugPrintOptions() -     target 1 entity=GameEntity error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6137570 GameState.DebugPrintOptions() -     target 2 entity=BehEh error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6143980 GameState.DebugPrintOptions() -     target 3 entity=The Innkeeper error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6151260 GameState.DebugPrintOptions() -     target 4 entity=[name=Tyrande Whisperwind id=64 zone=PLAY zonePos=0 cardId=HERO_09a player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.6159780 GameState.DebugPrintOptions() -     target 5 entity=[name=Lesser Heal id=65 zone=PLAY zonePos=0 cardId=CS1h_001_H1 player=1] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6168520 GameState.DebugPrintOptions() -     target 6 entity=[name=Lesser Heal id=67 zone=PLAY zonePos=0 cardId=CS1h_001 player=2] error=REQ_HERO_OR_MINION_TARGET errorParam=
D 23:16:30.6180250 GameState.DebugPrintOptions() -     target 7 entity=[name=Friendly Bartender id=9 zone=PLAY zonePos=3 cardId=CFM_654 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.6188420 GameState.DebugPrintOptions() -     target 8 entity=[name=Flame Juggler id=26 zone=PLAY zonePos=4 cardId=AT_094 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.6196650 GameState.DebugPrintOptions() -     target 9 entity=[name=Friendly Bartender id=15 zone=PLAY zonePos=5 cardId=CFM_654 player=1] error=REQ_ENEMY_TARGET errorParam=
D 23:16:30.6204660 GameState.DebugPrintOptions() -     target 10 entity=[name=Chillwind Yeti id=37 zone=PLAY zonePos=1 cardId=CS2_182 player=2] error=REQ_TARGET_TAUNTER errorParam=
D 23:16:30.6212910 GameState.DebugPrintOptions() -     target 11 entity=[name=Anduin Wrynn id=66 zone=PLAY zonePos=0 cardId=HERO_09 player=2] error=REQ_TARGET_TAUNTER errorParam=
D 23:16:30.6222210 GameState.DebugPrintOptions() -   option 9 type=POWER mainEntity=[name=Shadow Word: Death id=23 zone=HAND zonePos=2 cardId=EX1_622 player=1] error=REQ_TARGET_TO_PLAY errorParam=
D 23:16:30.6232190 GameState.DebugPrintOptions() -   option 10 type=POWER mainEntity=[name=Ragnaros the Firelord id=16 zone=HAND zonePos=5 cardId=EX1_298 player=1] error=REQ_ENOUGH_MANA errorParam=
D 23:16:30.6242450 GameState.DebugPrintOptions() -   option 11 type=POWER mainEntity=GameEntity error=REQ_YOUR_TURN errorParam=
D 23:16:30.6249860 GameState.DebugPrintOptions() -   option 12 type=POWER mainEntity=The Innkeeper error=REQ_YOUR_TURN errorParam=
D 23:16:30.6257420 GameState.DebugPrintOptions() -   option 13 type=POWER mainEntity=[name=Tyrande Whisperwind id=64 zone=PLAY zonePos=0 cardId=HERO_09a player=1] error=REQ_ATTACK_GREATER_THAN_0 errorParam=
D 23:16:30.6274730 GameState.DebugPrintOptions() -   option 14 type=POWER mainEntity=[name=Anduin Wrynn id=66 zone=PLAY zonePos=0 cardId=HERO_09 player=2] error=REQ_YOUR_TURN errorParam=
D 23:16:30.6284990 GameState.DebugPrintOptions() -   option 15 type=POWER mainEntity=[name=Lesser Heal id=67 zone=PLAY zonePos=0 cardId=CS1h_001 player=2] error=REQ_YOUR_TURN errorParam=
D 23:16:30.6293790 GameState.DebugPrintOptions() -   option 16 type=POWER mainEntity=[name=Chillwind Yeti id=37 zone=PLAY zonePos=1 cardId=CS2_182 player=2] error=REQ_YOUR_TURN errorParam=
D 23:16:30.6303440 GameState.DebugPrintOptions() -   option 17 type=POWER mainEntity=[name=UNKNOWN ENTITY [cardType=INVALID] id=44 zone=HAND zonePos=1 cardId= player=2] error=REQ_YOUR_TURN errorParam=
""".strip()
