import imaplib
import email
from email.header import decode_header
from typing import List, Dict


class IMAPClient:
    def __init__(self, host: str, username: str, password: str, ssl: bool = True):
        self.host = host
        self.username = username
        self.password = password
        self.ssl = ssl
        self.conn = None

    def connect(self):
        if self.ssl:
            self.conn = imaplib.IMAP4_SSL(self.host)
        else:
            self.conn = imaplib.IMAP4(self.host)
        self.conn.login(self.username, self.password)

    def fetch_unseen(self, mailbox: str = "INBOX") -> List[Dict]:
        self.conn.select(mailbox)
        status, messages = self.conn.search(None, "UNSEEN")
        email_ids = messages[0].split()

        results = []
        for eid in email_ids:
            status, msg_data = self.conn.fetch(eid, "(RFC822)")
            if status != "OK":
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            results.append({
                "id": eid.decode(),
                "from": msg.get("From"),
                "to": msg.get("To"),
                "subject": subject,
                "body": self._get_body(msg)
            })
        return results

    def _get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""
