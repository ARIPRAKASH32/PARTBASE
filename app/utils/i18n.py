"""
Tamil & English localization dictionary for Chennai pilot clusters.
"""

JOB_CATEGORIES_TA = {
    "shop_helper": "கடை உதவியாளர்",
    "packing": "பேக்கிங் உதவியாளர்",
    "cashier": "பணப் பதிவாளர் / பில்லிங்",
    "cleaning": "சுத்தம் செய்தல்",
    "data_entry": "டேட்டா என்ட்ரி",
    "delivery": "டெலிவரி உதவியாளர்",
    "promoter": "கடை விளம்பரதாரர்"
}

DAYS_TA = {
    "today": "இன்று",
    "tomorrow": "நாளை",
    "weekend": "வார இறுதி"
}

def translate_category(category_key):
    """Return Tamil name for category or formatted english fallback."""
    return JOB_CATEGORIES_TA.get(category_key, category_key.replace('_', ' ').title())

def translate_day(day_key):
    """Return Tamil name for day option or fallback."""
    return DAYS_TA.get(day_key, day_key.title())
