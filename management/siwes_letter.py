"""
SIWES acceptance letter rendering.

Draws the letter onto the company letterhead and returns a PDF. Everything
except the handful of values passed in is fixed here, so a generated letter is
identical to the one before it apart from the student's details.

Kept separate from courses/certificate_generator.py on purpose: that module
composites text at fixed pixel coordinates and cannot lay out a wrapped,
justified paragraph, which is what the body of this letter is.
"""
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image as PILImage

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas as pdfcanvas

ASSETS = Path(__file__).resolve().parent / 'letter_assets'
LETTERHEAD = ASSETS / 'letterhead.png'
SIGNATURE_STAMP = ASSETS / 'signature_stamp.png'

# The sample letter is set in Cambria, a Microsoft font that is not on the
# server. Liberation Serif is the closest serif available; the fallbacks keep
# rendering sane on a box that has neither.
_FONT_CANDIDATES = [
    ('LiberationSerif', 'LiberationSerif-Bold',
     '/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',
     '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'),
    ('DejaVuSerif', 'DejaVuSerif-Bold',
     '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
     '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'),
]

MONTH_NAMES = [
    'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
    'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER',
]

SIGNATORY_NAME = 'JABIR AHMAD BELLO'
SIGNATORY_ORG = 'ALGADDAF TECHNOLOGY HUB.'

MARGIN = inch
BODY_SIZE = 14
LEADING = 20

# The letterhead footer band occupies roughly the last inch of the page. The
# signatory block is pinned above it; the stamp sits directly on top of that.
SIGNATURE_BLOCK_TOP = 1.95 * inch
STAMP_MAX_HEIGHT = 1.15 * inch


def _register_fonts():
    """
    Register a serif pair and return (regular, bold) font names.

    Falls back to the built-in Times, which is always present, so a missing
    system font degrades the look rather than breaking generation.
    """
    for regular, bold, regular_path, bold_path in _FONT_CANDIDATES:
        if Path(regular_path).exists() and Path(bold_path).exists():
            if regular not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(regular, regular_path))
                pdfmetrics.registerFont(TTFont(bold, bold_path))
                # Without the family mapping, <b> in a Paragraph silently
                # renders at regular weight.
                pdfmetrics.registerFontFamily(regular, normal=regular, bold=bold,
                                              italic=regular, boldItalic=bold)
            return regular, bold
    return 'Times-Roman', 'Times-Bold'


def _ordinal(day: int) -> str:
    """1 -> 1ST, 2 -> 2ND, 3 -> 3RD, 4 -> 4TH, 11..13 -> TH."""
    if 11 <= day % 100 <= 13:
        suffix = 'TH'
    else:
        suffix = {1: 'ST', 2: 'ND', 3: 'RD'}.get(day % 10, 'TH')
    return f'{day}{suffix}'


def _end_month_year(start_month: int, start_year: int, duration_months: int):
    """Inclusive of the start month: 3 months from October ends in December."""
    zero_based = (start_month - 1) + (duration_months - 1)
    return (zero_based % 12) + 1, start_year + zero_based // 12


def generate_siwes_letter_pdf(*, student_name, course_of_study, registration_no,
                              institution, institution_state, duration_months,
                              start_month, start_year, letter_date) -> BytesIO:
    """
    Render one acceptance letter and return it as a PDF in a BytesIO,
    positioned at the start and ready to stream.
    """
    regular, bold = _register_fonts()
    page_w, page_h = A4
    text_w = page_w - 2 * MARGIN

    buf = BytesIO()
    c = pdfcanvas.Canvas(buf, pagesize=A4)

    # Letterhead first, full bleed, so everything else sits on top of it.
    # Header, RC number and footer all come from these pixels rather than
    # being redrawn, so they cannot drift.
    if LETTERHEAD.exists():
        c.drawImage(str(LETTERHEAD), 0, 0, width=page_w, height=page_h,
                    preserveAspectRatio=False, mask='auto')

    base = ParagraphStyle('base', fontName=regular, fontSize=BODY_SIZE, leading=LEADING)
    right = ParagraphStyle('right', parent=base, alignment=TA_RIGHT)
    centre = ParagraphStyle('centre', parent=base, alignment=TA_CENTER, fontName=bold)
    body = ParagraphStyle('body', parent=base, alignment=TA_JUSTIFY)

    def draw(paragraph_style, html, y, width=text_w, x=MARGIN):
        """Draw one paragraph and return the y just below it."""
        p = Paragraph(html, paragraph_style)
        _, h = p.wrap(width, page_h)
        p.drawOn(c, x, y - h)
        return y - h

    # Values are uppercased to match the sample, and escaped because they are
    # interpolated into reportlab's mini-markup — a name containing '&' would
    # otherwise corrupt the paragraph.
    name = escape(str(student_name).upper())
    course = escape(str(course_of_study).upper())
    reg_no = escape(str(registration_no).upper())
    inst = escape(str(institution))
    state = escape(str(institution_state))

    end_month, end_year = _end_month_year(start_month, start_year, duration_months)
    start_txt = f'{MONTH_NAMES[start_month - 1]}, {start_year}'
    end_txt = f'{MONTH_NAMES[end_month - 1]} {end_year}'
    months_txt = f'{duration_months} Month' + ('s' if duration_months != 1 else '')

    # Start below the letterhead's header block.
    y = page_h - 3.15 * inch

    y = draw(right, f'{_ordinal(letter_date.day)} {MONTH_NAMES[letter_date.month - 1]}, '
                    f'{letter_date.year}', y)
    y -= 0.35 * inch

    y = draw(base, 'The SIWES Coordinator,', y)
    y = draw(base, f'{inst},', y)
    y = draw(base, f'{state}.', y)
    y -= 0.28 * inch

    y = draw(base, 'Sir,', y)
    y -= 0.28 * inch

    y = draw(centre, 'SIWES ACCEPTANCE', y)
    y -= 0.28 * inch

    y = draw(body,
             f'I wish to inform you that we accepted your student bearing <b>{name}</b> '
             f'studying <b>{course}</b> with Registration No. <b>{reg_no}</b> To undergo '
             f'his/her SIWES Program under our organization for the period of '
             f'<b>{months_txt}</b> from <b>{start_txt}</b> to <b>{end_txt}</b>.', y)
    y -= 0.3 * inch

    y = draw(base, 'Thank you for your esteem regard.', y)
    y -= 0.28 * inch
    y = draw(base, 'Yours Faithfully,', y)

    # The signature block is pinned a fixed distance above the bottom rather
    # than flowing after the body. The letterhead footer occupies the last inch
    # of the page, and flowed positioning would push the signatory into it as
    # soon as a long institution name added a line to the body.
    sig_top = SIGNATURE_BLOCK_TOP
    if SIGNATURE_STAMP.exists():
        # Size the stamp to the gap actually left between the closing line and
        # the signatory block, capped so it stays a sensible size on a short
        # letter. Derived rather than fixed so a body that runs long shrinks the
        # stamp instead of overprinting the text on either side of it.
        available = y - (sig_top + 0.08 * inch)
        stamp_h = max(min(STAMP_MAX_HEIGHT, available), 0)
        if stamp_h > 0.4 * inch:
            # Aspect comes from the asset itself; the image is trimmed to the
            # stamp, so the box maps to what is actually inked.
            with PILImage.open(SIGNATURE_STAMP) as im:
                src_w, src_h = im.size
            stamp_w = stamp_h * src_w / src_h
            c.drawImage(str(SIGNATURE_STAMP), MARGIN - 0.15 * inch,
                        sig_top + 0.08 * inch, width=stamp_w, height=stamp_h,
                        preserveAspectRatio=True, mask='auto')

    sig_y = draw(base, SIGNATORY_NAME, sig_top)
    draw(base, SIGNATORY_ORG, sig_y)

    c.showPage()
    c.save()
    buf.seek(0)
    return buf
