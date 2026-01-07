"""
Certificate Generator Utility
Creates beautiful PNG certificates using PIL/Pillow
"""
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
from datetime import datetime
import os


def generate_certificate_png(student_name, course_title, certificate_id, issued_date=None):
    """
    Generate a beautiful PNG certificate
    
    Args:
        student_name: Full name of the student
        course_title: Title of the completed course
        certificate_id: Unique certificate ID
        issued_date: Date when certificate was issued (defaults to today)
    
    Returns:
        BytesIO object containing the PNG image
    """
    # Certificate dimensions (A4 size in pixels at 300 DPI)
    width = 3508  # 11.69 inches * 300 DPI
    height = 2480  # 8.27 inches * 300 DPI
    
    # Create a new image with a gradient background
    # Start with a base color
    img = Image.new('RGB', (width, height), color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Draw decorative border
    border_width = 40
    border_color = '#1e40af'  # Blue
    
    # Outer border
    draw.rectangle(
        [(border_width, border_width), (width - border_width, height - border_width)],
        outline=border_color,
        width=8
    )
    
    # Inner decorative border
    inner_border = 60
    draw.rectangle(
        [(inner_border, inner_border), (width - inner_border, height - inner_border)],
        outline='#3b82f6',
        width=3
    )
    
    # Draw decorative corner elements
    corner_size = 150
    corner_thickness = 6
    
    # Top-left corner
    draw.line([(inner_border, inner_border), (inner_border + corner_size, inner_border)], 
              fill='#1e40af', width=corner_thickness)
    draw.line([(inner_border, inner_border), (inner_border, inner_border + corner_size)], 
              fill='#1e40af', width=corner_thickness)
    
    # Top-right corner
    draw.line([(width - inner_border, inner_border), (width - inner_border - corner_size, inner_border)], 
              fill='#1e40af', width=corner_thickness)
    draw.line([(width - inner_border, inner_border), (width - inner_border, inner_border + corner_size)], 
              fill='#1e40af', width=corner_thickness)
    
    # Bottom-left corner
    draw.line([(inner_border, height - inner_border), (inner_border + corner_size, height - inner_border)], 
              fill='#1e40af', width=corner_thickness)
    draw.line([(inner_border, height - inner_border), (inner_border, height - inner_border - corner_size)], 
              fill='#1e40af', width=corner_thickness)
    
    # Bottom-right corner
    draw.line([(width - inner_border, height - inner_border), (width - inner_border - corner_size, height - inner_border)], 
              fill='#1e40af', width=corner_thickness)
    draw.line([(width - inner_border, height - inner_border), (width - inner_border, height - inner_border - corner_size)], 
              fill='#1e40af', width=corner_thickness)
    
    # Try to load a nice font, fallback to default if not available
    # Common font paths on different systems
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/times.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ]
    
    title_font = None
    name_font = None
    body_font = None
    small_font = None
    
    # Try to load fonts
    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 120)
                name_font = ImageFont.truetype(font_path, 100)
                body_font = ImageFont.truetype(font_path, 60)
                small_font = ImageFont.truetype(font_path, 40)
                break
        except:
            continue
    
    # Fallback to default font if no font found
    if not title_font:
        default_font = ImageFont.load_default()
        # Scale default font sizes
        title_font = default_font
        name_font = default_font
        body_font = default_font
        small_font = default_font
    
    # Title text
    title = "CERTIFICATE OF COMPLETION"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = 300
    
    # Draw title with shadow effect
    shadow_offset = 3
    draw.text((title_x + shadow_offset, title_y + shadow_offset), title, 
              fill='#1e3a8a', font=title_font)
    draw.text((title_x, title_y), title, fill='#1e40af', font=title_font)
    
    # Subtitle
    subtitle = "This is to certify that"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=body_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 200
    
    draw.text((subtitle_x, subtitle_y), subtitle, fill='#4b5563', font=body_font)
    
    # Student name (highlighted)
    name_y = subtitle_y + 180
    name_bbox = draw.textbbox((0, 0), student_name, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (width - name_width) // 2
    
    # Draw name with underline
    draw.text((name_x, name_y), student_name, fill='#1e40af', font=name_font)
    underline_y = name_y + 120
    draw.line([(name_x - 20, underline_y), (name_x + name_width + 20, underline_y)], 
              fill='#1e40af', width=4)
    
    # Course completion text
    course_text = f"has successfully completed the course"
    course_bbox = draw.textbbox((0, 0), course_text, font=body_font)
    course_width = course_bbox[2] - course_bbox[0]
    course_x = (width - course_width) // 2
    course_y = name_y + 250
    
    draw.text((course_x, course_y), course_text, fill='#4b5563', font=body_font)
    
    # Course title (highlighted)
    course_title_y = course_y + 120
    course_title_bbox = draw.textbbox((0, 0), course_title, font=name_font)
    course_title_width = course_title_bbox[2] - course_title_bbox[0]
    course_title_x = (width - course_title_width) // 2
    
    # Wrap course title if too long
    if course_title_width > width - 400:
        # Split into multiple lines
        words = course_title.split()
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_bbox = draw.textbbox((0, 0), word, font=name_font)
            word_width = word_bbox[2] - word_bbox[0]
            if current_width + word_width > width - 400:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
            else:
                current_line.append(word)
                current_width += word_width + 20  # Add space width
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw multiple lines
        line_height = 120
        for i, line in enumerate(lines):
            line_bbox = draw.textbbox((0, 0), line, font=name_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (width - line_width) // 2
            line_y = course_title_y + (i * line_height)
            draw.text((line_x, line_y), line, fill='#1e40af', font=name_font)
    else:
        draw.text((course_title_x, course_title_y), course_title, fill='#1e40af', font=name_font)
    
    # Date
    if issued_date:
        date_str = issued_date.strftime("%B %d, %Y")
    else:
        date_str = datetime.now().strftime("%B %d, %Y")
    
    date_text = f"Issued on {date_str}"
    date_bbox = draw.textbbox((0, 0), date_text, font=small_font)
    date_width = date_bbox[2] - date_bbox[0]
    date_x = (width - date_width) // 2
    date_y = height - 400
    
    draw.text((date_x, date_y), date_text, fill='#6b7280', font=small_font)
    
    # Certificate ID
    cert_id_text = f"Certificate ID: {certificate_id}"
    cert_id_bbox = draw.textbbox((0, 0), cert_id_text, font=small_font)
    cert_id_width = cert_id_bbox[2] - cert_id_bbox[0]
    cert_id_x = (width - cert_id_width) // 2
    cert_id_y = date_y + 60
    
    draw.text((cert_id_x, cert_id_y), cert_id_text, fill='#9ca3af', font=small_font)
    
    # Organization name at bottom
    org_text = "ALGADDAF Technology Hub"
    org_bbox = draw.textbbox((0, 0), org_text, font=body_font)
    org_width = org_bbox[2] - org_bbox[0]
    org_x = (width - org_width) // 2
    org_y = height - 250
    
    draw.text((org_x, org_y), org_text, fill='#1e40af', font=body_font)
    
    # Save to BytesIO
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG', quality=95, dpi=(300, 300))
    img_buffer.seek(0)
    
    return img_buffer


def save_certificate_image(certificate, student_name, course_title, certificate_id, issued_date=None):
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
        issued_date=issued_date
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

