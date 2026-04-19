from django.db import models
from django.contrib.auth import get_user_model
import uuid
import re


def _parse_months(duration_str: str) -> int:
    """Extract number of months from a string like '4 Months' or '6 months'."""
    m = re.search(r'(\d+)', str(duration_str or ''))
    return int(m.group(1)) if m else 1

User = get_user_model()


class CourseCatalog(models.Model):
    """Algaddaf official course catalog with prices"""
    sn = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'course_catalog'
        ordering = ['sn']

    def __str__(self):
        return f"{self.sn}. {self.name}"


class StudentRecord(models.Model):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    MARITAL_CHOICES = [('single', 'Single'), ('married', 'Married')]
    STUDENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('it_student', 'IT Student'),
        ('nysc', 'NYSC'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # A. Personal Information
    passport_photo = models.ImageField(upload_to='student_passports/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_CHOICES)
    home_address = models.TextField()
    phone_no = models.CharField(max_length=20)
    alt_phone_no = models.CharField(max_length=20, blank=True, null=True)
    parent_phone_no = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True, null=True)

    # B. Educational Qualification
    highest_qualification = models.CharField(max_length=100, blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    year_of_graduation = models.CharField(max_length=4, blank=True, null=True)
    graduation_class = models.CharField(max_length=100, blank=True, null=True)

    # C. Course
    course = models.ForeignKey(CourseCatalog, on_delete=models.PROTECT, related_name='enrollments')
    duration_of_training = models.CharField(max_length=20, blank=True, null=True)
    student_type = models.CharField(max_length=20, choices=STUDENT_TYPE_CHOICES, default='full_time')

    # D. Fees
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # E. Official Use
    application_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    id_no = models.CharField(max_length=50, blank=True, null=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='student_records_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_records'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.course.name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Total fee = price per month × number of months
        duration_str = self.duration_of_training or (self.course.duration if self.course_id else '')
        months = _parse_months(duration_str)
        self.course_fee = self.course.price * months

        # IT/NYSC get 50% discount
        if self.student_type in ('it_student', 'nysc'):
            self.amount_to_pay = self.course_fee / 2
        else:
            self.amount_to_pay = self.course_fee
        self.balance = self.amount_to_pay - self.amount_paid
        super().save(*args, **kwargs)
