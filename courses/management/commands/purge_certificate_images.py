from django.core.management.base import BaseCommand

from courses.models import Certificate


class Command(BaseCommand):
    help = (
        "Delete the certificate image files stored before certificates were "
        "rendered on demand, and clear their reference in the database. "
        "Safe: certificates are redrawn from their records whenever they are "
        "viewed or downloaded. Use --dry-run first to see what would go."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report what would be deleted without deleting anything.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        stored = Certificate.objects.filter(image_file__isnull=False).exclude(image_file='')

        files = 0
        already_missing = 0
        bytes_freed = 0

        for certificate in stored.iterator():
            try:
                bytes_freed += certificate.image_file.size
            except (FileNotFoundError, OSError, ValueError):
                already_missing += 1
            files += 1

            if not dry_run:
                # Removes the file from storage (a file that is already gone is ignored)
                certificate.image_file.delete(save=False)
                certificate.save(update_fields=['image_file'])

        verb = 'Would delete' if dry_run else 'Deleted'
        self.stdout.write(
            f"{verb} {files} certificate image file(s), "
            f"{bytes_freed / (1024 * 1024):.1f} MB"
            + (f" ({already_missing} already missing from disk)" if already_missing else "")
        )
        if dry_run:
            self.stdout.write("Dry run: nothing was changed.")
