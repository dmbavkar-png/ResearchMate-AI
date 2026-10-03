import base64
from email import policy
from email.parser import BytesParser

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailTool:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly"
    ]

    def __init__(self):
        project_dir = Path(__file__).resolve().parent.parent
        self.credentials_path = (
            project_dir / "credentials" / "credentials.json"
        )
        self.token_path = (
            project_dir / "credentials" / "token.json"
        )
        self.service = None

    def authenticate(self):
        creds = None

        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(
                str(self.token_path),
                self.SCOPES,
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    raise FileNotFoundError(
                        "Missing credentials/credentials.json. "
                        "Place your Google OAuth Desktop client "
                        "JSON file there."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path),
                    self.SCOPES,
                )
                creds = flow.run_local_server(port=0)

            self.token_path.write_text(
                creds.to_json(),
                encoding="utf-8",
            )

        self.service = build(
            "gmail",
            "v1",
            credentials=creds,
            cache_discovery=False,
        )
        return True

    def list_emails(self, max_results=5):
        if self.service is None:
            self.authenticate()

        result = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                labelIds=["INBOX"],
                maxResults=max_results,
            )
            .execute()
        )

        emails = []

        for item in result.get("messages", []):
            message = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=item["id"],
                    format="metadata",
                    metadataHeaders=["From", "Subject", "Date"],
                )
                .execute()
            )

            headers = {
                header["name"].lower(): header["value"]
                for header in message.get("payload", {}).get(
                    "headers", []
                )
            }

            emails.append({
                "id": item["id"],
                "from": headers.get("from", ""),
                "subject": headers.get("subject", "(No subject)"),
                "date": headers.get("date", ""),
            })

        return emails
        
    def search_emails(self, query, max_results=10):
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Enter a search keyword or Gmail query.")

        if self.service is None:
            self.authenticate()

        result = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                q=query.strip(),
                maxResults=max_results,
            )
            .execute()
        )

        emails = []

        for item in result.get("messages", []):
            message = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=item["id"],
                    format="metadata",
                    metadataHeaders=["From", "Subject", "Date"],
                )
                .execute()
            )

            headers = {
                header["name"].lower(): header["value"]
                for header in message.get("payload", {}).get(
                    "headers", []
                )
            }

            emails.append({
                "id": item["id"],
                "from": headers.get("from", ""),
                "subject": headers.get("subject", "(No subject)"),
                "date": headers.get("date", ""),
            })

        return emails

    def read_email(self, message_id):
        if not isinstance(message_id, str) or not message_id.strip():
            raise ValueError("A Gmail message ID is required.")

        if self.service is None:
            self.authenticate()

        result = (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id.strip(),
                format="raw",
            )
            .execute()
        )

        encoded = result["raw"]
        encoded += "=" * (-len(encoded) % 4)

        raw_message = base64.urlsafe_b64decode(encoded)
        message = BytesParser(policy=policy.default).parsebytes(
            raw_message
        )

        # Prefer plain text, excluding attachment parts.
        body_part = message.get_body(preferencelist=("plain",))
        body_format = "plain"

        if body_part is None:
            body_part = message.get_body(preferencelist=("html",))
            body_format = "html"

        body = (
            body_part.get_content()
            if body_part is not None
            else "(No readable message body found.)"
        )

        return {
            "id": result["id"],
            "from": str(message.get("From", "")),
            "to": str(message.get("To", "")),
            "subject": str(message.get("Subject", "(No subject)")),
            "date": str(message.get("Date", "")),
            "body": body,
            "body_format": body_format,
        }