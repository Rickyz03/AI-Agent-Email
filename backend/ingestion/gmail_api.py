from typing import List, Dict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import email


class GmailAPI:
    def __init__(self, creds: Credentials):
        self.creds = creds
        self.service = build("gmail", "v1", credentials=creds)

    def fetch_unread(self) -> List[Dict]:
        results = (
            self.service.users()
            .messages()
            .list(userId="me", q="is:unread")
            .execute()
        )
        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            m = (
                self.service.users()
                .messages()
                .get(userId="me", id=msg["id"], format="raw")
                .execute()
            )
            raw = base64.urlsafe_b64decode(m["raw"])
            mime_msg = email.message_from_bytes(raw)
            emails.append(
                {
                    "id": msg["id"],
                    "from": mime_msg.get("From"),
                    "to": mime_msg.get("To"),
                    "subject": mime_msg.get("Subject"),
                    "body": self._get_body(mime_msg),
                }
            )
        return emails

    def _get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""
