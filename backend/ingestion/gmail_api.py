from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import List
import base64
import email


class ParsedEmail:
    def __init__(self, subject, from_addr, to_addrs, body, language="it"):
        self.subject = subject
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.body = body
        self.language = language


class GmailAPI:
    def __init__(self, token_path: str = "ingestion/token.json", creds_path: str = "ingestion/credentials.json"):
        """
        Initialize Gmail API client.
        Requires credentials.json (OAuth2 client secrets) and token.json (user access token) under ingestion/.
        """
        self.creds = Credentials.from_authorized_user_file(token_path)

        # Build service
        self.service = build("gmail", "v1", credentials=self.creds)

    def fetch_unread(self) -> List[ParsedEmail]:
        """
        Fetch unread messages from Gmail inbox.
        """
        results = self.service.users().messages().list(userId="me", q="is:unread").execute()
        messages = results.get("messages", [])
        parsed_emails = []

        for msg in messages:
            msg_data = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
            payload = msg_data["payload"]
            headers = payload["headers"]

            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
            from_addr = next((h["value"] for h in headers if h["name"] == "From"), "")
            to_addrs = [h["value"] for h in headers if h["name"] == "To"]

            body = ""
            if "data" in payload["body"]:
                body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
            elif "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain":
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break

            parsed_emails.append(
                ParsedEmail(
                    subject=subject,
                    from_addr=from_addr,
                    to_addrs=to_addrs,
                    body=body,
                )
            )

        return parsed_emails


    def fetch_n_mails(self, n: int) -> List[ParsedEmail]:
        """
        Fetch the last n messages from Gmail inbox.
        """
        results = self.service.users().messages().list(userId="me", maxResults=n).execute()
        messages = results.get("messages", [])
        parsed_emails = []

        for msg in messages:
            msg_data = self.service.users().messages().get(userId="me", id=msg["id"]).execute()
            payload = msg_data["payload"]
            headers = payload["headers"]

            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
            from_addr = next((h["value"] for h in headers if h["name"] == "From"), "")
            to_addrs = [h["value"] for h in headers if h["name"] == "To"]

            body = ""
            if "data" in payload["body"]:
                body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
            elif "parts" in payload:
                for part in payload["parts"]:
                    if part["mimeType"] == "text/plain":
                        body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                        break

            parsed_emails.append(
                ParsedEmail(
                    subject=subject,
                    from_addr=from_addr,
                    to_addrs=to_addrs,
                    body=body,
                )
            )

        return parsed_emails

