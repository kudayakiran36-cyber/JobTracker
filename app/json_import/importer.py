from datetime import date
from app.json_import.validator import validate_json_text
from app.core.constants import SCHEMA_VERSION

def parse(text):
    data = validate_json_text(text)
    data.setdefault("schema_version", SCHEMA_VERSION)
    if data.get("deadline"):
        data["deadline"] = date.fromisoformat(data["deadline"])
    return data
