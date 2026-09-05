from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from googleapiclient.discovery import build

class GmailClient:
    def __init__(self, credentials):
        self.service = build("gmail", "v1", credentials=credentials)
    def list_messages(self, max_results=100):
        result = self.service.users().messages().list(userId="me", maxResults=max_results).execute()
        rows = []
        for item in result.get("messages", []):
            msg = self.service.users().messages().get(
                userId="me", id=item["id"], format="metadata",
                metadataHeaders=["From","Subject","Date"]
            ).execute()
            headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
            received = None
            if headers.get("date"):
                try: received = parsedate_to_datetime(headers["date"]).astimezone().replace(tzinfo=None)
                except Exception: pass
            rows.append({
                "gmail_message_id": msg["id"], "thread_id": msg.get("threadId"),
                "sender": headers.get("from"), "subject": headers.get("subject"),
                "received_at": received, "snippet": msg.get("snippet"),
                "gmail_link": f"https://mail.google.com/mail/u/0/#all/{msg['id']}"
            })
        return rows
