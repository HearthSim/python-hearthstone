from io import StringIO

from hearthstone.stringsfile import load


TEST_STRINGS = """TAG	TEXT	COMMENT	AUDIOFILE
VO_ICC09_Saurfang_Male_Orc_CursedBlade_01	Who’s idea was this?
VO_ICC09_Saurfang_Male_Orc_Doomerang_01	Hmm… I gotta get one of those…

VO_ICC06_Marrowgar_Male_BoneWraith_Intro_01	None may enter the master's sanctum! 
VO_ICC06_Marrowgar_Male_BoneWraith_Bonespike_01	The only escape is death!"""  # noqa: W291


def test_load_blank_line():
	assert load(StringIO(TEST_STRINGS)) == {
		"VO_ICC09_Saurfang_Male_Orc_CursedBlade_01": {
			"TEXT": "Who’s idea was this?"
		},
		"VO_ICC09_Saurfang_Male_Orc_Doomerang_01": {
			"TEXT": "Hmm… I gotta get one of those…"
		},
		"VO_ICC06_Marrowgar_Male_BoneWraith_Intro_01": {
			"TEXT": "None may enter the master's sanctum! "
		},
		"VO_ICC06_Marrowgar_Male_BoneWraith_Bonespike_01": {
			"TEXT": "The only escape is death!"
		}
	}
