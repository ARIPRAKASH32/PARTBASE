import pytest
from app.utils.i18n import translate_category, translate_day

def test_translate_category():
    assert translate_category("shop_helper") == "கடை உதவியாளர்"
    assert translate_category("packing") == "பேக்கிங் உதவியாளர்"
    assert translate_category("unknown_role") == "Unknown Role"

def test_translate_day():
    assert translate_day("today") == "இன்று"
    assert translate_day("tomorrow") == "நாளை"
    assert translate_day("other") == "Other"
