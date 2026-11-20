import pytest
from app.utils.helpers import mask_phone, format_currency

def test_mask_phone_standard():
    assert mask_phone("+919876543210") == "+91 98xxx xxxxx"

def test_mask_phone_without_country_code():
    assert mask_phone("9876543210") == "98xxx xxxxx"

def test_mask_phone_empty():
    assert mask_phone("") == ""
    assert mask_phone(None) == ""

def test_format_currency_hour():
    assert format_currency(120, "hour") == "₹120/hr"

def test_format_currency_day():
    assert format_currency(600, "day") == "₹600/day"
