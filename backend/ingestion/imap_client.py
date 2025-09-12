import imaplib
import email
from email.header import decode_header
from typing import List


class ParsedEmail:
    def __init__(self, subject, from_addr, to_addrs, body, language="it"):
        self.subject = subject
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.body = body
        self.language = language


class IMAPClient:
    def __init__(self, host: str = "imap.gmail.com", username: str = None, password: str = None):
        self.host = host
        self.username = username
        self.password = password

    def fetch_unseen(self) -> List[ParsedEmail]:
        """
        Connect to IMAP server and fetch unseen emails.
        Returns a list of ParsedEmail objects.
        """
        if not self.username or not self.password:
            return []

        conn = imaplib.IMAP4_SSL(self.host)
        conn.login(self.username, self.password)
        conn.select("inbox")

        status, messages = conn.search(None, "UNSEEN")
        parsed_emails = []

        for num in messages[0].split():
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
