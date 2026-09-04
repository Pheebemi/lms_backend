from rest_framework import serializers
from .models import CourseCatalog, StudentRecord, ManualCertificate, SiwesLetter


class CourseCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCatalog
        fields = ['id', 'sn', 'name', 'duration', 'price', 'is_active']


class ManualCertificateSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model = ManualCertificate
        fields = [
            'id', 'recipient_name', 'course', 'course_name',
            'grade', 'grade_display', 'certificate_id', 'issued_at', 'created_by_name',
        ]
        read_only_fields = ['id', 'certificate_id', 'issued_at', 'created_by_name']
        # Drop the auto unique-together validator: the generate view intentionally
        # reuses an existing (recipient, course) certificate so its ID stays stable.
        validators = []

    def validate_recipient_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Recipient name is required.")
        return value


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
        # course_fee, amount_to_pay and balance are all derived in Model.save()
        read_only_fields = ['id', 'course_fee', 'amount_to_pay', 'balance', 'created_by', 'created_at', 'updated_at']

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


class SiwesLetterSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    start_month_display = serializers.CharField(source='get_start_month_display', read_only=True)
    end_month = serializers.SerializerMethodField()
    end_year = serializers.SerializerMethodField()

    class Meta:
        model = SiwesLetter
        fields = [
            'id', 'student_name', 'course_of_study', 'registration_no',
            'institution', 'institution_state', 'duration_months',
            'start_month', 'start_month_display', 'start_year',
            'end_month', 'end_year', 'letter_date',
            'reference_id', 'issued_at', 'created_by_name',
        ]
        read_only_fields = ['id', 'reference_id', 'issued_at', 'created_by_name']

    def get_end_month(self, obj):
        return obj.end_month_year[0]

    def get_end_year(self, obj):
        return obj.end_month_year[1]

    def validate_duration_months(self, value):
        if not 1 <= value <= 12:
            raise serializers.ValidationError("Duration must be between 1 and 12 months.")
        return value

    def validate_start_year(self, value):
        if not 2000 <= value <= 2100:
            raise serializers.ValidationError("Enter a valid year.")
        return value

    def validate(self, attrs):
        # Trim the free-text fields; a trailing space reaches the printed letter.
        for field in ('student_name', 'course_of_study', 'registration_no',
                      'institution', 'institution_state'):
            if field in attrs:
                attrs[field] = attrs[field].strip()
                if not attrs[field]:
                    raise serializers.ValidationError({field: "This field is required."})
        return attrs
