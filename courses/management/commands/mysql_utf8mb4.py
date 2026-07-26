"""
Convert the MySQL database and every table to utf8mb4 / utf8mb4_unicode_ci.

Emoji and other 4-byte characters throw `Incorrect string value` on 3-byte
`utf8` columns. Run this on MySQL if that error appears during `loaddata` (or
any save). Safe to re-run; does nothing on SQLite.

    python manage.py mysql_utf8mb4          # convert
    python manage.py mysql_utf8mb4 --check   # just report current charsets
"""

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Convert the MySQL database and all tables to utf8mb4.'

    def add_arguments(self, parser):
        parser.add_argument('--check', action='store_true',
                            help='Only report table charsets; make no changes.')

    def handle(self, *args, **options):
        if connection.vendor != 'mysql':
            self.stdout.write(self.style.WARNING(
                f'Database is "{connection.vendor}", not MySQL — nothing to do.'
            ))
            return

        db_name = connection.settings_dict['NAME']

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name, table_collation
                FROM information_schema.tables
                WHERE table_schema = %s AND table_type = 'BASE TABLE'
                ORDER BY table_name
                """,
                [db_name],
            )
            tables = cursor.fetchall()

            if options['check']:
                self.stdout.write(f'Database: {db_name}')
                for name, collation in tables:
                    flag = '' if (collation or '').startswith('utf8mb4') else '  <-- not utf8mb4'
                    self.stdout.write(f'  {name}: {collation}{flag}')
                return

            # Database default charset (affects new tables)
            self.stdout.write(f'Converting database {db_name} to utf8mb4…')
            cursor.execute(
                f'ALTER DATABASE `{db_name}` '
                'CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
            )

            converted = 0
            for name, collation in tables:
                if (collation or '').startswith('utf8mb4'):
                    continue
                self.stdout.write(f'  converting {name} ({collation}) …')
                cursor.execute(
                    f'ALTER TABLE `{name}` '
                    'CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
                )
                converted += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Converted {converted} table(s); {len(tables) - converted} already utf8mb4.'
        ))
