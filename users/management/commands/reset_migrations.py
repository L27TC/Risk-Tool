from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Resets migration history for the specified app.'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations WHERE app='admin';")
            cursor.execute("DELETE FROM django_migrations WHERE app='users';")
            self.stdout.write(self.style.SUCCESS('Successfully reset migration history for admin and users apps.'))
