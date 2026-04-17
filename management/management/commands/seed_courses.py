"""
Usage:
    python manage.py seed_courses
    python manage.py seed_courses --clear   # wipe existing catalog first
"""
from django.core.management.base import BaseCommand
from management.models import CourseCatalog

COURSES = [
    # (sn, name, duration, price)
    (1,  "Computer Appreciation",              "2 months",  15000),
    (2,  "Microsoft Office Suite",             "2 months",  20000),
    (3,  "Desktop Publishing (DTP)",           "2 months",  20000),
    (4,  "Web Design",                         "3 months",  30000),
    (5,  "Graphic Design",                     "3 months",  30000),
    (6,  "Video Editing",                      "3 months",  30000),
    (7,  "Digital Marketing",                  "3 months",  30000),
    (8,  "Mobile Phone Repairs",               "3 months",  35000),
    (9,  "Laptop / Computer Repairs",          "3 months",  35000),
    (10, "CCTV Installation",                  "2 months",  25000),
    (11, "Solar Panel Installation",           "3 months",  40000),
    (12, "Inverter / UPS Maintenance",         "2 months",  25000),
    (13, "Electrical Wiring",                  "3 months",  35000),
    (14, "Data Analysis (Excel / Power BI)",   "3 months",  35000),
    (15, "Programming (Python)",               "4 months",  50000),
    (16, "Programming (JavaScript)",           "4 months",  50000),
    (17, "Cybersecurity Fundamentals",         "4 months",  50000),
    (18, "Networking & IT Support",            "3 months",  40000),
    (19, "Accounting Software (Sage / QuickBooks)", "2 months", 25000),
    (20, "Fashion Design & Tailoring",         "6 months",  45000),
    (21, "Catering & Food Processing",         "3 months",  30000),
    (22, "Photography",                        "2 months",  25000),
    (23, "Interior Decoration",                "3 months",  35000),
    (24, "Autocad / Technical Drawing",        "3 months",  40000),
    (25, "Project Management (PMP Prep)",      "3 months",  60000),
]


class Command(BaseCommand):
    help = "Seed the CourseCatalog with Algaddaff official courses and prices."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing catalog entries before seeding.',
        )

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
            self.style.SUCCESS(
                f"Done. {created_count} course(s) created, {updated_count} updated."
            )
        )
