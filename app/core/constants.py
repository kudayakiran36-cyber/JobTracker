APP_NAME = "Job Tracker"
APP_VERSION = "1.0.0"
SCHEMA_VERSION = "1.0"

STATUSES = ("Interested", "Applied", "Not Interested", "Rejected")
APPLICATION_DATE_TYPES = ("Exact", "Approximate")

# Fixed lifecycle timers. Reminder values below are user-configurable.
RECENTLY_VISITED_HOURS = 72
RECYCLE_BIN_HOURS = 24

ALLOWED_TRANSITIONS = {
    "Interested": {"Applied", "Not Interested", "Rejected"},
    "Applied": {"Interested", "Not Interested", "Rejected"},
    "Not Interested": {"Interested", "Rejected"},
    "Rejected": {"Interested", "Not Interested"},
}

DEFAULT_SETTINGS = {
    "applied_reminder_days": "3",
    "interested_first_reminder_days": "5",
    "interested_second_reminder_days": "8",
    "deadline_reminder_days": "3",
    "deadline_rejection_days": "3",
}
