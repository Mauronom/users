import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from hex.mailing.domain.ports import MailSenderPort

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def _load_creds(token_path):
    try:
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(str(token_path), "w") as f:
                f.write(creds.to_json())
        return creds
    except Exception:
        return None


def get_gmail_service(token_path):
    creds = _load_creds(token_path)
    if not creds or not creds.valid:
        raise RuntimeError(
            f"No valid Gmail token at {token_path}. "
            "Run: python manage.py generate_gmail_token"
        )
    return build("gmail", "v1", credentials=creds)


def generate_token(credentials_path, token_path, port=8080):
    """OAuth2 flow: prints auth URL, user pastes back the redirect URL. No local server needed."""
    from urllib.parse import urlparse, parse_qs

    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
    flow.redirect_uri = f"http://localhost:{port}"
    auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")

    print(f"\nOpen this URL in your browser:\n\n  {auth_url}\n")
    print("After authorizing, your browser will show an error page — that's fine.")
    redirect_url = input("Paste the full URL from the browser address bar: ").strip()

    code = parse_qs(urlparse(redirect_url).query)["code"][0]
    flow.fetch_token(code=code)

    with open(str(token_path), "w") as f:
        f.write(flow.credentials.to_json())
    return flow.credentials


class GmailSender(MailSenderPort):
    def __init__(self, credentials_path, token_path):
        self.credentials_path = credentials_path
        self.token_path = token_path

    def send(self, mail):
        service = get_gmail_service(self.token_path)
        if mail.images or mail.attachments:
            message = MIMEMultipart("related")
            message["to"] = mail.contact.mail
            message["subject"] = mail.subject
            message.attach(MIMEText(mail.body, "html"))
            for cid, img_bytes in (mail.images or {}).items():
                print(cid)
                print("MimeType")
                img = MIMEImage(img_bytes)
                img.add_header("Content-ID", f"<{cid}>")
                img.add_header("Content-Disposition", "inline")
                print("attachbefore")
                message.attach(img)
                print("attachafter")
            for name, data in (mail.attachments or []):
                part = MIMEBase("application", "octet-stream")
                part.set_payload(data)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{name}"')
                message.attach(part)
        else:
            message = MIMEText(mail.body, "html")
            message["to"] = mail.contact.mail
            message["subject"] = mail.subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
