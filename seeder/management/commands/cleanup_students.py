from django.core.management import BaseCommand

from authentication.models import User


class Command(BaseCommand):
    help = "Delete all users with role STUDENT."

    def add_arguments(self, parser):
        parser.add_argument("--noinput", "--yes", action="store_true",
                            help="Skip the confirmation prompt.")

    def handle(self, *args, **options):
        students = User.objects.filter(role=User.Role.STUDENT)
        count = students.count()
        if count == 0:
            self.stdout.write("No students found.")
            return

        if not options["noinput"]:
            try:
                answer = input(f"WARNING. THIS ACTION CANNOT BE UNDONE: Delete {count} students? [y/N] ")
            except EOFError:
                self.stdout.write("No TTY available. Use --noinput with the command.")
                return
            if answer.strip().lower() != "y":
                self.stdout.write("Aborted.")
                return

        deleted, _ = students.delete()
        self.stdout.write(f"Deleted {deleted} records ({count} students + related).")
