import json
from jsonschema import Draft202012Validator
from app.json_import.schema import SCHEMA
from app.core.exceptions import ValidationError

def validate_json_text(text):
    try: data = json.loads(text)
    except json.JSONDecodeError as e: raise ValidationError(f"Invalid JSON: {e}")
    errors = sorted(Draft202012Validator(SCHEMA).iter_errors(data), key=lambda e: list(e.path))
    if errors:
        raise ValidationError("; ".join(e.message for e in errors))
    return data
