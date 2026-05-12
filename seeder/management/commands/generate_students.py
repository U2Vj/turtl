import argparse
import secrets
from pathlib import Path

from django.core.management import BaseCommand, CommandError
from django.db import transaction

from authentication.models import User
from catalog.models import Classroom
from enrollments.models import Enrollment


def valid_int(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer")
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"{value!r} must be >= 1")
    return ivalue


ANIMALS = [
    "fox", "otter", "bear", "wolf", "eagle", "hawk", "lynx", "panda", "tiger",
    "lion", "koala", "moose", "deer", "owl", "raven", "seal", "shark", "whale",
    "zebra", "badger", "beaver", "falcon", "heron", "puma",
]
ALPHABET = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def make_password(length):
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def make_email(used, count, domain):
    failcount = 0
    while failcount < 100:
        candidate = f"{secrets.choice(ANIMALS)}-{count}@{domain}"
        if candidate in used or User.objects.filter(email=candidate).exists():
            failcount += 1
            continue
        used.add(candidate)
        return candidate
    raise CommandError("Failed to generate unique email after 100 attempts.")

class Command(BaseCommand):
    help = "Generate student users for a classroom and output credentials in a printable file"

    def add_arguments(self, parser):
        parser.add_argument("count", type=valid_int)
        parser.add_argument("classroom_id", type=valid_int)
        parser.add_argument("--domain", default="turtl")
        parser.add_argument("--password-length", type=valid_int, default=10)
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
                password = make_password(options["password_length"])
                user = User.objects.create_student(email=email, password=password)
                user.username = email.split("@")[0]
                user.save()
                Enrollment.objects.create(classroom=classroom, student=user)
                created.append((email, password))

        output = Path(options["output"]).resolve()
        output.write_text(render_html(created), encoding="utf-8")
        self.stdout.write(f"{count} Users added. List: {output}")


def render_html(users):
    cards = "\n".join(
        f'<div class="card">'
        f'<div class="tag">TURTL</div>'
        f'<div>Email: <code>{email}</code></div>'
        f'<div>Password: <code>{password}</code></div></div>'
        for email, password in users
    )
    return (
        '<!doctype html><meta charset="utf-8">'
        '<style>'
        '@page{size:A4;margin:10mm}'
        '.sheet{display:grid;grid-template-columns:1fr 1fr}'
        '.tag{font-size:10pt;font-weight:bold;margin-bottom:4mm}'
        '.card{border:1px dashed #888;padding:6mm;min-height:30mm;page-break-inside:avoid;box-sizing:border-box;margin:-0.5px}'
        'code{font-size:11pt}'
        '</style>'
        f'<div class="sheet">{cards}</div>'
    )
