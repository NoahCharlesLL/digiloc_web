import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DRAWINGS_FILE = DATA_DIR / "area_drawings.json"

POI_ICONS = {
    "toilet": ("tint", "#4FA8E0"),
    "wifi": ("wifi", "#5BC27A"),
    "power": ("bolt", "#E05B5B"),
}

def load_locations():
    with open(DATA_DIR / "locations.json", encoding="utf-8") as f:
        return json.load(f)

def load_drawings():
    if DRAWINGS_FILE.exists():
        with open(DRAWINGS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_drawings(drawings):
    with open(DRAWINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(drawings, f, indent=2)