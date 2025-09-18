import imaplib
import email
from email.header import decode_header
from typing import List, Optional
from utils.settings import settings


class ParsedEmail:
    def __init__(self, subject, from_addr, to_addrs, body, language="it"):
        self.subject = subject
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.body = body
        self.language = language


class IMAPClient:
    def __init__(
        self,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        port: Optional[int] = None,
    ):
        self.host = host or settings.IMAP_HOST
        self.port = port or settings.IMAP_PORT
        self.username = username or settings.IMAP_USERNAME
        self.password = password or settings.IMAP_PASSWORD


    def fetch_n_unread_mails(self, n: int) -> List[ParsedEmail]:
        """
        Connect to IMAP server and fetch the last n unseen emails.
        Returns a list of ParsedEmail objects.
        """
        if not self.username or not self.password:
            return []

        conn = imaplib.IMAP4_SSL(self.host, self.port)
        conn.login(self.username, self.password)
        conn.select("inbox")

        status, messages = conn.search(None, "UNSEEN")
        all_ids = messages[0].split()
        last_n_ids = all_ids[-n:] if n > 0 else all_ids

        parsed_emails = []
        for num in last_n_ids:
            _, data = conn.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, _ = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            from_addr = msg.get("From")
            to_addrs = msg.get_all("To", [])

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            parsed_emails.append(
                ParsedEmail(
                    subject=subject,
                    from_addr=from_addr,
                    to_addrs=to_addrs,
                    body=body,
                )
            )

        conn.close()
        conn.logout()
        return parsed_emails


    def fetch_n_mails(self, n: int) -> List[ParsedEmail]:
        """
        Connect to IMAP server and fetch the last n emails from the inbox.
        Returns a list of ParsedEmail objects.
        """
        if not self.username or not self.password:
            return []

        conn = imaplib.IMAP4_SSL(self.host, self.port)
        conn.login(self.username, self.password)
        conn.select("inbox")

        status, messages = conn.search(None, "ALL")
        all_ids = messages[0].split()
        last_n_ids = all_ids[-n:] if n > 0 else all_ids

        parsed_emails = []
        for num in last_n_ids:
            _, data = conn.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, _ = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            from_addr = msg.get("From")
            to_addrs = msg.get_all("To", [])

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            parsed_emails.append(
                ParsedEmail(
                    subject=subject,
                    from_addr=from_addr,
                    to_addrs=to_addrs,
                    body=body,
                )
            )

        conn.close()
        conn.logout()
        return parsed_emails

