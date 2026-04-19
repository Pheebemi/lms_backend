"""
Usage:
    python manage.py seed_courses
    python manage.py seed_courses --clear   # wipe existing catalog first
"""
from django.core.management.base import BaseCommand
from management.models import CourseCatalog

# Exact courses from the Algaddaff Technology Hub Application Form
# Price is PER MONTH — total fee = price × duration months
COURSES = [
    # (sn, name, duration, price_per_month)
    (1,  "Certificate in Computer Appreciation",          "3 Months",  20000),
    (2,  "Diploma in Computer Appreciation",              "6 Months",  15000),
    (3,  "Certificate in Web Design and Development",     "4 Months",  40000),
    (4,  "Diploma in Web Design and Development",         "6 Months",  30000),
    (5,  "Certificate in Graphics and Animation",         "3 Months",  20000),
    (6,  "Diploma in Graphics and Animation",             "6 Months",  30000),
    (7,  "Certificate in Digital Marketing",              "3 Months",  20000),
    (8,  "Diploma in Digital Marketing",                  "6 Months",  30000),
    (9,  "Certificate in Software Programming",           "4 Months",  40000),
    (10, "Diploma in Software Programming",               "6 Months",  30000),
    (11, "Certificate in Hardware Maintenance",           "4 Months",  40000),
    (12, "Diploma in Hardware Maintenance",               "6 Months",  30000),
    (13, "Certificate in Networking Engineering",         "4 Months",  40000),
    (14, "Diploma in Networking Engineering",             "6 Months",  30000),
    (15, "Certificate in Cyber Security",                 "4 Months",  40000),
    (16, "Diploma in Cyber Security",                     "6 Months",  30000),
    (17, "Certificate in Data Science and Machine Learning", "4 Months", 40000),
    (18, "Diploma in Data Science and Machine Learning",  "6 Months",  30000),
    (19, "Certificate in Artificial Intelligence",        "2 Months",  25000),
    (20, "Diploma in Artificial Intelligence",            "4 Months",  20000),
    (21, "Certificate in Crypto Currency",                "2 Months",  25000),
    (22, "Diploma in Crypto Currency",                    "4 Months",  20000),
    (23, "Agribusiness Training",                         "3 Months",  50000),
    (24, "Solar Installations Training",                  "3 Months",  50000),
    (25, "CCTV Camera Training",                          "3 Months",  50000),
]


class Command(BaseCommand):
    help = "Seed CourseCatalog with exact Algaddaff courses. Prices are per month."

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true',
                            help='Delete all existing catalog entries before seeding.')

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = CourseCatalog.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Cleared {deleted} existing course(s)."))

        created_count = 0
        updated_count = 0

        for sn, name, duration, price in COURSES:
            obj, created = CourseCatalog.objects.update_or_create(
                sn=sn,
                defaults={
                    'name': name,
                    'duration': duration,
                    'price': price,
                    'is_active': True,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
            self.stdout.write(
                f"  {'✓ Created' if created else '↻ Updated'}: {sn}. {name} — {duration} — ₦{price:,}/month"
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {created_count} created, {updated_count} updated."
        ))
        self.stdout.write(self.style.WARNING(
            "NOTE: Courses 6–8 (Diploma in Graphics, Digital Marketing cert/diploma) "
            "were not visible in the form photos — please verify and correct if needed."
        ))
