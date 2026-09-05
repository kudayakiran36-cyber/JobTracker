import pytest
from app.json_import.validator import validate_json_text
from app.core.exceptions import ValidationError
def test_valid():
    x=validate_json_text('{"job_title":"Python Developer","company_name":"Acme","job_url":"https://example.com"}')
    assert x["job_title"]=="Python Developer"
def test_invalid():
    with pytest.raises(ValidationError): validate_json_text('{"company_name":"Acme"}')
