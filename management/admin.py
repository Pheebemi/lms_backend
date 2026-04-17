from django.contrib import admin
from .models import CourseCatalog, StudentRecord


@admin.register(CourseCatalog)
class CourseCatalogAdmin(admin.ModelAdmin):
    list_display = ['sn', 'name', 'duration', 'price', 'is_active']
    list_editable = ['is_active']
    ordering = ['sn']


@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'phone_no', 'course', 'student_type',
        'course_fee', 'amount_paid', 'balance', 'application_status', 'created_at',
    ]
    list_filter = ['application_status', 'student_type', 'gender', 'course']
    search_fields = ['first_name', 'last_name', 'phone_no', 'id_no', 'email']
    readonly_fields = ['id', 'amount_to_pay', 'balance', 'created_by', 'created_at', 'updated_at']
    ordering = ['-created_at']
