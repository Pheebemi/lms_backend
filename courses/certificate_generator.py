"""
Certificate Generator Utility
Creates beautiful PNG certificates using PIL/Pillow
"""
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
from datetime import datetime
import os


# Centre coordinates (x, y) of each grade checkbox on the template (2000×1414)
GRADE_BOX_CENTERS = {
    'pass': (547, 962),
    'lower_credit': (990, 962),
    'upper_credit': (1412, 962),
    'distinction': (1875, 962),
}


def generate_certificate_png(student_name, course_title, certificate_id, issued_date=None, completed_date=None, render_course_title=False, grade=None):
    """
    Generate a PNG certificate using your custom design

    Args:
        student_name: Full name of the student
        course_title: Title of the completed course
        certificate_id: Unique certificate ID
        issued_date: Date when certificate was issued (defaults to today)
        render_course_title: Deprecated — the template already names the course,
            so the course title is not drawn.
        grade: One of 'pass', 'lower_credit', 'upper_credit', 'distinction'.
            When set, an X is placed in the matching checkbox.

    Returns:
        BytesIO object containing the PNG image
    """
    # Load your custom certificate design
    template_path = "media/certificates/certificate_template.png"  # Change this to your template filename

    try:
        # Open your template image
        img = Image.open(template_path).convert('RGB')
        width, height = img.size
    except FileNotFoundError:
        # Fallback: create a blank certificate if template not found
        width = 3508
        height = 2480
        img = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(img)

    # Load fonts for text overlay (customize for your template)
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/times.ttf",
    ]

    # Load fonts with sizes appropriate for your template
    student_name_font = None
    course_name_font = None
    certificate_id_font = None
    date_font = None
    grade_font = None

    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                student_name_font = ImageFont.truetype(font_path, 85)   # Recipient name
                course_name_font = ImageFont.truetype(font_path, 68)     # Course name
                certificate_id_font = ImageFont.truetype(font_path, 38)  # Certificate ID
                date_font = ImageFont.truetype(font_path, 40)            # Graduation date
                grade_font = ImageFont.truetype(font_path, 60)           # Grade checkbox mark
                break
        except:
            continue

    # Fallback fonts
    if not student_name_font:
        default_font = ImageFont.load_default()
        student_name_font = default_font
        course_name_font = default_font
        certificate_id_font = default_font
        date_font = default_font
        grade_font = default_font

    # ── Text overlays (coordinates match certificate_template.png, 2000×1414) ──

    # Certificate ID — placed just after the printed "CERT ID:" label
    draw.text((430, 438), certificate_id,
              fill='#000000', font=certificate_id_font, anchor='lm')  # Left-middle anchor

    # Recipient name — centred on the line under "This certificate is presented to:"
    draw.text((1000, 655), student_name.upper(),
              fill='#000000', font=student_name_font, anchor='mm')  # Center anchor

    # Course name — centred on the second line ("...has been awarded a ___")
    if course_title:
        draw.text((1000, 805), course_title,
                  fill='#000000', font=course_name_font, anchor='mm')  # Center anchor

    # Grade — X in the matching checkbox (Pass / Lower Credit / Upper Credit / Distinction)
    if grade and grade in GRADE_BOX_CENTERS:
        draw.text(GRADE_BOX_CENTERS[grade], 'X',
                  fill='#000000', font=grade_font, anchor='mm')

    # Graduation date — on the line above the "Graduation Date" label
    if completed_date:
        completion_text = completed_date.strftime('%d %B, %Y').upper()
        draw.text((810, 1165), completion_text,
                  fill='#000000', font=date_font, anchor='mm')

    # Save to BytesIO
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG', quality=95, dpi=(300, 300))
    img_buffer.seek(0)
    
    return img_buffer


def save_certificate_image(certificate, student_name, course_title, certificate_id, issued_date=None, completed_date=None):
    """
    Generate and save certificate PNG to the certificate model
    
    Args:
        certificate: Certificate model instance
        student_name: Full name of the student
        course_title: Title of the course
        certificate_id: Unique certificate ID
        issued_date: Date when certificate was issued
    
    Returns:
        The certificate instance with image_file saved
    """
    # Generate the PNG
    img_buffer = generate_certificate_png(
        student_name=student_name,
        course_title=course_title,
        certificate_id=certificate_id,
        issued_date=issued_date,
        completed_date=completed_date
    )
    
    # Create filename
    filename = f"certificate_{certificate_id}_{certificate.student.id}.png"
    
    # Save to the certificate model
    certificate.image_file.save(
        filename,
        ContentFile(img_buffer.read()),
        save=True
    )
    
    return certificate

