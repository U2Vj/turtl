import secrets
from pathlib import Path

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand, CommandError
from django.db import transaction

from authentication.models import User
from catalog.models import Classroom
from enrollments.models import Enrollment


ANIMALS = [
    "fox", "otter", "bear", "wolf", "eagle", "hawk", "lynx", "panda", "tiger",
    "lion", "koala", "moose", "deer", "owl", "raven", "seal", "shark", "whale",
    "zebra", "badger", "beaver", "falcon", "heron", "puma",
]
ALPHABET = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def make_password_string(length):
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def make_email(used, count, domain):
    while True:
        candidate = f"{secrets.choice(ANIMALS)}-{count}@{domain}"
        if candidate in used or User.objects.filter(email=candidate).exists():
            continue
        used.add(candidate)
        return candidate


class Command(BaseCommand):
    help = "Generate student users for a classroom and output credentials in a printable file"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)
        parser.add_argument("classroom_id", type=int)
        parser.add_argument("--domain", default="turtl")
        parser.add_argument("--password-length", type=int, default=10)
        parser.add_argument("--output", default="users.html")

    def handle(self, *args, **options):
        count = options["count"]
        try:
            classroom = Classroom.objects.get(pk=options["classroom_id"])
        except Classroom.DoesNotExist:
            raise CommandError(f"Classroom {options['classroom_id']} does not exist.")

        created = []
        used = set()
        with transaction.atomic():
            for i in range(count):
                email = make_email(used, i, options["domain"])
                password = make_password_string(options["password_length"])
                user = User.objects.create(
                    email=email,
                    username=email.split("@")[0],
                    password=make_password(password),
                    role=User.Role.STUDENT,
                )
                Enrollment.objects.create(classroom=classroom, student=user)
                created.append((email, password))

        output = Path(options["output"]).resolve()
        output.write_text(render_html(created), encoding="utf-8")
        self.stdout.write(f"{count} Users added. List: {output}")


def render_html(users):
    cards = "\n".join(
        f'<div class="card">'
        f'<div>turtl.seclab.inf.fh-dortmund.de</div>'
        f'<div>Email: <code>{email}</code></div>'
        f'<div>Password: <code>{password}</code></div></div>'
        for email, password in users
    )
    return (
        '<!doctype html><meta charset="utf-8">'
        '<style>'
        '@page{size:A4;margin:10mm}'
        '.sheet{display:grid;grid-template-columns:1fr 1fr}'
        '.card{border:1px dashed #888;padding:6mm;min-height:30mm;page-break-inside:avoid;box-sizing:border-box;margin:-0.5px}'
        'code{font-size:11pt}'
        '</style>'
        f'<div class="sheet">{cards}</div>'
    )
