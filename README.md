# Job Tracker 1.0

Personal, local-first Windows desktop job tracker built with Python, PySide6, SQLite and SQLAlchemy.

## What it does

- Tracks jobs in Interested, Applied, Not Interested and Rejected.
- Imports structured job JSON produced by an external AI/tool.
- Requires job title, company and job URL.
- Allows optional job details and NULL for missing data.
- Tracks application date and Exact/Approximate date type.
- Stores resumes locally and references them from applications.
- Maintains append-only meaningful History.
- Provides configurable reminders.
- Automatically moves Interested jobs to Rejected after the configured post-deadline period.
- Has Recently Visited (72 hours), Favorites and a 24-hour Recycle Bin.
- Includes an Update Center for manual Gmail/application matching.
- Supports one Gmail account at a time.
- Creates portable `.jtb` backups containing the database and resumes.
- Keeps UI/theme concerns separate from core services.
- Includes a loading screen.
- Uses no internal AI and does not scrape jobs.

## Run from source

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Conda is also supported.

## Gmail

Gmail is optional. Create an OAuth Desktop App credential in Google Cloud, save it as `credentials.json` beside the application, then use Update Center → Check Gmail. The first authorization opens a browser. The resulting token is local and should not be committed.

The app does not run background Gmail checks.

## Build a Windows executable

Build on Windows:

```bash
pip install -r requirements.txt
pyinstaller --noconfirm --clean --windowed --name JobTracker main.py
```

The executable will be under `dist\JobTracker\` for the default onedir build.

For a portable package, keep the executable and the `data` folder together. Copy/restore a `.jtb` backup on another PC.

## Data layout

```text
JobTracker/
  main.py
  app/
  data/
    jobtracker.db
    Resumes/
    Backups/
  resources/
  tests/
```

## Testing

```bash
pytest
```

## Notes

- `data/jobtracker.db` is created automatically.
- Resume paths are stored relative to the project data area.
- Restore makes a safety backup before replacing the current database/files.
- Recycle Bin expiry is measured exactly from the deletion timestamp.
- Recently Visited expiry is measured exactly from the latest visit.
