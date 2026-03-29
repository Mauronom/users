from django.core.management.base import BaseCommand
from django.conf import settings
from hex.mailing.infra.gmail_sender import generate_token


class Command(BaseCommand):
    help = "OAuth2 flow to generate token.json for Gmail API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--port", type=int, default=8080,
            help="Local port for the OAuth redirect (default: 8080)"
        )

    def handle(self, *args, **options):
        port = options["port"]
        self.stdout.write(
            f"Starting OAuth flow on port {port}.\n"
            f"If running in Docker, make sure port {port} is forwarded:\n"
            f"  docker run -p {port}:{port} ...\n"
            "A URL will be printed — open it in your browser.\n"
            "After authorizing, you'll be redirected to localhost and the token will be saved.\n"
        )
        generate_token(settings.GMAIL_CREDENTIALS_PATH, settings.GMAIL_TOKEN_PATH, port=port)
        self.stdout.write(self.style.SUCCESS(f"token.json written to {settings.GMAIL_TOKEN_PATH}"))
