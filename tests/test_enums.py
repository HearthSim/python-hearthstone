from datetime import datetime
from hearthstone import enums


def test_zodiac_dates():
	assert enums.ZodiacYear.as_of_date(datetime(2014, 1, 1)) == enums.ZodiacYear.PRE_STANDARD
	assert enums.ZodiacYear.as_of_date(datetime(2016, 1, 1)) == enums.ZodiacYear.PRE_STANDARD
	assert enums.ZodiacYear.as_of_date(datetime(2016, 6, 1)) == enums.ZodiacYear.KRAKEN
	assert enums.ZodiacYear.as_of_date(datetime(2017, 1, 1)) == enums.ZodiacYear.KRAKEN
	assert enums.ZodiacYear.as_of_date(datetime(2017, 5, 1)) == enums.ZodiacYear.MAMMOTH
