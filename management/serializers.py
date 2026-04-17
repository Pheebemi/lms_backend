from rest_framework import serializers
from .models import CourseCatalog, StudentRecord


class CourseCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCatalog
        fields = ['id', 'sn', 'name', 'duration', 'price', 'is_active']


class StudentRecordSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_sn = serializers.IntegerField(source='course.sn', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = StudentRecord
        fields = [
            'id',
            # Personal
            'passport_photo',
            'first_name',
            'last_name',
            'full_name',
            'gender',
            'marital_status',
            'home_address',
            'phone_no',
            'alt_phone_no',
            'parent_phone_no',
            'date_of_birth',
            'email',
            # Educational
            'highest_qualification',
            'school_name',
            'year_of_graduation',
            'graduation_class',
            # Course
            'course',
            'course_name',
            'course_sn',
            'duration_of_training',
            'student_type',
            # Fees (read-only — calculated in save())
            'course_fee',
            'amount_to_pay',
            'amount_paid',
            'balance',
            # Official
            'application_status',
            'id_no',
            # Meta
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'amount_to_pay', 'balance', 'created_by', 'created_at', 'updated_at']

    def validate_passport_photo(self, value):
        if value and value.size > 100 * 1024:  # 100 KB
            raise serializers.ValidationError("Passport photo must be 100 KB or smaller.")
        return value


class StudentRecordListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    course_name = serializers.CharField(source='course.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = StudentRecord
        fields = [
            'id',
            'passport_photo',
            'first_name',
            'last_name',
            'full_name',
            'phone_no',
            'course_name',
            'student_type',
            'course_fee',
            'amount_to_pay',
            'amount_paid',
            'balance',
            'application_status',
            'id_no',
            'created_by_name',
            'created_at',
        ]
