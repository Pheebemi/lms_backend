import html as _html
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Category, Course, Lesson, Quiz, QuizQuestion

User = get_user_model()


def to_html_content(raw: str) -> str:
    """Convert plain-text lesson content to safe Quill/TipTap HTML."""
    lines = raw.strip().splitlines()
    parts: list[str] = []
    buffer: list[str] = []

    def flush_buffer():
        if buffer:
            escaped = _html.escape("\n".join(buffer))
            parts.append(f'<pre><code>{escaped}</code></pre>')
            buffer.clear()

    if lines and lines[0].startswith("Welcome to Lesson"):
        parts.append(f'<h2>{_html.escape(lines[0])}</h2>')
        lines = lines[1:]

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("───") or stripped.startswith("---"):
            flush_buffer()
            title = stripped.replace("─", "").replace("-", "").strip()
            if title:
                parts.append(f'<h3>{_html.escape(title)}</h3>')
        else:
            buffer.append(line)

    flush_buffer()
    return "\n".join(parts)

LESSONS = [
    {
        "order": 1,
        "title": "CSS Basics — Syntax, Selectors & Specificity",
        "description": "Learn what CSS is, how to link it to HTML, understand the rule syntax, and master selectors: element, class, id, attribute, pseudo-class, pseudo-element, and specificity.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 1: CSS Basics — Syntax, Selectors & Specificity

CSS (Cascading Style Sheets) controls the visual presentation of HTML documents.

─── WHAT IS CSS? ──────────────────────────────────────────────────────────────
CSS separates content (HTML) from presentation (styles).
A CSS rule has two parts:
    selector { property: value; }

Example:
    h1 { color: red; font-size: 2rem; }

─── THREE WAYS TO ADD CSS ─────────────────────────────────────────────────────
1. External stylesheet (best practice):
       <link rel="stylesheet" href="styles.css">

2. Internal <style> block inside <head>:
       <style> p { color: blue; } </style>

3. Inline style attribute (lowest maintainability):
       <p style="color: blue;">Text</p>

─── SELECTORS ─────────────────────────────────────────────────────────────────
    *           — universal selector (all elements)
    p           — element / type selector
    .box        — class selector
    #header     — id selector
    p, h1       — group selector (comma)
    div p       — descendant combinator (p inside div)
    div > p     — child combinator (direct child only)
    h1 + p      — adjacent sibling (immediately after h1)
    h1 ~ p      — general sibling (all p after h1)

─── ATTRIBUTE SELECTORS ───────────────────────────────────────────────────────
    [href]           — has the href attribute
    [type="text"]    — attribute equals value
    [class~="nav"]   — attribute contains word
    [href^="https"]  — attribute starts with
    [href$=".pdf"]   — attribute ends with
    [href*="google"] — attribute contains substring

─── PSEUDO-CLASSES ────────────────────────────────────────────────────────────
    :hover        — mouse over the element
    :focus        — element has keyboard/input focus
    :active       — element being clicked
    :visited      — visited link
    :first-child  — first child of its parent
    :last-child   — last child of its parent
    :nth-child(n) — nth child (n can be number, odd, even, formula)
    :not(selector)— elements that do NOT match

─── PSEUDO-ELEMENTS ───────────────────────────────────────────────────────────
    ::before      — insert content before element
    ::after       — insert content after element
    ::first-line  — first line of text
    ::first-letter— first letter of text
    ::placeholder — placeholder text in inputs
    ::selection   — text selected by the user

─── SPECIFICITY (highest to lowest) ──────────────────────────────────────────
    Inline styles          1-0-0-0
    ID selectors           0-1-0-0
    Class / pseudo-class / attribute  0-0-1-0
    Element / pseudo-element  0-0-0-1
    Universal *            0-0-0-0

When two rules conflict, higher specificity wins.
Equal specificity → last rule in the file wins (cascade).
!important overrides all (use sparingly).

─── CSS COMMENTS ──────────────────────────────────────────────────────────────
    /* This is a CSS comment */
""",
        "quiz_title": "Quiz 1 — CSS Basics, Selectors & Specificity",
        "quiz_description": "20 questions on CSS syntax, selectors, combinators, pseudo-classes, pseudo-elements, and specificity.",
        "time_limit": 20,
        "questions": [
            {"q": "What does CSS stand for?", "o": ["Creative Style Sheets", "Cascading Style Sheets", "Computer Style Sheets", "Colorful Style Sheets"], "a": "Cascading Style Sheets"},
            {"q": "Which HTML tag links an external CSS stylesheet?", "o": ["<style>", "<css>", "<script>", "<link>"], "a": "<link>"},
            {"q": "What is the correct CSS syntax for a rule?", "o": ["selector: {property = value}", "selector { property: value; }", "selector | property | value", "selector -> property: value"], "a": "selector { property: value; }"},
            {"q": "Which selector targets ALL elements on the page?", "o": ["all", "every", "body", "*"], "a": "*"},
            {"q": "Which selector targets elements by their class attribute?", "o": ["#classname", "classname", ".classname", "*classname"], "a": ".classname"},
            {"q": "Which selector targets a single unique element by its id?", "o": [".id", "*id", "id", "#id"], "a": "#id"},
            {"q": "Which combinator selects DIRECT children only?", "o": ["div p (space)", "div + p", "div ~ p", "div > p"], "a": "div > p"},
            {"q": "Which combinator selects ALL descendants (not just direct children)?", "o": ["div > p", "div + p", "div ~ p", "div p (space)"], "a": "div p (space)"},
            {"q": "Which combinator selects the immediately following sibling?", "o": ["div ~ p", "div > p", "div p", "div + p"], "a": "div + p"},
            {"q": "Which pseudo-class applies when a user hovers over an element?", "o": [":active", ":focus", ":visited", ":hover"], "a": ":hover"},
            {"q": "Which pseudo-class targets the first child of its parent?", "o": [":first-element", ":first-type", ":nth-child(0)", ":first-child"], "a": ":first-child"},
            {"q": "Which pseudo-element inserts content BEFORE an element?", "o": ["::after", "::first-line", "::prepend", "::before"], "a": "::before"},
            {"q": "Which pseudo-element inserts content AFTER an element?", "o": ["::before", "::append", "::last", "::after"], "a": "::after"},
            {"q": "Which has the highest specificity?", "o": ["Element selector", "Class selector", "ID selector", "Inline style"], "a": "Inline style"},
            {"q": "When two CSS rules have equal specificity, which one wins?", "o": ["The first rule in the file", "The rule with more properties", "The shorter rule", "The last rule in the file"], "a": "The last rule in the file"},
            {"q": "What does !important do in CSS?", "o": ["Marks a comment as important", "Overrides all other declarations regardless of specificity", "Makes the browser load the style first", "Applies style only to the first element"], "a": "Overrides all other declarations regardless of specificity"},
            {"q": "Which attribute selector matches elements whose href starts with 'https'?", "o": ["[href='https']", "[href$='https']", "[href*='https']", "[href^='https']"], "a": "[href^='https']"},
            {"q": "Which pseudo-class targets elements that do NOT match a given selector?", "o": [":exclude()", ":without()", ":none()", ":not()"], "a": ":not()"},
            {"q": "What is the correct syntax for a CSS comment?", "o": ["// comment", "<!-- comment -->", "## comment", "/* comment */"], "a": "/* comment */"},
            {"q": "Which pseudo-class targets every even-numbered child element?", "o": [":nth-child(2)", ":even-child", ":nth-child(even)", ":second-child"], "a": ":nth-child(even)"},
        ],
    },
    {
        "order": 2,
        "title": "Colors, Backgrounds & Gradients",
        "description": "Master CSS color formats (named, hex, rgb, hsl, rgba, hsla), background properties, linear and radial gradients, and background shorthand.",
        "duration_minutes": 30,
        "content": """Welcome to Lesson 2: Colors, Backgrounds & Gradients

CSS provides multiple ways to specify color and rich background options.

─── COLOR FORMATS ─────────────────────────────────────────────────────────────
    Named:   color: red;  color: cornflowerblue;
    Hex:     color: #FF5733;  (shorthand: #F53)
    RGB:     color: rgb(255, 87, 51);
    RGBA:    color: rgba(255, 87, 51, 0.8);   (last value = opacity 0–1)
    HSL:     color: hsl(11, 100%, 60%);       (hue, saturation, lightness)
    HSLA:    color: hsla(11, 100%, 60%, 0.8);

─── TEXT COLOR vs BACKGROUND COLOR ───────────────────────────────────────────
    color:             sets the text (foreground) color
    background-color:  sets the background color of the element

─── BACKGROUND PROPERTIES ─────────────────────────────────────────────────────
    background-color:     #fff
    background-image:     url('bg.jpg')
    background-repeat:    repeat | no-repeat | repeat-x | repeat-y
    background-position:  center center | top left | 50% 50%
    background-size:      auto | cover | contain | 200px 100px
    background-attachment: scroll | fixed | local
    background-origin:    border-box | padding-box | content-box
    background-clip:      border-box | padding-box | content-box | text

─── BACKGROUND SHORTHAND ──────────────────────────────────────────────────────
    background: #fff url('bg.jpg') no-repeat center center / cover;
    Order: color image repeat position / size

─── MULTIPLE BACKGROUNDS ──────────────────────────────────────────────────────
    background:
        url('top.png') no-repeat top center,
        url('bottom.png') no-repeat bottom center,
        #f0f0f0;
    First listed = top layer.

─── LINEAR GRADIENT ───────────────────────────────────────────────────────────
    background: linear-gradient(direction, color-stop1, color-stop2, ...);

    background: linear-gradient(to right, #ff6b6b, #feca57);
    background: linear-gradient(135deg, blue, green 40%, yellow);

Direction keywords: to right | to left | to bottom | to top
                    to bottom right | 45deg | 180deg

─── RADIAL GRADIENT ───────────────────────────────────────────────────────────
    background: radial-gradient(shape size at position, color1, color2);
    background: radial-gradient(circle at center, #ff6b6b, #feca57);

─── CONIC GRADIENT ────────────────────────────────────────────────────────────
    background: conic-gradient(from 0deg, red, yellow, green, blue, red);

─── OPACITY ───────────────────────────────────────────────────────────────────
    opacity: 0.5;   (affects entire element including children)
    Use rgba/hsla to affect only the color, not child elements.
""",
        "quiz_title": "Quiz 2 — Colors, Backgrounds & Gradients",
        "quiz_description": "20 questions on color formats, background properties, gradients, and opacity.",
        "time_limit": 20,
        "questions": [
            {"q": "Which CSS property sets the text (foreground) color?", "o": ["background-color", "font-color", "text-color", "color"], "a": "color"},
            {"q": "Which CSS property sets the background color of an element?", "o": ["color", "bg-color", "fill", "background-color"], "a": "background-color"},
            {"q": "What is the hex color code for pure white?", "o": ["#000000", "#FF0000", "#FFFFFF", "#00FF00"], "a": "#FFFFFF"},
            {"q": "What is the hex color code for pure black?", "o": ["#FFFFFF", "#FF0000", "#000000", "#0000FF"], "a": "#000000"},
            {"q": "What does the 'a' stand for in rgba()?", "o": ["Angle", "Array", "Alpha (opacity)", "Attribute"], "a": "Alpha (opacity)"},
            {"q": "In rgba(255, 0, 0, 0.5), what does 0.5 represent?", "o": ["50% brightness", "50% saturation", "50% opacity/transparency", "50% hue"], "a": "50% opacity/transparency"},
            {"q": "Which color format uses Hue, Saturation, and Lightness?", "o": ["RGB", "HEX", "RGBA", "HSL"], "a": "HSL"},
            {"q": "In HSL, what range is used for the Hue value?", "o": ["0–100", "0–255", "0–360", "0–1"], "a": "0–360"},
            {"q": "Which background property prevents an image from repeating?", "o": ["background-repeat: stop", "background-image: none", "background-repeat: no-repeat", "background-size: cover"], "a": "background-repeat: no-repeat"},
            {"q": "Which background-size value scales the image to cover the entire container (may crop)?", "o": ["contain", "fill", "stretch", "cover"], "a": "cover"},
            {"q": "Which background-size value scales the image to fit inside the container (no cropping)?", "o": ["cover", "fill", "fit", "contain"], "a": "contain"},
            {"q": "Which background-attachment value fixes the background relative to the viewport (parallax effect)?", "o": ["local", "scroll", "absolute", "fixed"], "a": "fixed"},
            {"q": "Which CSS function creates a linear colour gradient?", "o": ["gradient()", "color-gradient()", "linear-gradient()", "background-gradient()"], "a": "linear-gradient()"},
            {"q": "Which CSS function creates a radial (circular/elliptical) colour gradient?", "o": ["circular-gradient()", "ellipse-gradient()", "radial-gradient()", "round-gradient()"], "a": "radial-gradient()"},
            {"q": "In linear-gradient(to right, red, blue), which direction does the gradient flow?", "o": ["Top to bottom", "Bottom to top", "Right to left", "Left to right"], "a": "Left to right"},
            {"q": "What does opacity: 0 do to an element?", "o": ["Removes it from the DOM", "Makes it fully transparent (invisible but still takes space)", "Hides it like display: none", "Makes it semi-transparent"], "a": "Makes it fully transparent (invisible but still takes space)"},
            {"q": "What is the shorthand #F00 equivalent to in full hex?", "o": ["#F00000", "#FF0000", "#0F0000", "#00FF00"], "a": "#FF0000"},
            {"q": "Which property in the background shorthand sets the image?", "o": ["background-src", "background-url", "background-file", "background-image"], "a": "background-image"},
            {"q": "When multiple backgrounds are listed, which layer appears on top?", "o": ["The last one listed", "The smallest one", "The first one listed", "The one with highest z-index"], "a": "The first one listed"},
            {"q": "Which CSS function creates a cone-shaped gradient rotating around a centre point?", "o": ["cone-gradient()", "sweep-gradient()", "angular-gradient()", "conic-gradient()"], "a": "conic-gradient()"},
        ],
    },
    {
        "order": 3,
        "title": "The Box Model — Margin, Border, Padding & Sizing",
        "description": "Master the CSS box model: content, padding, border, and margin. Understand box-sizing, outline, border-radius, and how to calculate element dimensions.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 3: The Box Model — Margin, Border, Padding & Sizing

Every HTML element is a rectangular box. The CSS box model describes the space it occupies.

─── THE BOX MODEL ─────────────────────────────────────────────────────────────
From inside out:

    ┌──────────────────────────────┐  ← margin (transparent)
    │  ┌────────────────────────┐  │  ← border
    │  │  ┌──────────────────┐  │  │  ← padding (fills with background-color)
    │  │  │    content       │  │  │
    │  │  └──────────────────┘  │  │
    │  └────────────────────────┘  │
    └──────────────────────────────┘

─── CONTENT ───────────────────────────────────────────────────────────────────
    width:   200px;
    height:  100px;

─── PADDING ───────────────────────────────────────────────────────────────────
Space between content and border. Inherits background-color.
    padding: 20px;                     /* all sides */
    padding: 10px 20px;                /* top/bottom | left/right */
    padding: 10px 15px 20px 25px;      /* top right bottom left */
    padding-top / padding-right / padding-bottom / padding-left

─── BORDER ────────────────────────────────────────────────────────────────────
    border: 2px solid #333;
    border-width / border-style / border-color
    Border styles: solid | dashed | dotted | double | groove | ridge | inset | outset | none | hidden

    border-radius: 8px;        /* rounded corners */
    border-radius: 50%;        /* circle (when width = height) */

─── MARGIN ────────────────────────────────────────────────────────────────────
Space outside the border (transparent — does NOT inherit background).
    margin: 20px;
    margin: 0 auto;            /* centre block element horizontally */
    Negative margins are allowed.

⚠ Margin collapsing: vertical margins between adjacent block elements collapse to the larger of the two values.

─── BOX-SIZING ────────────────────────────────────────────────────────────────
    box-sizing: content-box;  (default) — width/height apply to content only
    box-sizing: border-box;   — width/height include padding + border

Best practice:
    *, *::before, *::after { box-sizing: border-box; }

─── CALCULATING TOTAL WIDTH (content-box default) ─────────────────────────────
    Total width = width + padding-left + padding-right + border-left + border-right + margin-left + margin-right

─── OUTLINE ───────────────────────────────────────────────────────────────────
    outline: 2px solid blue;
    outline-offset: 4px;
    Outlines do NOT take up space in the layout (no box model impact).

─── OVERFLOW ──────────────────────────────────────────────────────────────────
    overflow: visible | hidden | scroll | auto
    overflow-x / overflow-y (horizontal/vertical independently)
""",
        "quiz_title": "Quiz 3 — The Box Model",
        "quiz_description": "20 questions on content, padding, border, margin, box-sizing, border-radius, outline, and overflow.",
        "time_limit": 20,
        "questions": [
            {"q": "What are the four areas of the CSS box model from inside to outside?", "o": ["margin, border, padding, content", "padding, border, margin, content", "content, padding, border, margin", "content, margin, padding, border"], "a": "content, padding, border, margin"},
            {"q": "Which property adds space BETWEEN the content and the border?", "o": ["margin", "border-spacing", "padding", "gap"], "a": "padding"},
            {"q": "Which property adds space OUTSIDE the border?", "o": ["padding", "outer-space", "gap", "margin"], "a": "margin"},
            {"q": "What does margin: 0 auto do to a block element?", "o": ["Removes all margins", "Centres it horizontally", "Centres it vertically", "Adds equal padding on all sides"], "a": "Centres it horizontally"},
            {"q": "With box-sizing: content-box (default), what do width and height apply to?", "o": ["Content + padding + border", "Content + padding only", "Content + border only", "Content only"], "a": "Content only"},
            {"q": "With box-sizing: border-box, what do width and height include?", "o": ["Content only", "Content + margin", "Content + padding + border", "Content + padding only"], "a": "Content + padding + border"},
            {"q": "Which box-sizing value is considered best practice and recommended globally?", "o": ["content-box", "padding-box", "margin-box", "border-box"], "a": "border-box"},
            {"q": "What does border-radius: 50% do when applied to a square element?", "o": ["Adds a shadow", "Makes it a triangle", "Makes it an oval", "Makes it a circle"], "a": "Makes it a circle"},
            {"q": "Which CSS property controls what happens to content that overflows its container?", "o": ["clip", "scroll", "visible", "overflow"], "a": "overflow"},
            {"q": "What is margin collapsing?", "o": ["Margins being set to zero", "Margins being added together", "Negative margins cancelling out", "Vertical margins between adjacent blocks merging to the larger value"], "a": "Vertical margins between adjacent blocks merging to the larger value"},
            {"q": "What is the difference between outline and border?", "o": ["No difference", "Outline is inside the element; border is outside", "Border takes up space in the layout; outline does not", "Outline takes up space; border does not"], "a": "Border takes up space in the layout; outline does not"},
            {"q": "Which shorthand sets padding as: top=10px, right=20px, bottom=15px, left=5px?", "o": ["padding: 10px 15px 20px 5px", "padding: 10px 5px 15px 20px", "padding: 10px 20px 15px 5px", "padding: 5px 10px 20px 15px"], "a": "padding: 10px 20px 15px 5px"},
            {"q": "What is the total rendered width of an element with: width:200px, padding:10px, border:5px using content-box?", "o": ["200px", "215px", "220px", "230px"], "a": "230px"},
            {"q": "What is the total rendered width of the same element using border-box?", "o": ["170px", "200px", "215px", "230px"], "a": "200px"},
            {"q": "Which border-style value creates a dashed border?", "o": ["dotted", "lined", "broken", "dashed"], "a": "dashed"},
            {"q": "Which border-style value creates a dotted border?", "o": ["dashed", "dotted", "points", "spots"], "a": "dotted"},
            {"q": "Which property adds space between the outline and the element's border?", "o": ["outline-margin", "outline-gap", "outline-padding", "outline-offset"], "a": "outline-offset"},
            {"q": "Which overflow value adds a scrollbar only when content actually overflows?", "o": ["scroll", "hidden", "clip", "auto"], "a": "auto"},
            {"q": "Which overflow value always shows scrollbars even if content fits?", "o": ["auto", "visible", "clip", "scroll"], "a": "scroll"},
            {"q": "Which overflow value hides overflowing content without a scrollbar?", "o": ["scroll", "auto", "hidden", "clip"], "a": "hidden"},
        ],
    },
    {
        "order": 4,
        "title": "Typography & Text Styling",
        "description": "Style text with font-family, font-size, font-weight, line-height, letter-spacing, text-align, text-decoration, text-transform, and web fonts via @font-face and Google Fonts.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 4: Typography & Text Styling

Typography is one of the most visible aspects of design. CSS gives you full control over text rendering.

─── FONT FAMILY ───────────────────────────────────────────────────────────────
    font-family: 'Roboto', Arial, sans-serif;
    Always provide a font stack with a generic fallback:
    Generic families: serif | sans-serif | monospace | cursive | fantasy | system-ui

─── FONT SIZE ─────────────────────────────────────────────────────────────────
    font-size: 16px;     /* absolute pixels */
    font-size: 1rem;     /* relative to root element (html) font-size */
    font-size: 1em;      /* relative to parent element's font-size */
    font-size: 120%;     /* percentage of parent */
    font-size: 1.5vw;    /* viewport width */

─── FONT WEIGHT ───────────────────────────────────────────────────────────────
    font-weight: normal | bold | lighter | bolder
    font-weight: 100 | 200 | 300 | 400 (normal) | 500 | 600 | 700 (bold) | 800 | 900

─── FONT STYLE ────────────────────────────────────────────────────────────────
    font-style: normal | italic | oblique

─── LINE HEIGHT ───────────────────────────────────────────────────────────────
    line-height: 1.6;     /* unitless — recommended: 1.4–1.8 */
    line-height: 24px;
    line-height: 150%;

─── LETTER & WORD SPACING ─────────────────────────────────────────────────────
    letter-spacing: 0.05em;   /* space between characters */
    word-spacing: 0.1em;      /* space between words */

─── TEXT ALIGNMENT ────────────────────────────────────────────────────────────
    text-align: left | right | center | justify

─── TEXT DECORATION ───────────────────────────────────────────────────────────
    text-decoration: none | underline | overline | line-through
    text-decoration: underline dotted red;   /* line + style + color */

─── TEXT TRANSFORM ────────────────────────────────────────────────────────────
    text-transform: uppercase | lowercase | capitalize | none

─── TEXT INDENT ───────────────────────────────────────────────────────────────
    text-indent: 2em;   /* indent first line of paragraph */

─── TEXT SHADOW ───────────────────────────────────────────────────────────────
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    /* horizontal-offset vertical-offset blur color */

─── WHITE SPACE ───────────────────────────────────────────────────────────────
    white-space: normal | nowrap | pre | pre-wrap | pre-line
    white-space: nowrap   — prevents line wrapping

─── FONT SHORTHAND ────────────────────────────────────────────────────────────
    font: italic bold 1.2rem/1.6 'Roboto', sans-serif;
    /* style weight size/line-height family */

─── WEB FONTS ─────────────────────────────────────────────────────────────────
Google Fonts (in <head>):
    <link href="https://fonts.googleapis.com/css2?family=Roboto" rel="stylesheet">

@font-face (self-hosted):
    @font-face {
        font-family: 'MyFont';
        src: url('myfont.woff2') format('woff2');
    }
""",
        "quiz_title": "Quiz 4 — Typography & Text Styling",
        "quiz_description": "20 questions on font properties, text alignment, decoration, transform, spacing, shadow, and web fonts.",
        "time_limit": 20,
        "questions": [
            {"q": "Which CSS property sets the typeface/font used for text?", "o": ["font-type", "font-name", "typeface", "font-family"], "a": "font-family"},
            {"q": "Which unit is relative to the ROOT element's font-size?", "o": ["em", "px", "rem", "%"], "a": "rem"},
            {"q": "Which unit is relative to the PARENT element's font-size?", "o": ["rem", "px", "em", "vw"], "a": "em"},
            {"q": "What is the numeric font-weight value for 'bold'?", "o": ["600", "900", "500", "700"], "a": "700"},
            {"q": "What is the numeric font-weight value for 'normal'?", "o": ["200", "300", "400", "500"], "a": "400"},
            {"q": "Which property controls the vertical space between lines of text?", "o": ["line-spacing", "vertical-spacing", "text-height", "line-height"], "a": "line-height"},
            {"q": "Which property sets the horizontal spacing between individual characters?", "o": ["word-spacing", "char-spacing", "tracking", "letter-spacing"], "a": "letter-spacing"},
            {"q": "Which text-align value spreads text to fill the full line width?", "o": ["full", "fill", "stretch", "justify"], "a": "justify"},
            {"q": "Which text-decoration value removes the default underline from links?", "o": ["hidden", "off", "remove", "none"], "a": "none"},
            {"q": "Which text-transform value converts all text to UPPERCASE?", "o": ["capitalize", "upper", "caps", "uppercase"], "a": "uppercase"},
            {"q": "Which text-transform value capitalises only the First Letter of Each Word?", "o": ["title", "proper", "first-letter", "capitalize"], "a": "capitalize"},
            {"q": "Which property adds a shadow effect to text?", "o": ["font-shadow", "box-shadow", "drop-shadow", "text-shadow"], "a": "text-shadow"},
            {"q": "Which white-space value prevents text from wrapping to the next line?", "o": ["no-wrap", "clip", "overflow", "nowrap"], "a": "nowrap"},
            {"q": "Which CSS at-rule is used to load a self-hosted custom web font?", "o": ["@import-font", "@load-font", "@web-font", "@font-face"], "a": "@font-face"},
            {"q": "In the font shorthand, which property must always be included?", "o": ["font-style", "font-weight", "line-height", "font-family"], "a": "font-family"},
            {"q": "Which generic font family is best for body text on screens?", "o": ["serif", "cursive", "fantasy", "sans-serif"], "a": "sans-serif"},
            {"q": "Which property indents the first line of a paragraph?", "o": ["margin-left", "first-indent", "paragraph-indent", "text-indent"], "a": "text-indent"},
            {"q": "Which font-style value displays text in italic?", "o": ["slant", "incline", "oblique-light", "italic"], "a": "italic"},
            {"q": "What is the recommended unitless line-height range for body text readability?", "o": ["0.5–1.0", "1.0–1.2", "1.4–1.8", "2.0–3.0"], "a": "1.4–1.8"},
            {"q": "Which text-decoration style draws a line through the middle of text?", "o": ["underline", "overline", "strikethrough", "line-through"], "a": "line-through"},
        ],
    },
    {
        "order": 5,
        "title": "Display, Positioning & Z-index",
        "description": "Understand display values (block, inline, inline-block, none), CSS positioning (static, relative, absolute, fixed, sticky), z-index stacking, and visibility.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 5: Display, Positioning & Z-index

Understanding how elements are placed on the page is fundamental to CSS layout.

─── DISPLAY PROPERTY ──────────────────────────────────────────────────────────
    display: block         — full-width, starts on new line (div, p, h1)
    display: inline        — flows in text, no width/height (span, a, strong)
    display: inline-block  — flows in text BUT accepts width/height
    display: none          — removes element from layout (not rendered)
    display: flex          — flex container (Lesson 6)
    display: grid          — grid container (Lesson 7)
    display: table / table-cell / table-row — table-like behaviour

─── VISIBILITY vs DISPLAY: NONE ───────────────────────────────────────────────
    visibility: hidden  — element is invisible but STILL takes up space
    display: none       — element is completely removed from layout (no space)

─── POSITION PROPERTY ─────────────────────────────────────────────────────────
    static   — default; follows normal document flow; top/left/right/bottom have NO effect
    relative — offset FROM its normal position; still occupies original space
    absolute — removed from flow; positioned relative to nearest positioned ancestor
    fixed    — removed from flow; positioned relative to the VIEWPORT; stays on scroll
    sticky   — hybrid: relative until a scroll threshold, then fixed

Position offsets: top | right | bottom | left

─── POSITIONED ANCESTOR ───────────────────────────────────────────────────────
An "absolute" child positions itself relative to the nearest ancestor with
position: relative | absolute | fixed | sticky (NOT static).
Common pattern:
    .parent  { position: relative; }
    .child   { position: absolute; top: 0; right: 0; }

─── Z-INDEX ───────────────────────────────────────────────────────────────────
    z-index: 10;
    Controls stacking order. Higher value = on top.
    Only works on POSITIONED elements (not static).
    z-index: auto   — participates in parent stacking context
    z-index: -1     — behind normal flow elements

─── STACKING CONTEXT ──────────────────────────────────────────────────────────
A new stacking context is created by: position (non-static) + z-index value,
opacity < 1, transform, filter, will-change, isolation: isolate, etc.

─── CENTERING TECHNIQUES ──────────────────────────────────────────────────────
Absolute centering:
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);

─── FLOAT & CLEAR (legacy) ────────────────────────────────────────────────────
    float: left | right | none
    clear: left | right | both | none
    Float removes elements from normal flow (used before flexbox/grid).
    Clearfix: .parent::after { content: ''; display: table; clear: both; }
""",
        "quiz_title": "Quiz 5 — Display, Positioning & Z-index",
        "quiz_description": "20 questions on display values, position types, offsets, z-index, stacking contexts, and float.",
        "time_limit": 20,
        "questions": [
            {"q": "Which display value makes an element take up the full available width and start on a new line?", "o": ["inline", "inline-block", "flex", "block"], "a": "block"},
            {"q": "Which display value allows an element to sit inline with text but also accept width and height?", "o": ["block", "inline", "flex", "inline-block"], "a": "inline-block"},
            {"q": "Which display value completely removes an element from the layout?", "o": ["visibility: hidden", "opacity: 0", "hidden", "none"], "a": "none"},
            {"q": "What is the difference between display: none and visibility: hidden?", "o": ["No difference", "display:none hides but keeps space; visibility:hidden removes element", "visibility:hidden removes element; display:none hides but keeps space", "display:none removes element from layout; visibility:hidden hides but keeps space"], "a": "display:none removes element from layout; visibility:hidden hides but keeps space"},
            {"q": "Which position value is the default for all elements?", "o": ["relative", "absolute", "fixed", "static"], "a": "static"},
            {"q": "Which position value offsets an element from its normal position without removing it from flow?", "o": ["static", "absolute", "fixed", "relative"], "a": "relative"},
            {"q": "Which position value removes an element from flow and positions it relative to its nearest positioned ancestor?", "o": ["fixed", "sticky", "relative", "absolute"], "a": "absolute"},
            {"q": "Which position value keeps an element fixed relative to the VIEWPORT as the user scrolls?", "o": ["absolute", "sticky", "relative", "fixed"], "a": "fixed"},
            {"q": "Which position value acts like relative until a scroll threshold, then behaves like fixed?", "o": ["relative", "absolute", "fixed", "sticky"], "a": "sticky"},
            {"q": "For position: absolute to work, what must its container have?", "o": ["display: block", "position: absolute", "overflow: hidden", "A position value other than static"], "a": "A position value other than static"},
            {"q": "Which property controls the stacking order of positioned elements?", "o": ["stack-order", "layer", "depth", "z-index"], "a": "z-index"},
            {"q": "Does z-index work on elements with position: static?", "o": ["Yes, always", "Only with a positive value", "Only with a negative value", "No"], "a": "No"},
            {"q": "Which z-index value places an element behind normal flow content?", "o": ["z-index: 0", "z-index: auto", "z-index: 1", "z-index: -1"], "a": "z-index: -1"},
            {"q": "What CSS technique centres an absolutely positioned element both horizontally and vertically?", "o": ["margin: auto", "top:0; left:0; margin: auto", "top:50%; left:50%; transform:translate(-50%,-50%)", "align: center"], "a": "top:50%; left:50%; transform:translate(-50%,-50%)"},
            {"q": "Which position value is NOT removed from the normal document flow?", "o": ["absolute", "fixed", "relative", "All of the above stay in flow"], "a": "relative"},
            {"q": "Which CSS property was used for layouts BEFORE flexbox and grid?", "o": ["display: table", "position: relative", "float", "clear"], "a": "float"},
            {"q": "Which clear value clears both left and right floats?", "o": ["all", "none", "left", "both"], "a": "both"},
            {"q": "Which display value is the default for <span> elements?", "o": ["block", "inline-block", "flex", "inline"], "a": "inline"},
            {"q": "Which display value is the default for <div> elements?", "o": ["inline", "flex", "inline-block", "block"], "a": "block"},
            {"q": "What creates a new stacking context in CSS?", "o": ["Any positioned element", "Only z-index: 0", "display: block", "A positioned element with a z-index value other than auto"], "a": "A positioned element with a z-index value other than auto"},
        ],
    },
    {
        "order": 6,
        "title": "Flexbox Layout",
        "description": "Master CSS Flexbox: flex container vs flex items, flex-direction, flex-wrap, justify-content, align-items, align-self, flex-grow, flex-shrink, flex-basis, and the flex shorthand.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 6: Flexbox Layout

Flexbox (Flexible Box Layout) is a one-dimensional layout system for rows OR columns.

─── ENABLING FLEXBOX ──────────────────────────────────────────────────────────
    .container { display: flex; }

─── FLEX CONTAINER PROPERTIES ─────────────────────────────────────────────────

flex-direction  — main axis direction
    row (default) | row-reverse | column | column-reverse

flex-wrap       — allow items to wrap onto multiple lines
    nowrap (default) | wrap | wrap-reverse

flex-flow       — shorthand for flex-direction + flex-wrap
    flex-flow: row wrap;

justify-content — align items along the MAIN axis
    flex-start | flex-end | center | space-between | space-around | space-evenly

align-items     — align items along the CROSS axis (single line)
    stretch (default) | flex-start | flex-end | center | baseline

align-content   — align MULTIPLE lines along the cross axis (when wrapping)
    flex-start | flex-end | center | space-between | space-around | stretch

gap             — space between flex items
    gap: 20px;
    row-gap: 10px; column-gap: 20px;

─── FLEX ITEM PROPERTIES ──────────────────────────────────────────────────────

flex-grow       — factor by which item GROWS to fill available space (default: 0)
    flex-grow: 1;   (item takes equal share of free space)

flex-shrink     — factor by which item SHRINKS when space is tight (default: 1)
    flex-shrink: 0;  (item never shrinks)

flex-basis      — initial size of the item BEFORE growing/shrinking (default: auto)
    flex-basis: 200px;

flex            — shorthand: flex-grow flex-shrink flex-basis
    flex: 1;        → flex: 1 1 0  (most common)
    flex: auto;     → flex: 1 1 auto
    flex: none;     → flex: 0 0 auto (no grow, no shrink)

align-self      — override container's align-items for a single item
    auto | stretch | flex-start | flex-end | center | baseline

order           — visual order of item (default: 0; lower = earlier)

─── MAIN AXIS vs CROSS AXIS ───────────────────────────────────────────────────
    flex-direction: row     → main = horizontal, cross = vertical
    flex-direction: column  → main = vertical,   cross = horizontal

─── COMMON PATTERNS ───────────────────────────────────────────────────────────
Centre an item:
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
    }

Equal-width columns:
    .item { flex: 1; }
""",
        "quiz_title": "Quiz 6 — Flexbox Layout",
        "quiz_description": "20 questions on flex container properties, flex item properties, axes, alignment, and common patterns.",
        "time_limit": 20,
        "questions": [
            {"q": "Which CSS property enables Flexbox on a container?", "o": ["display: block", "display: inline", "display: grid", "display: flex"], "a": "display: flex"},
            {"q": "Which property sets the direction of the main axis in Flexbox?", "o": ["flex-axis", "main-direction", "flex-wrap", "flex-direction"], "a": "flex-direction"},
            {"q": "What is the default value of flex-direction?", "o": ["column", "row-reverse", "column-reverse", "row"], "a": "row"},
            {"q": "Which property allows flex items to wrap onto multiple lines?", "o": ["flex-overflow", "flex-direction", "flex-break", "flex-wrap"], "a": "flex-wrap"},
            {"q": "Which property aligns items along the MAIN axis?", "o": ["align-items", "align-content", "align-self", "justify-content"], "a": "justify-content"},
            {"q": "Which property aligns items along the CROSS axis (single line)?", "o": ["justify-content", "justify-self", "align-content", "align-items"], "a": "align-items"},
            {"q": "Which justify-content value places equal space BETWEEN items (no space at edges)?", "o": ["space-around", "space-evenly", "center", "space-between"], "a": "space-between"},
            {"q": "Which justify-content value places equal space AROUND items (including edges)?", "o": ["space-between", "space-evenly", "center", "space-around"], "a": "space-around"},
            {"q": "What does flex-grow: 1 do?", "o": ["Fixes the item size at 1px", "Prevents the item from growing", "Allows the item to take its share of available free space", "Sets the item's width to 100%"], "a": "Allows the item to take its share of available free space"},
            {"q": "What does flex-shrink: 0 do?", "o": ["Makes the item disappear", "Allows the item to shrink as much as needed", "Sets item size to 0", "Prevents the item from shrinking below its flex-basis"], "a": "Prevents the item from shrinking below its flex-basis"},
            {"q": "What does flex-basis set?", "o": ["The maximum size of the item", "The order of the item", "The initial size of the item before growing/shrinking", "The gap between items"], "a": "The initial size of the item before growing/shrinking"},
            {"q": "What does flex: 1 expand to?", "o": ["flex: 1 0 0", "flex: 1 1 auto", "flex: 0 1 auto", "flex: 1 1 0"], "a": "flex: 1 1 0"},
            {"q": "Which property overrides align-items for a single flex item?", "o": ["justify-self", "self-align", "align-content", "align-self"], "a": "align-self"},
            {"q": "Which property changes the visual order of a flex item without changing the DOM?", "o": ["z-index", "flex-position", "index", "order"], "a": "order"},
            {"q": "When flex-direction is column, which axis becomes the main axis?", "o": ["Horizontal", "Diagonal", "Neither", "Vertical"], "a": "Vertical"},
            {"q": "Which property is a shorthand for flex-direction AND flex-wrap?", "o": ["flex-layout", "flex", "flex-box", "flex-flow"], "a": "flex-flow"},
            {"q": "What does align-content do (unlike align-items)?", "o": ["Aligns a single item", "Aligns the container itself", "Aligns multiple lines of items along the cross axis", "Aligns items along the main axis"], "a": "Aligns multiple lines of items along the cross axis"},
            {"q": "What is the default value of align-items?", "o": ["flex-start", "center", "flex-end", "stretch"], "a": "stretch"},
            {"q": "Which property adds space between flex items without using margin?", "o": ["padding", "spacing", "gutter", "gap"], "a": "gap"},
            {"q": "To perfectly centre content both horizontally and vertically in a flex container, you use:", "o": ["margin: auto on children", "text-align: center and vertical-align: middle", "justify-content: center and align-items: center", "position: absolute on children"], "a": "justify-content: center and align-items: center"},
        ],
    },
    {
        "order": 7,
        "title": "CSS Grid Layout",
        "description": "Build two-dimensional layouts with CSS Grid: grid-template-columns, grid-template-rows, fr unit, gap, grid-column/row placement, grid-template-areas, and auto-placement.",
        "duration_minutes": 45,
        "content": """Welcome to Lesson 7: CSS Grid Layout

CSS Grid is a two-dimensional layout system — it handles both rows AND columns simultaneously.

─── ENABLING GRID ─────────────────────────────────────────────────────────────
    .container { display: grid; }

─── DEFINING COLUMNS & ROWS ───────────────────────────────────────────────────
    grid-template-columns: 200px 1fr 1fr;
    grid-template-rows: 100px auto 50px;

    The fr unit distributes FREE space proportionally:
        grid-template-columns: 1fr 2fr 1fr;
        → column 2 gets twice the free space of columns 1 and 3

─── REPEAT() FUNCTION ─────────────────────────────────────────────────────────
    grid-template-columns: repeat(3, 1fr);     /* 3 equal columns */
    grid-template-columns: repeat(4, 200px);   /* 4 fixed columns */

─── MINMAX() FUNCTION ─────────────────────────────────────────────────────────
    grid-template-columns: repeat(3, minmax(150px, 1fr));
    Item is at least 150px wide but can grow up to 1fr.

─── AUTO-FILL vs AUTO-FIT ─────────────────────────────────────────────────────
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    auto-fill  — fills row with as many columns as possible (may leave empty)
    auto-fit   — collapses empty columns and stretches filled ones

─── GAP ───────────────────────────────────────────────────────────────────────
    gap: 20px;
    row-gap: 10px;
    column-gap: 20px;

─── PLACING GRID ITEMS ────────────────────────────────────────────────────────
    grid-column: 1 / 3;    /* start at line 1, end at line 3 (spans 2 columns) */
    grid-row:    1 / 2;
    grid-column: 1 / -1;   /* span all columns to the last line */
    grid-column: span 2;   /* span 2 columns from current position */

─── GRID TEMPLATE AREAS ───────────────────────────────────────────────────────
    .container {
        display: grid;
        grid-template-areas:
            "header header"
            "sidebar main"
            "footer footer";
        grid-template-columns: 200px 1fr;
    }
    .header  { grid-area: header; }
    .sidebar { grid-area: sidebar; }
    .main    { grid-area: main; }
    .footer  { grid-area: footer; }
    Use a dot (.) for an empty cell: "sidebar . main"

─── ALIGNMENT IN GRID ─────────────────────────────────────────────────────────
    justify-items   — align items along the INLINE (row) axis within their cell
    align-items     — align items along the BLOCK (column) axis within their cell
    justify-content — align the entire grid along the inline axis
    align-content   — align the entire grid along the block axis

    Per-item overrides:
    justify-self / align-self

─── IMPLICIT vs EXPLICIT GRID ─────────────────────────────────────────────────
    Explicit: defined by grid-template-columns / grid-template-rows
    Implicit: auto-generated rows/columns when items exceed the explicit grid
    grid-auto-rows: 100px;
    grid-auto-columns: 1fr;
    grid-auto-flow: row | column | dense
""",
        "quiz_title": "Quiz 7 — CSS Grid Layout",
        "quiz_description": "20 questions on grid-template-columns/rows, fr unit, repeat, minmax, gap, placement, template areas, and alignment.",
        "time_limit": 20,
        "questions": [
            {"q": "Which CSS property enables Grid layout on a container?", "o": ["display: flex", "display: block", "display: inline-grid", "display: grid"], "a": "display: grid"},
            {"q": "Which property defines the column structure of a grid?", "o": ["grid-columns", "grid-template", "grid-layout-columns", "grid-template-columns"], "a": "grid-template-columns"},
            {"q": "Which property defines the row structure of a grid?", "o": ["grid-rows", "grid-template", "grid-layout-rows", "grid-template-rows"], "a": "grid-template-rows"},
            {"q": "What does the fr unit represent in CSS Grid?", "o": ["Fixed ratio", "Font relative unit", "A fraction of the available free space", "Full row width"], "a": "A fraction of the available free space"},
            {"q": "What does repeat(3, 1fr) expand to?", "o": ["1fr 1fr", "1fr 2fr 3fr", "3fr", "1fr 1fr 1fr"], "a": "1fr 1fr 1fr"},
            {"q": "What does grid-column: 1 / 3 mean?", "o": ["Place in column 1 with width of 3px", "Span 3 columns", "Start at column line 1 and end at column line 3 (spans 2 columns)", "Start at column 1, span to column 3 inclusive"], "a": "Start at column line 1 and end at column line 3 (spans 2 columns)"},
            {"q": "What does grid-column: 1 / -1 do?", "o": ["Hides the item", "Places item in the last column", "Spans the item across ALL columns to the last grid line", "Reverses the column order"], "a": "Spans the item across ALL columns to the last grid line"},
            {"q": "What is the purpose of grid-template-areas?", "o": ["Sets background in grid cells", "Names grid lines", "Defines grid layout using named regions in a visual ASCII format", "Creates implicit grid rows"], "a": "Defines grid layout using named regions in a visual ASCII format"},
            {"q": "Which property assigns a grid item to a named template area?", "o": ["grid-name", "grid-position", "grid-region", "grid-area"], "a": "grid-area"},
            {"q": "What character represents an empty cell in grid-template-areas?", "o": ["0", "x", "empty", "."], "a": "."},
            {"q": "What does minmax(150px, 1fr) mean?", "o": ["The column is exactly 150px", "The column is at minimum 150px and at maximum 1fr of free space", "The column is 1fr wide with 150px gap", "The column cannot exceed 150px"], "a": "The column is at minimum 150px and at maximum 1fr of free space"},
            {"q": "What is the difference between auto-fill and auto-fit in repeat()?", "o": ["No difference", "auto-fill fills with as many columns as possible (can leave empty); auto-fit collapses empty columns", "auto-fit fills with as many columns as possible; auto-fill collapses empty columns", "auto-fill is for rows; auto-fit is for columns"], "a": "auto-fill fills with as many columns as possible (can leave empty); auto-fit collapses empty columns"},
            {"q": "Which property adds space between grid rows AND columns?", "o": ["margin", "padding", "spacing", "gap"], "a": "gap"},
            {"q": "Which property aligns grid items along the INLINE (horizontal) axis within their cell?", "o": ["align-items", "align-content", "justify-content", "justify-items"], "a": "justify-items"},
            {"q": "Which property aligns grid items along the BLOCK (vertical) axis within their cell?", "o": ["justify-items", "justify-content", "align-content", "align-items"], "a": "align-items"},
            {"q": "What is an implicit grid?", "o": ["A grid with no columns defined", "A grid created with display: inline-grid", "Auto-generated rows or columns for items that exceed the explicit grid", "A grid with equal rows and columns"], "a": "Auto-generated rows or columns for items that exceed the explicit grid"},
            {"q": "Which property sets the size of implicitly created rows?", "o": ["grid-implicit-rows", "grid-template-rows: auto", "grid-row-size", "grid-auto-rows"], "a": "grid-auto-rows"},
            {"q": "What does grid-column: span 3 mean?", "o": ["Place item in column 3", "Start at column 3", "Item spans 3 column tracks from its current position", "Item takes 3fr of space"], "a": "Item spans 3 column tracks from its current position"},
            {"q": "CSS Grid is best described as which type of layout system?", "o": ["One-dimensional (row only)", "One-dimensional (column only)", "Three-dimensional", "Two-dimensional (rows and columns)"], "a": "Two-dimensional (rows and columns)"},
            {"q": "What is the key difference between CSS Grid and Flexbox?", "o": ["Grid works only for columns; Flexbox for rows", "They are identical", "Grid is 2D (rows + columns); Flexbox is 1D (row or column)", "Flexbox is 2D; Grid is 1D"], "a": "Grid is 2D (rows + columns); Flexbox is 1D (row or column)"},
        ],
    },
    {
        "order": 8,
        "title": "Responsive Design & Media Queries",
        "description": "Build layouts that adapt to any screen size using media queries, breakpoints, mobile-first vs desktop-first approaches, viewport units, relative units, and CSS custom properties (variables).",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 8: Responsive Design & Media Queries

Responsive web design ensures your site looks great on all screen sizes.

─── VIEWPORT META TAG ─────────────────────────────────────────────────────────
Essential for mobile responsiveness:
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

─── MEDIA QUERIES ─────────────────────────────────────────────────────────────
    @media (max-width: 768px) {
        /* styles for screens 768px and below */
    }
    @media (min-width: 769px) and (max-width: 1200px) {
        /* styles for tablets */
    }

Media types: all | screen | print | speech

Media features:
    width / min-width / max-width
    height / min-height / max-height
    orientation: portrait | landscape
    resolution: 2dppx  (retina)
    prefers-color-scheme: dark | light
    prefers-reduced-motion: reduce

─── MOBILE-FIRST vs DESKTOP-FIRST ────────────────────────────────────────────
    Mobile-first  → write base styles for mobile, use min-width to scale UP
    Desktop-first → write base styles for desktop, use max-width to scale DOWN

Mobile-first (recommended):
    /* base styles for mobile */
    @media (min-width: 768px)  { /* tablet  */ }
    @media (min-width: 1200px) { /* desktop */ }

─── COMMON BREAKPOINTS ────────────────────────────────────────────────────────
    < 576px   Extra small (phones)
    576–767px Small (large phones)
    768–991px Medium (tablets)
    992–1199px Large (desktops)
    ≥ 1200px  Extra large

─── RELATIVE UNITS FOR RESPONSIVE DESIGN ──────────────────────────────────────
    %     — percentage of parent
    rem   — relative to root font-size
    em    — relative to current element's font-size
    vw    — 1% of viewport width
    vh    — 1% of viewport height
    vmin  — 1% of the smaller viewport dimension
    vmax  — 1% of the larger viewport dimension

─── CSS CUSTOM PROPERTIES (VARIABLES) ─────────────────────────────────────────
    :root {
        --primary-color: #3498db;
        --font-size-base: 1rem;
        --max-width: 1200px;
    }

    .button {
        background: var(--primary-color);
        font-size: var(--font-size-base);
    }

    /* Override in media query */
    @media (max-width: 768px) {
        :root { --font-size-base: 0.875rem; }
    }

─── FLUID TYPOGRAPHY ──────────────────────────────────────────────────────────
    font-size: clamp(1rem, 2.5vw, 2rem);
    /* min  preferred  max */

─── CSS CALC() ────────────────────────────────────────────────────────────────
    width: calc(100% - 2rem);
    padding: calc(1rem + 2vw);
    Can mix different units.
""",
        "quiz_title": "Quiz 8 — Responsive Design & Media Queries",
        "quiz_description": "20 questions on media queries, breakpoints, mobile-first, viewport units, CSS variables, clamp, and calc.",
        "time_limit": 20,
        "questions": [
            {"q": "Which HTML meta tag is essential for responsive web design on mobile?", "o": ["<meta name='responsive'>", "<meta name='mobile'>", "<meta name='viewport' content='width=device-width, initial-scale=1.0'>", "<meta charset='UTF-8'>"], "a": "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"},
            {"q": "Which CSS at-rule is used to apply styles based on screen size or device features?", "o": ["@screen", "@breakpoint", "@viewport", "@media"], "a": "@media"},
            {"q": "Which media feature applies styles to screens UP TO 768px wide?", "o": ["min-width: 768px", "max-width: 769px", "width: 768px", "max-width: 768px"], "a": "max-width: 768px"},
            {"q": "Which media feature applies styles to screens 768px and wider?", "o": ["max-width: 768px", "min-width: 769px", "width: 768px", "min-width: 768px"], "a": "min-width: 768px"},
            {"q": "What does the mobile-first approach mean?", "o": ["Only designing for mobile", "Writing base styles for desktop and overriding for mobile with max-width", "Writing base styles for mobile and scaling up with min-width media queries", "Using only viewport units"], "a": "Writing base styles for mobile and scaling up with min-width media queries"},
            {"q": "Which CSS unit represents 1% of the viewport width?", "o": ["vmin", "vmax", "vh", "vw"], "a": "vw"},
            {"q": "Which CSS unit represents 1% of the viewport height?", "o": ["vw", "vmin", "vmax", "vh"], "a": "vh"},
            {"q": "Which CSS unit is relative to the ROOT element's font-size?", "o": ["em", "px", "vw", "rem"], "a": "rem"},
            {"q": "How do you declare a CSS custom property (variable) named --primary-color?", "o": ["var(--primary-color: #333)", "set --primary-color: #333", "$primary-color: #333", "--primary-color: #333 inside :root {}"], "a": "--primary-color: #333 inside :root {}"},
            {"q": "How do you USE a CSS custom property named --primary-color?", "o": ["$primary-color", "--primary-color", "variable(--primary-color)", "var(--primary-color)"], "a": "var(--primary-color)"},
            {"q": "Which CSS function clamps a value between a minimum and maximum?", "o": ["range()", "between()", "minmax()", "clamp()"], "a": "clamp()"},
            {"q": "What does clamp(1rem, 2.5vw, 2rem) do?", "o": ["Sets font-size to exactly 2.5vw always", "Sets font-size to at least 1rem, preferring 2.5vw, but never exceeding 2rem", "Sets font-size between 1rem and 2rem only on mobile", "Sets minimum padding to 2rem"], "a": "Sets font-size to at least 1rem, preferring 2.5vw, but never exceeding 2rem"},
            {"q": "Which CSS function allows you to mix different units in calculations?", "o": ["mix()", "compute()", "convert()", "calc()"], "a": "calc()"},
            {"q": "Which media feature detects dark mode preference?", "o": ["prefers-theme: dark", "color-scheme: dark", "prefers-dark-mode: true", "prefers-color-scheme: dark"], "a": "prefers-color-scheme: dark"},
            {"q": "Which media feature detects the device orientation?", "o": ["device-angle", "screen-rotation", "display-mode", "orientation"], "a": "orientation"},
            {"q": "Which orientation value applies when the screen is taller than it is wide?", "o": ["vertical", "upright", "landscape", "portrait"], "a": "portrait"},
            {"q": "Where should CSS custom properties typically be declared for global access?", "o": ["In the body selector", "In a @media query", "In the html selector", "In the :root pseudo-class"], "a": "In the :root pseudo-class"},
            {"q": "Which unit vmin represents?", "o": ["1% of the viewport width", "1% of the viewport height", "1% of the larger viewport dimension", "1% of the smaller viewport dimension"], "a": "1% of the smaller viewport dimension"},
            {"q": "In a mobile-first approach, which type of media queries do you use to add desktop styles?", "o": ["max-width", "only screen", "not screen", "min-width"], "a": "min-width"},
            {"q": "Which media type targets only printed documents?", "o": ["document", "paper", "screen", "print"], "a": "print"},
        ],
    },
    {
        "order": 9,
        "title": "Transitions, Animations & Transforms",
        "description": "Add motion with CSS transitions, keyframe animations (@keyframes), animation properties, and 2D/3D transforms (translate, rotate, scale, skew, perspective).",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 9: Transitions, Animations & Transforms

CSS provides powerful tools to animate and transform elements without JavaScript.

─── CSS TRANSITIONS ───────────────────────────────────────────────────────────
Smoothly animate property changes triggered by state (e.g. :hover):
    transition: property duration timing-function delay;

    transition: background-color 0.3s ease;
    transition: all 0.5s ease-in-out 0.1s;
    transition: width 0.3s ease, opacity 0.5s linear;  /* multiple */

Timing functions:
    ease (default) | linear | ease-in | ease-out | ease-in-out
    cubic-bezier(x1, y1, x2, y2)
    steps(4, end)

─── CSS TRANSFORMS ────────────────────────────────────────────────────────────
Modify the visual appearance without affecting layout:

2D Transforms:
    transform: translateX(50px);       /* move right */
    transform: translateY(-20px);      /* move up */
    transform: translate(50px, -20px); /* move right and up */
    transform: rotate(45deg);          /* clockwise rotation */
    transform: scaleX(1.5);            /* stretch horizontally */
    transform: scale(2);               /* double size */
    transform: skewX(20deg);           /* skew along X axis */

Multiple transforms (space-separated):
    transform: translate(50px, 20px) rotate(45deg) scale(1.2);
    Note: order matters — transforms are applied right to left.

Transform origin:
    transform-origin: center center;   /* default */
    transform-origin: top left;
    transform-origin: 50% 100%;

3D Transforms:
    transform: rotateX(45deg);
    transform: rotateY(45deg);
    transform: perspective(500px) rotateY(45deg);

    perspective: 1000px;   /* on parent, sets 3D depth */

─── CSS ANIMATIONS ────────────────────────────────────────────────────────────
Keyframe animations run automatically (no state trigger needed):

1. Define keyframes:
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes bounce {
        0%   { transform: translateY(0); }
        50%  { transform: translateY(-30px); }
        100% { transform: translateY(0); }
    }

2. Apply to element:
    animation: fadeIn 0.5s ease-out forwards;

Animation properties:
    animation-name:            keyframe name
    animation-duration:        how long (e.g. 1s, 500ms)
    animation-timing-function: ease | linear | steps()
    animation-delay:           wait before starting
    animation-iteration-count: 1 | 3 | infinite
    animation-direction:       normal | reverse | alternate | alternate-reverse
    animation-fill-mode:       none | forwards | backwards | both
    animation-play-state:      running | paused

Shorthand:
    animation: name duration timing delay iteration direction fill-mode;

─── WILL-CHANGE ───────────────────────────────────────────────────────────────
    will-change: transform, opacity;
    Hints to the browser to promote the element to its own GPU layer.
    Use sparingly — only for known animations.
""",
        "quiz_title": "Quiz 9 — Transitions, Animations & Transforms",
        "quiz_description": "20 questions on CSS transitions, transform functions, @keyframes, animation properties, and timing functions.",
        "time_limit": 20,
        "questions": [
            {"q": "Which CSS property smoothly animates changes between two states (e.g. on :hover)?", "o": ["animation", "keyframe", "motion", "transition"], "a": "transition"},
            {"q": "What are the four values in the transition shorthand (in order)?", "o": ["name, duration, delay, timing-function", "property, delay, duration, timing-function", "property, timing-function, duration, delay", "property, duration, timing-function, delay"], "a": "property, duration, timing-function, delay"},
            {"q": "Which timing function makes the transition start slow, speed up, then slow down?", "o": ["linear", "ease-in", "ease-out", "ease-in-out"], "a": "ease-in-out"},
            {"q": "Which timing function makes the transition progress at a constant speed?", "o": ["ease", "ease-in", "ease-out", "linear"], "a": "linear"},
            {"q": "Which CSS property applies 2D and 3D transformations to an element?", "o": ["translate", "motion", "transform", "move"], "a": "transform"},
            {"q": "Which transform function moves an element horizontally and/or vertically?", "o": ["rotate()", "scale()", "skew()", "translate()"], "a": "translate()"},
            {"q": "Which transform function rotates an element by a given angle?", "o": ["turn()", "skew()", "translate()", "rotate()"], "a": "rotate()"},
            {"q": "Which transform function resizes an element?", "o": ["resize()", "size()", "translate()", "scale()"], "a": "scale()"},
            {"q": "What does transform: scale(2) do?", "o": ["Moves the element 2px", "Doubles the element's size", "Rotates it 2 degrees", "Halves the element's size"], "a": "Doubles the element's size"},
            {"q": "Which at-rule defines CSS keyframe animations?", "o": ["@animation", "@transition", "@motion", "@keyframes"], "a": "@keyframes"},
            {"q": "Which animation property specifies how many times an animation repeats?", "o": ["animation-repeat", "animation-loop", "animation-count", "animation-iteration-count"], "a": "animation-iteration-count"},
            {"q": "Which animation-iteration-count value makes an animation loop forever?", "o": ["forever", "loop", "repeat", "infinite"], "a": "infinite"},
            {"q": "Which animation-fill-mode value keeps the end state of the animation after it finishes?", "o": ["both", "backwards", "end", "forwards"], "a": "forwards"},
            {"q": "Which animation property controls whether the animation is running or paused?", "o": ["animation-state", "animation-control", "animation-status", "animation-play-state"], "a": "animation-play-state"},
            {"q": "Which animation-direction value makes the animation alternate between forward and reverse on each cycle?", "o": ["reverse", "loop", "back-forward", "alternate"], "a": "alternate"},
            {"q": "What does transform-origin control?", "o": ["The starting position of a translate", "The speed of a transform", "The fixed point around which transformations are applied", "The perspective depth"], "a": "The fixed point around which transformations are applied"},
            {"q": "Which property on a parent element sets the perspective depth for 3D child transforms?", "o": ["depth", "3d-view", "perspective-origin", "perspective"], "a": "perspective"},
            {"q": "What does will-change: transform tell the browser?", "o": ["Disable transitions on this element", "The element's transform will never change", "Pre-optimise (GPU layer) for upcoming transform changes", "Apply transform on page load"], "a": "Pre-optimise (GPU layer) for upcoming transform changes"},
            {"q": "What is the difference between a transition and an animation in CSS?", "o": ["They are identical", "Transitions are JavaScript-only; animations are CSS-only", "Transitions require a trigger (state change); animations can run automatically", "Animations require a trigger; transitions run automatically"], "a": "Transitions require a trigger (state change); animations can run automatically"},
            {"q": "When multiple transforms are chained (e.g. translate rotate scale), in what order are they applied?", "o": ["Left to right", "Randomly", "Simultaneously", "Right to left"], "a": "Right to left"},
        ],
    },
    {
        "order": 10,
        "title": "Final Review — Comprehensive CSS Assessment",
        "description": "A 100-question comprehensive quiz covering all nine CSS lessons: selectors, colors, box model, typography, display/position, flexbox, grid, responsive design, and animations.",
        "duration_minutes": 100,
        "content": """Welcome to Lesson 10: Final Review — Comprehensive CSS Assessment

This is your final assessment covering everything from Lessons 1 through 9.

Topics covered:
  1. CSS syntax, selectors, combinators & specificity
  2. Colors, backgrounds & gradients
  3. The box model — margin, border, padding & sizing
  4. Typography & text styling
  5. Display, positioning & z-index
  6. Flexbox layout
  7. CSS Grid layout
  8. Responsive design & media queries
  9. Transitions, animations & transforms

You have 100 questions and 100 minutes. A score of 70% is required to pass.

Good luck!
""",
        "quiz_title": "Final Quiz — Comprehensive CSS (100 Questions)",
        "quiz_description": "100-question comprehensive CSS assessment covering all topics from the entire course.",
        "time_limit": 100,
        "questions": [
            # Selectors & Basics (1–12)
            {"q": "What does CSS stand for?", "o": ["Creative Style Sheets", "Computer Style Sheets", "Colorful Style Sheets", "Cascading Style Sheets"], "a": "Cascading Style Sheets"},
            {"q": "Which selector targets ALL elements on a page?", "o": ["all", "every", "body", "*"], "a": "*"},
            {"q": "Which selector targets elements by class name?", "o": ["#classname", "classname", "*classname", ".classname"], "a": ".classname"},
            {"q": "Which selector targets a unique element by id?", "o": [".id", "*id", "id", "#id"], "a": "#id"},
            {"q": "Which combinator selects direct children only?", "o": ["div p", "div + p", "div ~ p", "div > p"], "a": "div > p"},
            {"q": "Which combinator selects the immediately adjacent sibling?", "o": ["div ~ p", "div > p", "div p", "div + p"], "a": "div + p"},
            {"q": "Which pseudo-class targets elements that do NOT match a selector?", "o": [":exclude()", ":without()", ":none()", ":not()"], "a": ":not()"},
            {"q": "Which pseudo-element inserts content before an element?", "o": ["::after", "::first-line", "::prepend", "::before"], "a": "::before"},
            {"q": "Which has the highest specificity?", "o": ["Element selector", "Class selector", "ID selector", "Inline style"], "a": "Inline style"},
            {"q": "When specificity is equal, which rule wins?", "o": ["The first rule", "The shorter rule", "The rule with more properties", "The last rule in the file"], "a": "The last rule in the file"},
            {"q": "What does !important do?", "o": ["Marks a comment", "Loads style first", "Applies to first element only", "Overrides all other declarations regardless of specificity"], "a": "Overrides all other declarations regardless of specificity"},
            {"q": "Which attribute selector matches elements whose href STARTS WITH 'https'?", "o": ["[href='https']", "[href$='https']", "[href*='https']", "[href^='https']"], "a": "[href^='https']"},
            # Colors & Backgrounds (13–22)
            {"q": "Which CSS property sets the text colour?", "o": ["background-color", "font-color", "text-color", "color"], "a": "color"},
            {"q": "What does the 'a' in rgba() stand for?", "o": ["Angle", "Attribute", "Array", "Alpha (opacity)"], "a": "Alpha (opacity)"},
            {"q": "Which colour format uses Hue, Saturation, and Lightness?", "o": ["RGB", "HEX", "RGBA", "HSL"], "a": "HSL"},
            {"q": "Which background-size value covers the container fully (may crop)?", "o": ["contain", "fill", "stretch", "cover"], "a": "cover"},
            {"q": "Which background-size value fits the image inside the container (no crop)?", "o": ["cover", "fill", "fit", "contain"], "a": "contain"},
            {"q": "Which CSS function creates a linear colour gradient?", "o": ["gradient()", "color-gradient()", "background-gradient()", "linear-gradient()"], "a": "linear-gradient()"},
            {"q": "Which CSS function creates a radial gradient?", "o": ["circular-gradient()", "ellipse-gradient()", "round-gradient()", "radial-gradient()"], "a": "radial-gradient()"},
            {"q": "What does opacity: 0 do?", "o": ["Removes from DOM", "display: none equivalent", "Hides with no space taken", "Makes fully transparent but still takes up space"], "a": "Makes fully transparent but still takes up space"},
            {"q": "What is the hex shorthand #F00 equivalent to?", "o": ["#F00000", "#0F0000", "#00FF00", "#FF0000"], "a": "#FF0000"},
            {"q": "Which background-attachment value creates a parallax-like fixed background?", "o": ["local", "scroll", "absolute", "fixed"], "a": "fixed"},
            # Box Model (23–32)
            {"q": "What are the four box model areas from inside out?", "o": ["margin, border, padding, content", "padding, border, margin, content", "content, margin, padding, border", "content, padding, border, margin"], "a": "content, padding, border, margin"},
            {"q": "Which property adds space between content and border?", "o": ["margin", "gap", "border-spacing", "padding"], "a": "padding"},
            {"q": "Which property adds space outside the border?", "o": ["padding", "outer-space", "gap", "margin"], "a": "margin"},
            {"q": "What does box-sizing: border-box do?", "o": ["Adds border to width/height calculation", "Applies box-shadow to border only", "Excludes margin from width", "Makes width/height include padding + border"], "a": "Makes width/height include padding + border"},
            {"q": "What does margin: 0 auto do?", "o": ["Removes all margins", "Centres vertically", "Adds equal padding", "Centres a block element horizontally"], "a": "Centres a block element horizontally"},
            {"q": "What is margin collapsing?", "o": ["Margins set to zero", "Margins added together", "Negative margins cancelling", "Adjacent vertical margins merging to the larger value"], "a": "Adjacent vertical margins merging to the larger value"},
            {"q": "What is the difference between outline and border in the box model?", "o": ["No difference", "Outline is inside; border outside", "Outline takes space; border does not", "Border takes space in layout; outline does not"], "a": "Border takes space in layout; outline does not"},
            {"q": "Which overflow value clips content without a scrollbar?", "o": ["scroll", "auto", "visible", "hidden"], "a": "hidden"},
            {"q": "Which overflow value adds scrollbars only when needed?", "o": ["scroll", "hidden", "clip", "auto"], "a": "auto"},
            {"q": "What total width does an element render at with: width:300px, padding:20px, border:5px (content-box)?", "o": ["300px", "320px", "325px", "350px"], "a": "350px"},
            # Typography (33–42)
            {"q": "Which CSS property sets the typeface?", "o": ["font-type", "font-name", "typeface", "font-family"], "a": "font-family"},
            {"q": "Which unit is relative to the root element's font-size?", "o": ["em", "px", "vw", "rem"], "a": "rem"},
            {"q": "Which font-weight number represents 'bold'?", "o": ["600", "900", "500", "700"], "a": "700"},
            {"q": "Which property sets vertical spacing between lines of text?", "o": ["line-spacing", "vertical-spacing", "text-height", "line-height"], "a": "line-height"},
            {"q": "Which property sets spacing between characters?", "o": ["word-spacing", "char-spacing", "tracking", "letter-spacing"], "a": "letter-spacing"},
            {"q": "Which text-align value stretches text to fill the full line?", "o": ["full", "fill", "stretch", "justify"], "a": "justify"},
            {"q": "Which text-transform value capitalises the first letter of every word?", "o": ["title", "proper", "first-letter", "capitalize"], "a": "capitalize"},
            {"q": "Which CSS at-rule loads a self-hosted custom web font?", "o": ["@import-font", "@load-font", "@web-font", "@font-face"], "a": "@font-face"},
            {"q": "Which property adds a shadow to text?", "o": ["font-shadow", "box-shadow", "drop-shadow", "text-shadow"], "a": "text-shadow"},
            {"q": "Which text-decoration value draws a line through the middle of text?", "o": ["underline", "overline", "strikethrough", "line-through"], "a": "line-through"},
            # Display & Position (43–54)
            {"q": "Which display value removes an element from layout entirely?", "o": ["visibility: hidden", "opacity: 0", "hidden", "none"], "a": "none"},
            {"q": "What is the difference between display:none and visibility:hidden?", "o": ["No difference", "display:none hides but keeps space", "visibility:hidden removes element from layout", "display:none removes element; visibility:hidden hides but keeps space"], "a": "display:none removes element; visibility:hidden hides but keeps space"},
            {"q": "Which position value is the default for all HTML elements?", "o": ["relative", "absolute", "fixed", "static"], "a": "static"},
            {"q": "Which position value offsets from normal position without removing from flow?", "o": ["static", "absolute", "fixed", "relative"], "a": "relative"},
            {"q": "Which position value removes from flow and positions relative to nearest positioned ancestor?", "o": ["fixed", "sticky", "relative", "absolute"], "a": "absolute"},
            {"q": "Which position value stays fixed relative to the viewport when scrolling?", "o": ["absolute", "sticky", "relative", "fixed"], "a": "fixed"},
            {"q": "Which position value acts like relative until a scroll threshold?", "o": ["relative", "absolute", "fixed", "sticky"], "a": "sticky"},
            {"q": "Which property controls stacking order?", "o": ["stack-order", "layer", "depth", "z-index"], "a": "z-index"},
            {"q": "Does z-index work on position: static elements?", "o": ["Yes, always", "Only positive values", "Only negative values", "No"], "a": "No"},
            {"q": "Which display value is the default for <span>?", "o": ["block", "inline-block", "flex", "inline"], "a": "inline"},
            {"q": "Which display value is the default for <div>?", "o": ["inline", "flex", "inline-block", "block"], "a": "block"},
            {"q": "Which display value flows inline but accepts width and height?", "o": ["block", "inline", "flex", "inline-block"], "a": "inline-block"},
            # Flexbox (55–64)
            {"q": "Which CSS value enables Flexbox on a container?", "o": ["display: block", "display: inline", "display: grid", "display: flex"], "a": "display: flex"},
            {"q": "What is the default flex-direction?", "o": ["column", "row-reverse", "column-reverse", "row"], "a": "row"},
            {"q": "Which property aligns items along the MAIN axis?", "o": ["align-items", "align-content", "align-self", "justify-content"], "a": "justify-content"},
            {"q": "Which property aligns items along the CROSS axis?", "o": ["justify-content", "justify-self", "align-content", "align-items"], "a": "align-items"},
            {"q": "Which justify-content value adds equal space between items with no space at edges?", "o": ["space-around", "space-evenly", "center", "space-between"], "a": "space-between"},
            {"q": "What does flex: 1 expand to?", "o": ["flex: 1 0 0", "flex: 1 1 auto", "flex: 0 1 auto", "flex: 1 1 0"], "a": "flex: 1 1 0"},
            {"q": "Which flex item property overrides the container's align-items for one item?", "o": ["justify-self", "self-align", "align-content", "align-self"], "a": "align-self"},
            {"q": "What does flex-shrink: 0 prevent?", "o": ["Item from growing", "Item from being displayed", "Item from wrapping", "Item from shrinking"], "a": "Item from shrinking"},
            {"q": "Which property adds space between flex items?", "o": ["margin", "padding", "spacing", "gap"], "a": "gap"},
            {"q": "To centre content both horizontally and vertically in flex, you need:", "o": ["margin: auto on children", "text-align: center and vertical-align: middle", "position: absolute on children", "justify-content: center and align-items: center"], "a": "justify-content: center and align-items: center"},
            # Grid (65–74)
            {"q": "Which CSS value enables Grid on a container?", "o": ["display: flex", "display: block", "display: table", "display: grid"], "a": "display: grid"},
            {"q": "What does the fr unit represent?", "o": ["Fixed ratio", "Font relative", "Full row width", "A fraction of the available free space"], "a": "A fraction of the available free space"},
            {"q": "What does repeat(4, 1fr) create?", "o": ["4 rows of 1fr", "1fr repeated 4 times = 4 equal columns", "4fr total", "1 column of 4fr"], "a": "1fr repeated 4 times = 4 equal columns"},
            {"q": "What does grid-column: 1 / -1 do?", "o": ["Hides the item", "Places in last column", "Starts at column 1 ends at column -1 (invalid)", "Spans all columns"], "a": "Spans all columns"},
            {"q": "Which property assigns a grid item to a named template area?", "o": ["grid-name", "grid-position", "grid-region", "grid-area"], "a": "grid-area"},
            {"q": "What character represents an empty cell in grid-template-areas?", "o": ["0", "x", "empty", "."], "a": "."},
            {"q": "What does minmax(100px, 1fr) mean?", "o": ["Exactly 100px", "At least 100px, up to 1fr", "At most 100px", "1fr with 100px gap"], "a": "At least 100px, up to 1fr"},
            {"q": "Grid is which type of layout system?", "o": ["1D row", "1D column", "3D", "2D rows and columns"], "a": "2D rows and columns"},
            {"q": "Which property sets the size of implicitly created grid rows?", "o": ["grid-template-rows: auto", "grid-implicit-rows", "grid-row-size", "grid-auto-rows"], "a": "grid-auto-rows"},
            {"q": "What does grid-column: span 2 mean?", "o": ["Place in column 2", "Start at column 2", "Span the item across 2 columns from its current position", "Item takes 2fr"], "a": "Span the item across 2 columns from its current position"},
            # Responsive (75–84)
            {"q": "Which at-rule applies conditional styles based on device/viewport features?", "o": ["@screen", "@breakpoint", "@viewport", "@media"], "a": "@media"},
            {"q": "Which approach writes base styles for mobile and scales up with min-width?", "o": ["Desktop-first", "Viewport-first", "Grid-first", "Mobile-first"], "a": "Mobile-first"},
            {"q": "Which CSS unit is 1% of viewport width?", "o": ["vh", "vmin", "vmax", "vw"], "a": "vw"},
            {"q": "Which CSS unit is 1% of viewport height?", "o": ["vw", "vmin", "vmax", "vh"], "a": "vh"},
            {"q": "How do you declare a CSS variable --accent-color as red?", "o": ["$accent-color: red", "var(--accent-color): red", "set --accent-color: red", "--accent-color: red inside :root"], "a": "--accent-color: red inside :root"},
            {"q": "How do you use a CSS variable named --accent-color?", "o": ["$accent-color", "--accent-color", "variable(--accent-color)", "var(--accent-color)"], "a": "var(--accent-color)"},
            {"q": "What does clamp(1rem, 3vw, 2rem) ensure?", "o": ["Font size is always 3vw", "Font size is always between 1rem and 2rem with 3vw preference", "Font size is 2rem on mobile", "Font size is 1rem on desktop"], "a": "Font size is always between 1rem and 2rem with 3vw preference"},
            {"q": "Which CSS function allows mixing different units like calc(100% - 2rem)?", "o": ["mix()", "compute()", "convert()", "calc()"], "a": "calc()"},
            {"q": "Which media feature applies styles when the device is in portrait orientation?", "o": ["orientation: vertical", "orientation: upright", "orientation: landscape", "orientation: portrait"], "a": "orientation: portrait"},
            {"q": "Which media feature detects user preference for dark mode?", "o": ["prefers-theme: dark", "color-scheme: dark", "prefers-dark-mode: true", "prefers-color-scheme: dark"], "a": "prefers-color-scheme: dark"},
            # Transitions, Animations & Transforms (85–100)
            {"q": "Which property creates a smooth state-change animation (e.g. on :hover)?", "o": ["animation", "keyframe", "motion", "transition"], "a": "transition"},
            {"q": "Which timing function results in constant speed throughout?", "o": ["ease", "ease-in", "ease-out", "linear"], "a": "linear"},
            {"q": "Which CSS property applies transformations to an element?", "o": ["translate", "motion", "move", "transform"], "a": "transform"},
            {"q": "Which transform function moves an element?", "o": ["rotate()", "scale()", "skew()", "translate()"], "a": "translate()"},
            {"q": "Which transform function rotates an element?", "o": ["turn()", "skew()", "translate()", "rotate()"], "a": "rotate()"},
            {"q": "What does transform: scale(0.5) do?", "o": ["Moves element 0.5px", "Doubles element size", "Rotates 0.5 degrees", "Halves the element's size"], "a": "Halves the element's size"},
            {"q": "Which at-rule defines CSS keyframe animations?", "o": ["@animation", "@transition", "@motion", "@keyframes"], "a": "@keyframes"},
            {"q": "Which animation-iteration-count value loops an animation forever?", "o": ["forever", "loop", "repeat", "infinite"], "a": "infinite"},
            {"q": "Which animation-fill-mode keeps the final keyframe state after completion?", "o": ["both", "backwards", "end", "forwards"], "a": "forwards"},
            {"q": "Which animation property pauses or plays an animation?", "o": ["animation-state", "animation-control", "animation-status", "animation-play-state"], "a": "animation-play-state"},
            {"q": "What is the key difference between a transition and an animation?", "o": ["They are identical", "Transitions are JS-only; animations CSS-only", "Animations require a trigger; transitions run automatically", "Transitions require a trigger (state change); animations can run automatically"], "a": "Transitions require a trigger (state change); animations can run automatically"},
            {"q": "What does transform-origin control?", "o": ["The starting position of translate", "The speed of a transform", "Perspective depth", "The fixed point around which transforms are applied"], "a": "The fixed point around which transforms are applied"},
            {"q": "Which animation-direction value alternates the animation forward and backward on each cycle?", "o": ["reverse", "loop", "back-forward", "alternate"], "a": "alternate"},
            {"q": "What does will-change: transform tell the browser?", "o": ["Disable transitions", "The transform never changes", "Apply transform on load", "Pre-optimise for upcoming transform changes (GPU layer)"], "a": "Pre-optimise for upcoming transform changes (GPU layer)"},
            {"q": "When multiple transforms are chained, in what order are they applied?", "o": ["Left to right", "Randomly", "Simultaneously", "Right to left"], "a": "Right to left"},
            {"q": "Which property on a PARENT element sets the depth for 3D child transforms?", "o": ["depth", "3d-view", "perspective-origin", "perspective"], "a": "perspective"},
        ],
    },
]


class Command(BaseCommand):
    help = "Create a detailed Introduction to CSS course: 9 content lessons each with a 20-question quiz, plus a 100-question final review."

    def handle(self, *args, **options):
        tutor = User.objects.filter(role="tutor").first()
        if not tutor:
            self.stdout.write(self.style.ERROR("No tutor found. Run create_sample_users first."))
            return
        self.stdout.write(f"Using tutor: {tutor.email}")

        category, _ = Category.objects.get_or_create(
            name="Web Development",
            defaults={"description": "Web technologies including HTML, CSS, and JavaScript", "color": "#F97316"},
        )

        course, created = Course.objects.get_or_create(
            title="Introduction to CSS — Complete Beginner Course",
            instructor=tutor,
            defaults={
                "description": (
                    "A comprehensive, lesson-by-lesson introduction to CSS. "
                    "Starting from selectors and specificity, you will progress through colors, the box model, "
                    "typography, positioning, Flexbox, CSS Grid, responsive design with media queries, "
                    "and finally transitions and animations. "
                    "Each of the 9 content lessons is followed by a 20-question quiz, "
                    "and the course concludes with a 100-question comprehensive final assessment."
                ),
                "short_description": "Master CSS from scratch — 9 detailed lessons, 9 quizzes, and a 100-question final exam.",
                "category": category,
                "price": 0.00,
                "is_free": True,
                "difficulty": "beginner",
                "duration_hours": 7,
                "language": "English",
                "status": "published",
            },
        )
        action = "Created" if created else "Found existing"
        self.stdout.write(self.style.SUCCESS(f"{action} course: {course.title}"))

        total_questions_created = 0

        for lesson_data in LESSONS:
            lesson, lesson_created = Lesson.objects.get_or_create(
                course=course,
                order=lesson_data["order"],
                defaults={
                    "title": lesson_data["title"],
                    "description": lesson_data["description"],
                    "lesson_type": "text",
                    "content": to_html_content(lesson_data["content"]),
                    "duration_minutes": lesson_data["duration_minutes"],
                    "is_published": True,
                },
            )
            lesson_action = "Created" if lesson_created else "Found"
            self.stdout.write(f"  {lesson_action} lesson {lesson_data['order']}: {lesson_data['title']}")

            quiz, _ = Quiz.objects.get_or_create(
                lesson=lesson,
                defaults={
                    "title": lesson_data["quiz_title"],
                    "description": lesson_data["quiz_description"],
                    "time_limit_minutes": lesson_data["time_limit"],
                    "passing_score": 70,
                    "max_attempts": 3,
                    "is_published": True,
                },
            )

            existing_q_count = quiz.questions.count()
            expected_q_count = len(lesson_data["questions"])

            if existing_q_count >= expected_q_count:
                self.stdout.write(f"    Quiz already has {existing_q_count} questions — skipping.")
                continue

            quiz.questions.all().delete()

            for i, q in enumerate(lesson_data["questions"], start=1):
                QuizQuestion.objects.create(
                    quiz=quiz,
                    question_text=q["q"],
                    question_type="multiple_choice",
                    order=i,
                    points=1,
                    options=q["o"],
                    correct_answer=q["a"],
                )
            total_questions_created += expected_q_count
            self.stdout.write(self.style.SUCCESS(f"    Added {expected_q_count} questions to: {lesson_data['quiz_title']}"))

        self.stdout.write(self.style.SUCCESS(
            f"\n{'='*60}\n"
            f"  Course   : {course.title}\n"
            f"  Lessons  : {len(LESSONS)} (9 content + 1 final review)\n"
            f"  Quizzes  : {len(LESSONS)} (20 questions each for lessons 1–9, 100 for final)\n"
            f"  Questions: {total_questions_created} total created this run\n"
            f"  Price    : FREE\n"
            f"  Status   : Published\n"
            f"{'='*60}"
        ))
