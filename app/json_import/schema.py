SCHEMA = {
  "type": "object",
  "required": ["job_title", "company_name", "job_url"],
  "properties": {
    "schema_version": {"type": "string"},
    "job_title": {"type": "string", "minLength": 1},
    "company_name": {"type": "string", "minLength": 1},
    "job_url": {"type": "string", "minLength": 1},
    "location": {"type": ["string", "null"]},
    "work_arrangement": {"type": ["string", "null"]},
    "salary": {"type": ["string", "null"]},
    "job_description": {"type": ["string", "null"]},
    "required_skills": {"type": ["array", "null"], "items": {"type": "string"}},
    "preferred_skills": {"type": ["array", "null"], "items": {"type": "string"}},
    "experience_required": {"type": ["string", "null"]},
    "job_type": {"type": ["string", "null"]},
    "deadline": {"type": ["string", "null"], "pattern": r"^\d{4}-\d{2}-\d{2}$"}
  },
  "additionalProperties": False
}
