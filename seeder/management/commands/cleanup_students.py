from django.core.management import BaseCommand

from authentication.models import User


class Command(BaseCommand):
    help = "Delete all users with role STUDENT."

    def handle(self, *args, **options):
        students = User.objects.filter(role=User.Role.STUDENT)
        count = students.count()
        if count == 0:
            self.stdout.write("No students found.")
            return

        answer = input(f"Delete {count} students? [y/N] ")
        if answer.strip().lower() != "y":
            self.stdout.write("Aborted.")
            return

        deleted, _ = students.delete()
        self.stdout.write(f"Deleted {deleted} records ({count} students + related).")
