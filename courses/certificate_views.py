"""
Certificate images.

Student course-completion certificates are not stored as files: the PNG is
drawn from the database record each time it is asked for, so certificates
cost no disk space. `certificate_image_url()` hands out a short-lived signed
link to `render_certificate_image()`; the link is signed (rather than
requiring a login) because it is used as an <img src> and in a plain fetch(),
neither of which can send the API's Authorization header.

`serve_certificate_image()` below only serves files written before this
change; run `manage.py purge_certificate_images` to delete them.
"""
from django.core import signing
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

CERTIFICATE_IMAGE_SALT = 'certificate-image'
# The frontend asks for a fresh link every time it loads a certificate, so an
# hour is generous; a leaked link stops working on its own.
CERTIFICATE_IMAGE_MAX_AGE = 60 * 60


def certificate_image_url(certificate, request=None):
    """Signed, expiring URL that renders this certificate's PNG on demand."""
    token = signing.dumps(certificate.pk, salt=CERTIFICATE_IMAGE_SALT)
    path = reverse('courses:certificate-image-render', args=[token])
    if request is not None:
        return request.build_absolute_uri(path)
    return f"{settings.BASE_URL.rstrip('/')}{path}"


@require_GET
def render_certificate_image(request, token):
    """Draw a certificate PNG from its database record. Nothing is written to disk."""
    try:
        certificate_pk = signing.loads(
            token, salt=CERTIFICATE_IMAGE_SALT, max_age=CERTIFICATE_IMAGE_MAX_AGE
        )
    except signing.BadSignature:  # includes SignatureExpired
        raise Http404("Invalid or expired certificate link")

    from .models import Certificate
    from .certificate_generator import generate_certificate_png

    certificate = get_object_or_404(
        Certificate.objects.select_related('student', 'course', 'enrollment'),
        pk=certificate_pk,
    )

    img_buffer = generate_certificate_png(
        student_name=f"{certificate.student.first_name} {certificate.student.last_name}",
        course_title=certificate.course.title,
        certificate_id=certificate.certificate_id,
        issued_date=certificate.issued_at,
        completed_date=certificate.enrollment.completed_at,
    )

    response = HttpResponse(img_buffer.read(), content_type='image/png')
    response['Content-Disposition'] = f'inline; filename="certificate_{certificate.certificate_id}.png"'
    # Never cached: a cached copy (which might lack CORS headers if it was first
    # loaded by an <img>) could break the later fetch() used for downloading.
    response['Cache-Control'] = 'private, no-store'
    return response


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
@cache_control(max_age=3600, public=True)
def serve_certificate_image(request, path):
    """
    Serve certificate PNG images with proper Content-Type headers
    """
    # Handle OPTIONS request for CORS
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, 'certificates', path)
    
    # Normalize paths for security check
    media_root = os.path.abspath(settings.MEDIA_ROOT)
    file_path_abs = os.path.abspath(file_path)
    
    # Security check: ensure the file is within MEDIA_ROOT/certificates
    certificates_dir = os.path.join(media_root, 'certificates')
    if not file_path_abs.startswith(os.path.abspath(certificates_dir)):
        raise Http404("Invalid file path")
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise Http404("Certificate image not found")
    
    # Read the file
    try:
        with open(file_path, 'rb') as f:
            image_data = f.read()
    except IOError:
        raise Http404("Error reading certificate image")
    
    # Determine content type based on file extension
    content_type = 'image/png'  # Default to PNG
    if file_path.lower().endswith('.png'):
        content_type = 'image/png'
    elif file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
        content_type = 'image/jpeg'
    elif file_path.lower().endswith('.gif'):
        content_type = 'image/gif'
    elif file_path.lower().endswith('.webp'):
        content_type = 'image/webp'
    
    # Create response with proper headers
    response = HttpResponse(image_data, content_type=content_type)
    response['Content-Length'] = str(len(image_data))
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    response['Cache-Control'] = 'public, max-age=3600'
    response['Access-Control-Allow-Origin'] = '*'  # Allow CORS for images
    response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    
    return response

