from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Category, Course, Lesson, Quiz, QuizQuestion

User = get_user_model()

LESSONS = [
    {
        "order": 1,
        "title": "HTML Document Structure & Basics",
        "description": "Learn the anatomy of an HTML document: DOCTYPE, root element, head, body, meta tags, comments, and how browsers parse HTML.",
        "duration_minutes": 30,
        "content": """Welcome to Lesson 1: HTML Document Structure & Basics

Every web page you visit is built with HTML. In this lesson you will learn the skeleton that every HTML document must follow.

─── THE DOCTYPE DECLARATION ───────────────────────────────────────────────────
Every HTML file must begin with a DOCTYPE declaration:
    <!DOCTYPE html>
This single line tells the browser to render the page in standards-compliant HTML5 mode.

─── THE ROOT ELEMENT ──────────────────────────────────────────────────────────
The <html> element wraps the entire document. The lang attribute specifies the human language:
    <html lang="en">

─── HEAD vs BODY ──────────────────────────────────────────────────────────────
• <head> — contains metadata (not visible to the user):
    - <title>       → the text in the browser tab
    - <meta>        → character set, viewport, description, keywords
    - <link>        → external CSS stylesheets
    - <script>      → JavaScript (better placed at end of <body>)
    - <style>       → embedded CSS

• <body> — contains everything the user sees.

─── META TAGS ─────────────────────────────────────────────────────────────────
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Page summary for search engines">

─── HTML COMMENTS ─────────────────────────────────────────────────────────────
    <!-- This is a comment and will not be displayed in the browser -->

─── VOID (SELF-CLOSING) ELEMENTS ──────────────────────────────────────────────
Some elements have no content and no closing tag:
    <br>  <hr>  <img>  <input>  <link>  <meta>

─── BLOCK vs INLINE ───────────────────────────────────────────────────────────
Block elements start on a new line and take full width:  <div>, <p>, <h1>–<h6>
Inline elements flow within text:  <span>, <a>, <strong>, <em>

─── MINIMAL VALID HTML5 PAGE ──────────────────────────────────────────────────
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Page</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
    </body>
    </html>
""",
        "quiz_title": "Quiz 1 — HTML Document Structure & Basics",
        "quiz_description": "20 questions covering DOCTYPE, html/head/body, meta tags, comments, void elements, and document anatomy.",
        "time_limit": 20,
        "questions": [
            {"q": "What does HTML stand for?", "o": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"], "a": "Hyper Text Markup Language"},
            {"q": "Which declaration must appear at the very top of an HTML5 document?", "o": ["<!DOCTYPE html>", "<html>", "<head>", "<!-- HTML5 -->"], "a": "<!DOCTYPE html>"},
            {"q": "What is the root element of an HTML page?", "o": ["<root>", "<body>", "<head>", "<html>"], "a": "<html>"},
            {"q": "Which element contains metadata about the HTML document (not visible to the user)?", "o": ["<meta>", "<data>", "<head>", "<info>"], "a": "<head>"},
            {"q": "Which element contains the visible page content?", "o": ["<main>", "<content>", "<html>", "<body>"], "a": "<body>"},
            {"q": "What does <!DOCTYPE html> tell the browser?", "o": ["The page uses CSS3", "The document is HTML5", "Load JavaScript first", "Use strict XML parsing"], "a": "The document is HTML5"},
            {"q": "Which tag sets the title shown in the browser tab?", "o": ["<heading>", "<caption>", "<title>", "<label>"], "a": "<title>"},
            {"q": "What is the correct HTML syntax for a comment?", "o": ["// This is a comment", "/* This is a comment */", "<!-- This is a comment -->", "## This is a comment"], "a": "<!-- This is a comment -->"},
            {"q": "Which meta tag specifies the character encoding of the document?", "o": ["<meta charset=\"UTF-8\">", "<meta encoding=\"UTF-8\">", "<meta lang=\"UTF-8\">", "<meta type=\"UTF-8\">"], "a": "<meta charset=\"UTF-8\">"},
            {"q": "HTML elements with no closing tag are called?", "o": ["Solo tags", "Self-elements", "Block elements", "Void elements"], "a": "Void elements"},
            {"q": "Where should the <script> tag be placed for best page-load performance?", "o": ["Inside <head>", "Before </body>", "After <html>", "Inside <meta>"], "a": "Before </body>"},
            {"q": "What does the lang attribute on <html> specify?", "o": ["The programming language used", "The human language of the page content", "The browser rendering language", "The HTML version"], "a": "The human language of the page content"},
            {"q": "Which element groups block-level content with no semantic meaning?", "o": ["<span>", "<section>", "<div>", "<main>"], "a": "<div>"},
            {"q": "Which element groups inline content with no semantic meaning?", "o": ["<div>", "<span>", "<p>", "<inline>"], "a": "<span>"},
            {"q": "Which tag links an external CSS stylesheet inside the <head>?", "o": ["<style>", "<css>", "<link>", "<stylesheet>"], "a": "<link>"},
            {"q": "What is the viewport meta tag primarily used for?", "o": ["Setting page background color", "Responsive web design on mobile devices", "Adding page keywords for SEO", "Linking stylesheets"], "a": "Responsive web design on mobile devices"},
            {"q": "Void elements in HTML5 cannot have which of the following?", "o": ["Attributes", "A closing tag", "An id attribute", "Inline styles"], "a": "A closing tag"},
            {"q": "Which attribute provides a tooltip when hovering over any HTML element?", "o": ["alt", "hint", "tooltip", "title"], "a": "title"},
            {"q": "Which HTML element embeds another HTML page within the current page?", "o": ["<embed>", "<frame>", "<iframe>", "<include>"], "a": "<iframe>"},
            {"q": "What is the purpose of <meta name=\"description\">?", "o": ["Style the page", "Set the favicon", "Provide a page summary for search engines", "Define the page title"], "a": "Provide a page summary for search engines"},
        ],
    },
    {
        "order": 2,
        "title": "Text Content — Headings, Paragraphs & Formatting",
        "description": "Master HTML text elements: headings (h1–h6), paragraphs, line breaks, horizontal rules, strong, em, mark, sub, sup, blockquote, pre, code, and more.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 2: Text Content — Headings, Paragraphs & Formatting

HTML provides a rich set of text elements to structure and style content meaningfully.

─── HEADINGS ──────────────────────────────────────────────────────────────────
HTML has six levels of headings, from most important to least:
    <h1> — main page title (use only once per page for SEO)
    <h2> — major sections
    <h3> — sub-sections
    <h4>, <h5>, <h6> — deeper nesting

─── PARAGRAPHS & BREAKS ───────────────────────────────────────────────────────
    <p>This is a paragraph.</p>
    Line break (void):  <br>
    Horizontal rule:    <hr>

─── SEMANTIC TEXT FORMATTING ──────────────────────────────────────────────────
    <strong>  — bold + semantically important
    <em>      — italic + semantically emphasized
    <b>       — bold (visual only, no added meaning)
    <i>       — italic (visual only: technical terms, foreign words)
    <u>       — underline
    <s>       — strikethrough (no longer accurate/relevant)
    <del>     — deleted text (document editing context)
    <ins>     — inserted text (document editing context)
    <mark>    — highlighted / relevant text
    <small>   — fine print / side comments
    <sup>     — superscript  (e.g. x²)
    <sub>     — subscript    (e.g. H₂O)

─── QUOTATIONS ────────────────────────────────────────────────────────────────
    <blockquote cite="url"> — long block quotation
    <q>                     — short inline quotation (adds quotation marks)
    <cite>                  — title of a work (book, film, article)

─── PREFORMATTED & CODE ───────────────────────────────────────────────────────
    <pre>   — preserves whitespace and line breaks (monospace)
    <code>  — inline code snippet
    <kbd>   — keyboard input
    <samp>  — sample output
    <var>   — variable in math or programming

─── ABBREVIATIONS ─────────────────────────────────────────────────────────────
    <abbr title="HyperText Markup Language">HTML</abbr>
""",
        "quiz_title": "Quiz 2 — Text Content & Formatting",
        "quiz_description": "20 questions on headings, paragraphs, semantic text elements, quotations, and preformatted content.",
        "time_limit": 20,
        "questions": [
            {"q": "How many heading levels does HTML provide?", "o": ["3", "4", "5", "6"], "a": "6"},
            {"q": "Which heading tag creates the largest (most important) heading?", "o": ["<h6>", "<h3>", "<h1>", "<heading>"], "a": "<h1>"},
            {"q": "Which heading tag creates the smallest heading?", "o": ["<h1>", "<h4>", "<h5>", "<h6>"], "a": "<h6>"},
            {"q": "Which tag defines a paragraph?", "o": ["<para>", "<pg>", "<p>", "<text>"], "a": "<p>"},
            {"q": "Which tag inserts a single line break?", "o": ["<lb>", "<newline>", "<br>", "<break>"], "a": "<br>"},
            {"q": "Which tag creates a thematic horizontal dividing line?", "o": ["<line>", "<divider>", "<rule>", "<hr>"], "a": "<hr>"},
            {"q": "Which element marks text as bold AND semantically important?", "o": ["<b>", "<bold>", "<strong>", "<i>"], "a": "<strong>"},
            {"q": "Which element marks text as italic AND semantically emphasized?", "o": ["<i>", "<em>", "<italic>", "<b>"], "a": "<em>"},
            {"q": "What is the key difference between <b> and <strong>?", "o": ["No difference", "<b> is visual only; <strong> adds semantic importance", "<strong> is deprecated in HTML5", "<b> adds semantic importance; <strong> is visual"], "a": "<b> is visual only; <strong> adds semantic importance"},
            {"q": "Which tag renders text with a strikethrough to indicate it is no longer accurate?", "o": ["<strike>", "<del>", "<s>", "<cross>"], "a": "<s>"},
            {"q": "Which tag marks deleted text in a document-editing context?", "o": ["<s>", "<removed>", "<del>", "<strike>"], "a": "<del>"},
            {"q": "Which tag highlights text to indicate relevance?", "o": ["<highlight>", "<mark>", "<yellow>", "<span>"], "a": "<mark>"},
            {"q": "Which tag renders text as superscript (e.g. x²)?", "o": ["<super>", "<up>", "<top>", "<sup>"], "a": "<sup>"},
            {"q": "Which tag renders text as subscript (e.g. H₂O)?", "o": ["<sub>", "<down>", "<low>", "<bottom>"], "a": "<sub>"},
            {"q": "Which element is used for a long block quotation?", "o": ["<quote>", "<cite>", "<blockquote>", "<q>"], "a": "<blockquote>"},
            {"q": "Which element is used for a short inline quotation?", "o": ["<blockquote>", "<quote>", "<q>", "<cite>"], "a": "<q>"},
            {"q": "Which element preserves whitespace and line breaks in monospace font?", "o": ["<text>", "<raw>", "<mono>", "<pre>"], "a": "<pre>"},
            {"q": "Which element displays an inline code snippet?", "o": ["<pre>", "<snippet>", "<code>", "<kbd>"], "a": "<code>"},
            {"q": "Which element represents keyboard input?", "o": ["<input>", "<key>", "<kbd>", "<type>"], "a": "<kbd>"},
            {"q": "Which element is used to define an abbreviation with its full form?", "o": ["<short>", "<abbr>", "<acronym>", "<title>"], "a": "<abbr>"},
        ],
    },
    {
        "order": 3,
        "title": "Links, Anchors & Navigation",
        "description": "Understand how to create hyperlinks, anchor links, email/phone links, downloadable links, and accessible navigation with the <nav> element.",
        "duration_minutes": 30,
        "content": """Welcome to Lesson 3: Links, Anchors & Navigation

Links are the foundation of the web. The anchor element <a> connects pages and resources.

─── BASIC HYPERLINK ───────────────────────────────────────────────────────────
    <a href="https://example.com">Visit Example</a>

─── OPEN IN NEW TAB ───────────────────────────────────────────────────────────
    <a href="https://example.com" target="_blank" rel="noopener noreferrer">
        Open in new tab
    </a>
    Always add rel="noopener noreferrer" with target="_blank" for security.

─── TARGET VALUES ─────────────────────────────────────────────────────────────
    _self    — same tab (default)
    _blank   — new tab / window
    _parent  — parent frame
    _top     — full window

─── EMAIL & PHONE LINKS ───────────────────────────────────────────────────────
    <a href="mailto:user@example.com">Email us</a>
    <a href="tel:+2348012345678">Call us</a>

─── ANCHOR / JUMP LINKS ───────────────────────────────────────────────────────
Link to a specific section using the element's id:
    <a href="#section2">Go to Section 2</a>
    ...
    <h2 id="section2">Section 2</h2>

─── DOWNLOADABLE LINKS ────────────────────────────────────────────────────────
    <a href="report.pdf" download>Download Report</a>
    The download attribute can optionally set the filename:
    <a href="img.png" download="my-photo.png">Download</a>

─── RELATIVE vs ABSOLUTE URLS ─────────────────────────────────────────────────
    Absolute:  https://example.com/about.html
    Relative:  about.html  or  ../images/logo.png

─── NAVIGATION ELEMENT ────────────────────────────────────────────────────────
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
    </nav>

─── SECURITY: rel ATTRIBUTE ───────────────────────────────────────────────────
    rel="nofollow"          — tell search engines not to follow the link
    rel="noopener noreferrer" — prevent tab-napping attacks on _blank links
    rel="external"          — indicates an external link
""",
        "quiz_title": "Quiz 3 — Links, Anchors & Navigation",
        "quiz_description": "20 questions on hyperlinks, target values, email/phone links, anchor IDs, download, and security attributes.",
        "time_limit": 20,
        "questions": [
            {"q": "Which tag creates a hyperlink in HTML?", "o": ["<link>", "<href>", "<url>", "<a>"], "a": "<a>"},
            {"q": "Which attribute specifies the destination URL of a hyperlink?", "o": ["src", "url", "href", "link"], "a": "href"},
            {"q": "Which target attribute value opens a link in a new browser tab?", "o": ["target=\"_new\"", "target=\"_blank\"", "target=\"_tab\"", "target=\"_window\""], "a": "target=\"_blank\""},
            {"q": "Which target attribute value keeps the link in the same tab (the default)?", "o": ["_same", "_self", "_current", "_default"], "a": "_self"},
            {"q": "How do you create an email link in HTML?", "o": ["<a href=\"email:user@ex.com\">", "<a href=\"send:user@ex.com\">", "<a href=\"mailto:user@ex.com\">", "<a href=\"mail:user@ex.com\">"], "a": "<a href=\"mailto:user@ex.com\">"},
            {"q": "How do you create a phone call link in HTML?", "o": ["<a href=\"phone:+123\">", "<a href=\"call:+123\">", "<a href=\"tel:+123\">", "<a href=\"dial:+123\">"], "a": "<a href=\"tel:+123\">"},
            {"q": "How do you link to a section with id=\"about\" on the same page?", "o": ["href=\"about\"", "href=\"@about\"", "href=\"#about\"", "href=\"*about\""], "a": "href=\"#about\""},
            {"q": "Which attribute makes a link trigger a file download?", "o": ["save", "export", "download", "file"], "a": "download"},
            {"q": "Which HTML element defines a block of navigation links?", "o": ["<menu>", "<links>", "<navigate>", "<nav>"], "a": "<nav>"},
            {"q": "What security attribute should always accompany target=\"_blank\"?", "o": ["rel=\"nofollow\"", "rel=\"noopener noreferrer\"", "rel=\"external\"", "rel=\"unsafe\""], "a": "rel=\"noopener noreferrer\""},
            {"q": "What is an absolute URL?", "o": ["A URL relative to the current page", "A root-relative URL starting with /", "A complete URL including protocol and domain", "A URL with no path"], "a": "A complete URL including protocol and domain"},
            {"q": "What is a relative URL?", "o": ["A URL that includes the full domain", "A URL defined relative to the current page location", "A URL with a protocol", "A URL pointing only to external sites"], "a": "A URL defined relative to the current page location"},
            {"q": "Which rel value tells search engines not to follow a link?", "o": ["rel=\"noindex\"", "rel=\"nofollow\"", "rel=\"nopass\"", "rel=\"ignore\""], "a": "rel=\"nofollow\""},
            {"q": "Which attribute on <a> specifies the language of the linked document?", "o": ["lang", "language", "hreflang", "locale"], "a": "hreflang"},
            {"q": "What does href=\"#\" do?", "o": ["Links to the homepage", "Scrolls to the top of the current page", "Creates a new anchor point", "Opens a new tab"], "a": "Scrolls to the top of the current page"},
            {"q": "How do you create a named anchor bookmark without a visible link?", "o": ["<anchor id=\"name\">", "<bookmark id=\"name\">", "Any element with an id attribute", "<a name=\"name\"> only"], "a": "Any element with an id attribute"},
            {"q": "What is the purpose of the title attribute on a link?", "o": ["Defines the link text", "Provides a tooltip / extra information on hover", "Sets the browser tab title", "Controls link behavior"], "a": "Provides a tooltip / extra information on hover"},
            {"q": "Which element defines a clickable area within an image map?", "o": ["<map>", "<zone>", "<region>", "<area>"], "a": "<area>"},
            {"q": "Which attribute on <img> connects it to a <map> element?", "o": ["map", "usemap", "mapref", "mapid"], "a": "usemap"},
            {"q": "Which attribute on <a> describes the relationship between the current and linked document?", "o": ["type", "rev", "rel", "href"], "a": "rel"},
        ],
    },
    {
        "order": 4,
        "title": "Images, Figures & Responsive Images",
        "description": "Learn to embed images with <img>, add captions with <figure>/<figcaption>, serve responsive images with <picture> and srcset, and understand image formats.",
        "duration_minutes": 30,
        "content": """Welcome to Lesson 4: Images, Figures & Responsive Images

Images make the web visual. HTML provides powerful tools to embed and optimize them.

─── BASIC IMAGE ───────────────────────────────────────────────────────────────
    <img src="photo.jpg" alt="A beautiful sunset" width="800" height="600">

Key attributes:
    src    — file path or URL of the image (required)
    alt    — alternative text (required for accessibility & SEO)
    width  — image width in pixels
    height — image height in pixels

─── WHY alt IS IMPORTANT ──────────────────────────────────────────────────────
• Screen readers read the alt text to visually impaired users
• Displayed when the image fails to load
• Indexed by search engines

─── FIGURE & FIGCAPTION ───────────────────────────────────────────────────────
    <figure>
        <img src="chart.png" alt="Sales chart">
        <figcaption>Figure 1: Monthly sales data</figcaption>
    </figure>

─── LAZY LOADING ──────────────────────────────────────────────────────────────
    <img src="large.jpg" alt="..." loading="lazy">
    The browser only loads the image when it approaches the viewport.

─── RESPONSIVE IMAGES WITH srcset ─────────────────────────────────────────────
    <img src="small.jpg"
         srcset="small.jpg 480w, medium.jpg 800w, large.jpg 1200w"
         sizes="(max-width: 600px) 480px, 800px"
         alt="Responsive image">

─── THE <picture> ELEMENT ─────────────────────────────────────────────────────
Serve different images based on screen size or format support:
    <picture>
        <source media="(max-width: 600px)" srcset="mobile.jpg">
        <source media="(max-width: 1200px)" srcset="tablet.jpg">
        <img src="desktop.jpg" alt="Team photo">
    </picture>

─── IMAGE FORMATS ─────────────────────────────────────────────────────────────
    JPEG/JPG — photos, complex images (lossy compression)
    PNG      — images needing transparency (lossless)
    GIF      — simple animations, limited colors
    SVG      — vector graphics (scalable, resolution-independent)
    WebP     — modern format: smaller size, supports transparency & animation

─── IMAGE MAPS ────────────────────────────────────────────────────────────────
    <img src="map.jpg" alt="World map" usemap="#worldmap">
    <map name="worldmap">
        <area shape="rect" coords="0,0,200,100" href="africa.html" alt="Africa">
        <area shape="circle" coords="300,150,50" href="europe.html" alt="Europe">
        <area shape="poly" coords="..." href="asia.html" alt="Asia">
    </map>
""",
        "quiz_title": "Quiz 4 — Images, Figures & Responsive Images",
        "quiz_description": "20 questions on img attributes, alt text, figure, picture, srcset, lazy loading, image formats, and image maps.",
        "time_limit": 20,
        "questions": [
            {"q": "Which tag is used to display an image in HTML?", "o": ["<image>", "<picture>", "<photo>", "<img>"], "a": "<img>"},
            {"q": "Which attribute specifies the image file path or URL?", "o": ["href", "url", "path", "src"], "a": "src"},
            {"q": "Which attribute provides alternative text for an image?", "o": ["title", "caption", "description", "alt"], "a": "alt"},
            {"q": "Why is the alt attribute important?", "o": ["It improves image resolution", "It provides accessibility for screen readers and SEO", "It is required to apply CSS styles", "It sets image dimensions"], "a": "It provides accessibility for screen readers and SEO"},
            {"q": "Which HTML5 element wraps an image together with its caption?", "o": ["<imgcaption>", "<figure>", "<gallery>", "<section>"], "a": "<figure>"},
            {"q": "Which element defines the caption for a <figure>?", "o": ["<caption>", "<label>", "<figcaption>", "<description>"], "a": "<figcaption>"},
            {"q": "What does loading=\"lazy\" do on an <img> element?", "o": ["Loads the image immediately at page load", "Delays loading until the image is near the viewport", "Reduces image file size", "Disables the image on mobile"], "a": "Delays loading until the image is near the viewport"},
            {"q": "What is the purpose of the <picture> element?", "o": ["Display multiple images simultaneously", "Provide responsive image sources for different screens/formats", "Replace the <img> tag entirely", "Create an image slideshow"], "a": "Provide responsive image sources for different screens/formats"},
            {"q": "Which tag inside <picture> defines a conditional image source?", "o": ["<img>", "<source>", "<media>", "<option>"], "a": "<source>"},
            {"q": "Which attribute on <img> provides multiple image sources for different viewport sizes?", "o": ["sources", "responsive", "srcset", "mediasrc"], "a": "srcset"},
            {"q": "Which image format is best suited for photographs?", "o": ["BMP", "TIFF", "JPEG/JPG", "SVG"], "a": "JPEG/JPG"},
            {"q": "Which image format supports transparency?", "o": ["JPG", "BMP", "TIFF", "PNG"], "a": "PNG"},
            {"q": "Which image format supports simple animation?", "o": ["PNG", "JPG", "SVG", "GIF"], "a": "GIF"},
            {"q": "Which image format is vector-based and fully scalable?", "o": ["PNG", "GIF", "JPG", "SVG"], "a": "SVG"},
            {"q": "Which modern image format offers smaller file sizes with transparency and animation support?", "o": ["TIFF", "BMP", "WebP", "ICO"], "a": "WebP"},
            {"q": "Which area shape value creates a rectangular clickable region in an image map?", "o": ["square", "rectangle", "box", "rect"], "a": "rect"},
            {"q": "Which area shape value creates a circular clickable region in an image map?", "o": ["round", "oval", "sphere", "circle"], "a": "circle"},
            {"q": "Which attribute on <img> connects it to its <map> element?", "o": ["map", "usemap", "mapref", "mapid"], "a": "usemap"},
            {"q": "What happens when an image fails to load and has no alt text?", "o": ["The page crashes", "A broken image icon is shown with no description", "The next image is shown instead", "The image is hidden automatically"], "a": "A broken image icon is shown with no description"},
            {"q": "Which attribute defines the intrinsic width of an image in pixels?", "o": ["size", "w", "width", "dimension"], "a": "width"},
        ],
    },
    {
        "order": 5,
        "title": "Lists — Ordered, Unordered & Description Lists",
        "description": "Create ordered lists, unordered lists, description lists, nested lists, and customise list markers and numbering.",
        "duration_minutes": 25,
        "content": """Welcome to Lesson 5: Lists — Ordered, Unordered & Description Lists

HTML provides three types of lists for organising content.

─── UNORDERED LIST ────────────────────────────────────────────────────────────
Uses bullet points. Default bullet: disc.
    <ul>
        <li>HTML</li>
        <li>CSS</li>
        <li>JavaScript</li>
    </ul>

─── ORDERED LIST ──────────────────────────────────────────────────────────────
Uses numbers or letters.
    <ol>
        <li>Learn HTML</li>
        <li>Learn CSS</li>
        <li>Build a project</li>
    </ol>

Attributes on <ol>:
    type="1"  — decimal numbers (default)
    type="A"  — uppercase letters
    type="a"  — lowercase letters
    type="I"  — uppercase Roman numerals
    type="i"  — lowercase Roman numerals
    start="5" — start counting from 5
    reversed  — count downward

─── LIST ITEM VALUE ───────────────────────────────────────────────────────────
Override a specific item's number:
    <li value="10">This item is numbered 10</li>

─── DESCRIPTION LIST ──────────────────────────────────────────────────────────
Term–definition pairs:
    <dl>
        <dt>HTML</dt>
        <dd>HyperText Markup Language — the structure of the web</dd>
        <dt>CSS</dt>
        <dd>Cascading Style Sheets — the styling of the web</dd>
    </dl>

─── NESTED LISTS ──────────────────────────────────────────────────────────────
Any list can be nested inside a <li>:
    <ul>
        <li>Frontend
            <ul>
                <li>HTML</li>
                <li>CSS</li>
            </ul>
        </li>
    </ul>

─── REMOVING DEFAULT STYLES ───────────────────────────────────────────────────
    <ul style="list-style-type: none; padding: 0;">
""",
        "quiz_title": "Quiz 5 — Lists",
        "quiz_description": "20 questions covering unordered lists, ordered lists, description lists, nested lists, and list attributes.",
        "time_limit": 20,
        "questions": [
            {"q": "Which tag creates an unordered (bulleted) list?", "o": ["<ol>", "<dl>", "<list>", "<ul>"], "a": "<ul>"},
            {"q": "Which tag creates an ordered (numbered) list?", "o": ["<ul>", "<list>", "<numbered>", "<ol>"], "a": "<ol>"},
            {"q": "Which tag defines each item inside an ordered or unordered list?", "o": ["<item>", "<it>", "<entry>", "<li>"], "a": "<li>"},
            {"q": "What is the default bullet style for an unordered list?", "o": ["Square", "Circle", "Diamond", "Disc"], "a": "Disc"},
            {"q": "What is the default numbering style for an ordered list?", "o": ["Roman numerals", "Letters", "Decimal numbers", "Hexadecimal"], "a": "Decimal numbers"},
            {"q": "Which attribute changes the numbering type of an <ol>?", "o": ["style", "numbering", "format", "type"], "a": "type"},
            {"q": "Which attribute sets the starting number of an <ol>?", "o": ["begin", "from", "start", "first"], "a": "start"},
            {"q": "Which list type is used for term–definition pairs?", "o": ["<ul>", "<ol>", "<tl>", "<dl>"], "a": "<dl>"},
            {"q": "Which tag defines a term in a description list?", "o": ["<term>", "<dt>", "<dd>", "<key>"], "a": "<dt>"},
            {"q": "Which tag defines the description in a description list?", "o": ["<definition>", "<dt>", "<desc>", "<dd>"], "a": "<dd>"},
            {"q": "Can lists be nested inside each other in HTML?", "o": ["No, lists cannot be nested", "Only <ol> inside <ul>", "Only <ul> inside <ol>", "Yes, any list can be nested inside another list item"], "a": "Yes, any list can be nested inside another list item"},
            {"q": "Where must <li> elements be placed?", "o": ["Anywhere in the HTML", "Inside <ul> or <ol> only", "Inside <dl> only", "Inside any block element"], "a": "Inside <ul> or <ol> only"},
            {"q": "Which type value for <ol> produces uppercase letters (A, B, C...)?", "o": ["type=\"uppercase\"", "type=\"ABC\"", "type=\"A\"", "type=\"alpha\""], "a": "type=\"A\""},
            {"q": "Which type value for <ol> produces lowercase Roman numerals?", "o": ["type=\"roman\"", "type=\"lower-roman\"", "type=\"lr\"", "type=\"i\""], "a": "type=\"i\""},
            {"q": "Which attribute on <ol> reverses the counting order (counts down)?", "o": ["descending", "countdown", "reversed", "backwards"], "a": "reversed"},
            {"q": "Can a single <dt> element have multiple <dd> elements?", "o": ["No, only one <dd> per <dt>", "Yes, one term can have multiple descriptions", "Only in HTML5", "Only when nested"], "a": "Yes, one term can have multiple descriptions"},
            {"q": "Which CSS property removes the default list bullet or number marker?", "o": ["bullet-style: none", "marker-type: none", "list-style-type: none", "list-bullet: none"], "a": "list-style-type: none"},
            {"q": "What does the value attribute on <li> do in an ordered list?", "o": ["Sets the item's CSS class", "Overrides the number of that specific item", "Sets a tooltip text", "Defines item priority"], "a": "Overrides the number of that specific item"},
            {"q": "Which type value for <ol> produces uppercase Roman numerals?", "o": ["type=\"ROMAN\"", "type=\"R\"", "type=\"I\"", "type=\"upper-roman\""], "a": "type=\"I\""},
            {"q": "Which HTML element represents a menu of commands or a toolbar?", "o": ["<nav>", "<commandlist>", "<toolbar>", "<menu>"], "a": "<menu>"},
        ],
    },
    {
        "order": 6,
        "title": "Tables — Structure, Spanning & Accessibility",
        "description": "Build structured HTML tables using table, thead, tbody, tfoot, th, td, tr; span cells with colspan/rowspan; group columns with colgroup; and write accessible tables.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 6: Tables — Structure, Spanning & Accessibility

HTML tables organise data into rows and columns. They should be used for tabular data only — never for page layout.

─── BASIC TABLE STRUCTURE ─────────────────────────────────────────────────────
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Age</th>
                <th>City</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Alice</td>
                <td>30</td>
                <td>Lagos</td>
            </tr>
        </tbody>
        <tfoot>
            <tr>
                <td colspan="3">End of data</td>
            </tr>
        </tfoot>
    </table>

─── KEY TABLE ELEMENTS ────────────────────────────────────────────────────────
    <table>   — container for the entire table
    <tr>      — table row
    <th>      — header cell (bold + centred by default)
    <td>      — data cell
    <thead>   — groups header rows
    <tbody>   — groups body rows
    <tfoot>   — groups footer rows
    <caption> — title above/below the table

─── SPANNING CELLS ────────────────────────────────────────────────────────────
Merge columns:  <td colspan="2">Spans two columns</td>
Merge rows:     <td rowspan="3">Spans three rows</td>

─── COLUMN GROUPS ─────────────────────────────────────────────────────────────
    <table>
        <colgroup>
            <col style="background-color: #f0f0f0">
            <col span="2" style="background-color: #e0f7fa">
        </colgroup>
        ...
    </table>

─── ACCESSIBILITY ─────────────────────────────────────────────────────────────
Use scope on <th> to associate headers with cells:
    <th scope="col">Name</th>   — header for a column
    <th scope="row">Alice</th>  — header for a row

Use id + headers attributes for complex tables:
    <th id="h-name">Name</th>
    <td headers="h-name">Alice</td>
""",
        "quiz_title": "Quiz 6 — Tables",
        "quiz_description": "20 questions on table structure, thead/tbody/tfoot, colspan, rowspan, caption, colgroup, and accessibility.",
        "time_limit": 20,
        "questions": [
            {"q": "Which tag creates a table in HTML?", "o": ["<grid>", "<tbl>", "<chart>", "<table>"], "a": "<table>"},
            {"q": "Which tag defines a table row?", "o": ["<tr>", "<td>", "<th>", "<row>"], "a": "<tr>"},
            {"q": "Which tag defines a standard table data cell?", "o": ["<tr>", "<cell>", "<tc>", "<td>"], "a": "<td>"},
            {"q": "Which tag defines a table header cell (bold and centred by default)?", "o": ["<td>", "<header>", "<thead>", "<th>"], "a": "<th>"},
            {"q": "Which element groups the header rows of a table?", "o": ["<th>", "<header>", "<thead>", "<top>"], "a": "<thead>"},
            {"q": "Which element groups the body rows of a table?", "o": ["<tbody>", "<body>", "<trows>", "<content>"], "a": "<tbody>"},
            {"q": "Which element groups the footer rows of a table?", "o": ["<tfoot>", "<footer>", "<tfooter>", "<bottom>"], "a": "<tfoot>"},
            {"q": "Which attribute makes a cell span multiple columns?", "o": ["span", "cols", "colspan", "columns"], "a": "colspan"},
            {"q": "Which attribute makes a cell span multiple rows?", "o": ["span", "rows", "rowspan", "rowmerge"], "a": "rowspan"},
            {"q": "Which element adds a visible title or caption to a table?", "o": ["<title>", "<header>", "<label>", "<caption>"], "a": "<caption>"},
            {"q": "Which element acts as a container for grouping <col> elements?", "o": ["<column>", "<cols>", "<colgroup>", "<colset>"], "a": "<colgroup>"},
            {"q": "Which element applies styles to individual columns without affecting cells?", "o": ["<column>", "<colstyle>", "<col>", "<tcol>"], "a": "<col>"},
            {"q": "Which attribute on <th> associates the header cell with its column or row for accessibility?", "o": ["for", "headers", "scope", "associate"], "a": "scope"},
            {"q": "What scope value associates a <th> with its entire column?", "o": ["\"td\"", "\"row\"", "\"cell\"", "\"col\""], "a": "\"col\""},
            {"q": "What scope value associates a <th> with its entire row?", "o": ["\"tr\"", "\"col\"", "\"line\"", "\"row\""], "a": "\"row\""},
            {"q": "How do you merge two adjacent cells horizontally into one?", "o": ["Use rowspan=\"2\"", "Use merge=\"horizontal\"", "Use colspan=\"2\"", "Use span=\"2\""], "a": "Use colspan=\"2\""},
            {"q": "How do you merge two cells vertically (across two rows)?", "o": ["Use colspan=\"2\"", "Use merge=\"vertical\"", "Use rowspan=\"2\"", "Use span=\"2\""], "a": "Use rowspan=\"2\""},
            {"q": "Tables in HTML should be used for which type of content?", "o": ["Page layout", "Navigation menus", "Tabular / data-driven content only", "Image galleries"], "a": "Tabular / data-driven content only"},
            {"q": "Which deprecated attribute adds space between table cells?", "o": ["padding", "spacing", "gap", "cellspacing"], "a": "cellspacing"},
            {"q": "Which deprecated attribute adds padding inside table cells?", "o": ["inner-space", "margin", "padding", "cellpadding"], "a": "cellpadding"},
        ],
    },
    {
        "order": 7,
        "title": "Forms — Inputs, Validation & Submission",
        "description": "Build complete HTML forms using form, input types, textarea, select, label, fieldset, legend, and HTML5 validation attributes.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 7: Forms — Inputs, Validation & Submission

HTML forms collect user data and send it to a server (or handle it client-side).

─── BASIC FORM STRUCTURE ──────────────────────────────────────────────────────
    <form action="/submit" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <button type="submit">Submit</button>
    </form>

─── FORM ATTRIBUTES ───────────────────────────────────────────────────────────
    action  — URL where form data is sent
    method  — HTTP method: get (visible in URL) or post (request body)
    enctype — encoding: "multipart/form-data" for file uploads

─── INPUT TYPES ───────────────────────────────────────────────────────────────
    text         — single-line text
    password     — masked text
    email        — validates email format
    number       — numeric value
    tel          — telephone number
    url          — URL
    date         — date picker
    time         — time picker
    checkbox     — tick box (multiple selections)
    radio        — radio button (one selection per group)
    file         — file upload
    hidden       — hidden field (not shown)
    submit       — submit button
    reset        — resets form fields
    button       — generic button
    range        — slider
    color        — colour picker
    search       — search field

─── LABEL ─────────────────────────────────────────────────────────────────────
Always connect labels to inputs for accessibility:
    <label for="email">Email:</label>
    <input type="email" id="email" name="email">

─── TEXTAREA & SELECT ─────────────────────────────────────────────────────────
    <textarea name="message" rows="5" cols="30"></textarea>

    <select name="country">
        <option value="ng">Nigeria</option>
        <option value="gh">Ghana</option>
    </select>

─── FIELDSET & LEGEND ─────────────────────────────────────────────────────────
    <fieldset>
        <legend>Personal Info</legend>
        ...
    </fieldset>

─── HTML5 VALIDATION ATTRIBUTES ───────────────────────────────────────────────
    required        — field must be filled
    minlength / maxlength — text length limits
    min / max       — numeric or date range
    pattern         — regex pattern
    placeholder     — hint text inside empty field
    value           — pre-filled value
    readonly        — user cannot change the value
    disabled        — field is completely inactive
    autofocus       — automatically focused on page load
    autocomplete    — on / off
""",
        "quiz_title": "Quiz 7 — Forms, Inputs & Validation",
        "quiz_description": "20 questions on form structure, input types, labels, textarea, select, fieldset, and HTML5 validation attributes.",
        "time_limit": 20,
        "questions": [
            {"q": "Which tag defines an HTML form?", "o": ["<input>", "<submit>", "<field>", "<form>"], "a": "<form>"},
            {"q": "Which attribute specifies where the form data is sent on submission?", "o": ["method", "send", "target", "action"], "a": "action"},
            {"q": "Which attribute specifies the HTTP method for form submission?", "o": ["type", "send", "submit", "method"], "a": "method"},
            {"q": "Which HTTP method sends form data appended to the URL?", "o": ["post", "put", "send", "get"], "a": "get"},
            {"q": "Which HTTP method sends form data in the request body (not visible in the URL)?", "o": ["get", "send", "hidden", "post"], "a": "post"},
            {"q": "Which input type creates a single-line text field?", "o": ["input", "field", "text", "string"], "a": "text"},
            {"q": "Which input type creates a password field with masked characters?", "o": ["secret", "hidden", "masked", "password"], "a": "password"},
            {"q": "Which input type creates a checkbox?", "o": ["check", "bool", "tick", "checkbox"], "a": "checkbox"},
            {"q": "Which input type creates a radio button?", "o": ["option", "round", "select", "radio"], "a": "radio"},
            {"q": "Which attribute groups radio buttons so only one can be selected at a time?", "o": ["group", "id", "name", "value"], "a": "name"},
            {"q": "Which input type creates a file upload button?", "o": ["upload", "attach", "document", "file"], "a": "file"},
            {"q": "Which input type creates a submit button?", "o": ["send", "go", "enter", "submit"], "a": "submit"},
            {"q": "Which input type creates a field that is not displayed but sends data?", "o": ["invisible", "none", "secret", "hidden"], "a": "hidden"},
            {"q": "Which tag creates a multi-line text input?", "o": ["<multiline>", "<textbox>", "<input type=\"multiline\">", "<textarea>"], "a": "<textarea>"},
            {"q": "Which tag creates a dropdown selection list?", "o": ["<dropdown>", "<list>", "<options>", "<select>"], "a": "<select>"},
            {"q": "Which tag defines each choice inside a <select> dropdown?", "o": ["<item>", "<choice>", "<li>", "<option>"], "a": "<option>"},
            {"q": "Which attribute marks a form field as required before submission?", "o": ["mandatory", "must-fill", "validate", "required"], "a": "required"},
            {"q": "Which attribute pre-fills a form field with a default value?", "o": ["default", "preset", "placeholder", "value"], "a": "value"},
            {"q": "Which attribute shows hint text inside an empty input field?", "o": ["hint", "title", "default", "placeholder"], "a": "placeholder"},
            {"q": "Which element groups related form controls with a visible border and title?", "o": ["<group>", "<section>", "<fieldset>", "<formgroup>"], "a": "<fieldset>"},
        ],
    },
    {
        "order": 8,
        "title": "HTML5 Semantic Elements & Page Layout",
        "description": "Understand semantic HTML5 elements: header, footer, main, nav, article, section, aside, hgroup, address, details, summary, meter, and progress.",
        "duration_minutes": 35,
        "content": """Welcome to Lesson 8: HTML5 Semantic Elements & Page Layout

Semantic HTML uses elements that clearly describe their meaning to both the browser and the developer.

─── WHY SEMANTIC HTML? ────────────────────────────────────────────────────────
• Accessibility: Screen readers navigate by landmarks
• SEO: Search engines understand page structure
• Maintainability: Code is easier to read and maintain

─── PAGE STRUCTURE ELEMENTS ───────────────────────────────────────────────────
    <header>  — introductory content, logos, navigation (can appear multiple times)
    <nav>     — primary navigation links
    <main>    — unique main content of the page (use only once)
    <footer>  — footer info: copyright, links, contact (can appear multiple times)

─── CONTENT SECTIONING ────────────────────────────────────────────────────────
    <article> — standalone, self-contained content (blog post, news article)
                Can be removed from the page and still make sense elsewhere.

    <section> — thematic grouping of content with a heading
                Represents a chapter or topic within the page.

    <aside>   — content tangentially related to main content (sidebar, pull quote)

─── ARTICLE vs SECTION ────────────────────────────────────────────────────────
    <article> — would make sense published on its own (syndicate-able)
    <section> — groups related content within a page; not standalone

─── TEXT-LEVEL SEMANTICS ──────────────────────────────────────────────────────
    <address> — contact information for the nearest <article> or <body>
    <hgroup>  — groups a heading with a sub-heading
    <time datetime="2024-01-15">January 15, 2024</time>

─── INTERACTIVE ELEMENTS ──────────────────────────────────────────────────────
    <details>           — expandable/collapsible disclosure widget
        <summary>       — visible label for the <details> element
        <p>Hidden content revealed on click</p>
    </details>

─── PROGRESS & MEASUREMENT ────────────────────────────────────────────────────
    <progress value="70" max="100">70%</progress>
    <meter value="0.6" min="0" max="1">60%</meter>

    progress — task completion (upload progress, form steps)
    meter    — a scalar value within a defined range (battery, score)

─── NON-SEMANTIC FALLBACKS ────────────────────────────────────────────────────
    <div>   — block-level grouping (no meaning)
    <span>  — inline grouping (no meaning)
    Use these only when no semantic element fits.
""",
        "quiz_title": "Quiz 8 — HTML5 Semantic Elements",
        "quiz_description": "20 questions on header, footer, main, nav, article, section, aside, details, summary, meter, progress, and semantic best practices.",
        "time_limit": 20,
        "questions": [
            {"q": "What makes an HTML element 'semantic'?", "o": ["It has visual styling built in", "It conveys meaning about its content to browsers and developers", "It is only available in HTML5", "It replaces CSS"], "a": "It conveys meaning about its content to browsers and developers"},
            {"q": "Which element defines the primary navigation links of a page?", "o": ["<menu>", "<links>", "<navigate>", "<nav>"], "a": "<nav>"},
            {"q": "Which element defines the header or introduction section of a page or section?", "o": ["<top>", "<head>", "<title>", "<header>"], "a": "<header>"},
            {"q": "Which element defines the footer of a page or section?", "o": ["<bottom>", "<end>", "<foot>", "<footer>"], "a": "<footer>"},
            {"q": "Which element defines the primary unique content of a page?", "o": ["<body>", "<content>", "<primary>", "<main>"], "a": "<main>"},
            {"q": "Which element represents a standalone, self-contained piece of content (e.g. a blog post)?", "o": ["<div>", "<section>", "<content>", "<article>"], "a": "<article>"},
            {"q": "Which element defines a thematic section of content, typically with a heading?", "o": ["<div>", "<part>", "<chapter>", "<section>"], "a": "<section>"},
            {"q": "Which element represents content tangentially related to the main content, like a sidebar?", "o": ["<extra>", "<sidebar>", "<note>", "<aside>"], "a": "<aside>"},
            {"q": "What is the key difference between <article> and <section>?", "o": ["No difference", "<article> is standalone/syndicate-able; <section> groups thematically related content", "<section> is standalone; <article> groups content", "<article> is for news only"], "a": "<article> is standalone/syndicate-able; <section> groups thematically related content"},
            {"q": "Which non-semantic element is used for block-level grouping with no meaning?", "o": ["<block>", "<group>", "<span>", "<div>"], "a": "<div>"},
            {"q": "Which non-semantic element is used for inline grouping with no meaning?", "o": ["<inline>", "<text>", "<div>", "<span>"], "a": "<span>"},
            {"q": "Can a page have multiple <header> elements?", "o": ["No, only one per page", "Yes, each section or article can have its own <header>", "Yes, but only inside <article>", "Only in HTML 5.1+"], "a": "Yes, each section or article can have its own <header>"},
            {"q": "Which element is used for contact information (author or owner of content)?", "o": ["<contact>", "<info>", "<address>", "<details>"], "a": "<address>"},
            {"q": "Which element creates a disclosure widget (expandable/collapsible section)?", "o": ["<collapse>", "<expand>", "<toggle>", "<details>"], "a": "<details>"},
            {"q": "Which element defines the visible heading or label inside a <details> element?", "o": ["<label>", "<title>", "<caption>", "<summary>"], "a": "<summary>"},
            {"q": "Which element represents a scalar measurement within a known range (e.g. battery level)?", "o": ["<range>", "<scale>", "<gauge>", "<meter>"], "a": "<meter>"},
            {"q": "Which element displays a task completion bar (e.g. upload progress)?", "o": ["<bar>", "<loading>", "<meter>", "<progress>"], "a": "<progress>"},
            {"q": "Which element groups a main heading with a related sub-heading?", "o": ["<headings>", "<hgroup>", "<titles>", "<group>"], "a": "<hgroup>"},
            {"q": "How many <main> elements should a page have?", "o": ["As many as needed", "One per section", "Only one", "Two maximum"], "a": "Only one"},
            {"q": "Why should developers prefer semantic HTML over generic <div> elements?", "o": ["Semantic HTML loads faster", "Generic divs use more memory", "Semantic HTML improves accessibility, SEO, and code readability", "Semantic HTML applies default visual styles automatically"], "a": "Semantic HTML improves accessibility, SEO, and code readability"},
        ],
    },
    {
        "order": 9,
        "title": "HTML5 Media, Embedding & Advanced Features",
        "description": "Embed video, audio, iframes, canvas, and SVG; use track for subtitles; control autoplay, loop, muted, and poster; understand Open Graph meta tags and the sandbox attribute.",
        "duration_minutes": 40,
        "content": """Welcome to Lesson 9: HTML5 Media, Embedding & Advanced Features

HTML5 introduced native support for video, audio, and interactive graphics — no plugins required.

─── VIDEO ─────────────────────────────────────────────────────────────────────
    <video src="movie.mp4" controls width="720" poster="thumb.jpg">
        Your browser does not support the video tag.
    </video>

Common attributes:
    controls   — show play/pause/volume controls
    autoplay   — play on page load (requires muted in most browsers)
    muted      — mute audio by default
    loop       — loop the video
    poster     — thumbnail image shown before playback
    preload    — none | metadata | auto

─── MULTIPLE SOURCES ──────────────────────────────────────────────────────────
    <video controls>
        <source src="movie.mp4" type="video/mp4">
        <source src="movie.webm" type="video/webm">
        Your browser does not support the video tag.
    </video>

─── AUDIO ─────────────────────────────────────────────────────────────────────
    <audio controls>
        <source src="song.mp3" type="audio/mpeg">
        <source src="song.ogg" type="audio/ogg">
    </audio>

─── TEXT TRACKS (SUBTITLES / CAPTIONS) ────────────────────────────────────────
    <video controls>
        <source src="video.mp4" type="video/mp4">
        <track src="subs_en.vtt" kind="subtitles" srclang="en" label="English" default>
    </video>

track kind values: subtitles | captions | descriptions | chapters | metadata

─── IFRAME ────────────────────────────────────────────────────────────────────
    <iframe src="https://example.com"
            width="600" height="400"
            title="Example"
            sandbox="allow-scripts allow-same-origin"
            loading="lazy">
    </iframe>

sandbox attribute restricts what the embedded page can do.
Common sandbox values:
    allow-scripts         — run JavaScript
    allow-forms           — submit forms
    allow-same-origin     — treat as same origin
    allow-popups          — open popups

─── CANVAS ────────────────────────────────────────────────────────────────────
    <canvas id="myCanvas" width="500" height="300"></canvas>
Drawn on with JavaScript. Pixel-based / raster rendering.

─── SVG INLINE ────────────────────────────────────────────────────────────────
    <svg width="100" height="100">
        <circle cx="50" cy="50" r="40" fill="blue" />
    </svg>
Vector-based, scalable, part of the DOM.

─── OPEN GRAPH META TAGS ──────────────────────────────────────────────────────
Control how your page appears when shared on social media:
    <meta property="og:title" content="My Page Title">
    <meta property="og:description" content="Description here">
    <meta property="og:image" content="https://example.com/image.jpg">

─── VIDEO POSTER & PRELOAD ────────────────────────────────────────────────────
    poster="thumb.jpg"  — thumbnail shown before play
    preload="metadata"  — load only metadata (dimensions, duration)
""",
        "quiz_title": "Quiz 9 — HTML5 Media, Embedding & Advanced Features",
        "quiz_description": "20 questions on video, audio, source, track, iframe, sandbox, canvas, SVG, and Open Graph tags.",
        "time_limit": 20,
        "questions": [
            {"q": "Which tag embeds a video natively in HTML5?", "o": ["<movie>", "<media>", "<embed>", "<video>"], "a": "<video>"},
            {"q": "Which tag embeds audio natively in HTML5?", "o": ["<sound>", "<mp3>", "<music>", "<audio>"], "a": "<audio>"},
            {"q": "Which attribute shows the browser's built-in media controls?", "o": ["showcontrols", "ui", "buttons", "controls"], "a": "controls"},
            {"q": "Which attribute makes a video play automatically on page load?", "o": ["play", "onload", "start", "autoplay"], "a": "autoplay"},
            {"q": "Which attribute mutes a video by default?", "o": ["silent", "noaudio", "volume=\"0\"", "muted"], "a": "muted"},
            {"q": "Which attribute makes a video/audio loop continuously?", "o": ["repeat", "continuous", "cycle", "loop"], "a": "loop"},
            {"q": "Which attribute sets the thumbnail image shown before a video plays?", "o": ["thumbnail", "cover", "preview", "poster"], "a": "poster"},
            {"q": "Which tag inside <video> or <audio> specifies an alternative media file source?", "o": ["<file>", "<media>", "<src>", "<source>"], "a": "<source>"},
            {"q": "Which attribute on <source> specifies the media MIME type?", "o": ["format", "mime", "kind", "type"], "a": "type"},
            {"q": "Which tag provides subtitles or captions for a video?", "o": ["<subtitle>", "<caption>", "<text>", "<track>"], "a": "<track>"},
            {"q": "Which kind attribute value on <track> identifies subtitle text?", "o": ["text", "sub", "captions", "subtitles"], "a": "subtitles"},
            {"q": "Which element embeds another HTML page within the current page?", "o": ["<frame>", "<include>", "<embed>", "<iframe>"], "a": "<iframe>"},
            {"q": "Which attribute on <iframe> sets the URL of the embedded page?", "o": ["href", "link", "url", "src"], "a": "src"},
            {"q": "Which sandbox value allows a sandboxed iframe to submit forms?", "o": ["allow-scripts", "allow-navigation", "allow-forms", "allow-submit"], "a": "allow-forms"},
            {"q": "What is the <canvas> element used for?", "o": ["Display vector graphics", "Embed external content", "Pixel-based drawing via JavaScript", "Create responsive layouts"], "a": "Pixel-based drawing via JavaScript"},
            {"q": "What is the key difference between <canvas> and <svg>?", "o": ["They are the same", "<canvas> is pixel-based JavaScript drawing; <svg> is declarative vector markup", "<svg> is JavaScript-based; <canvas> is declarative", "<canvas> is for 3D only; <svg> for 2D only"], "a": "<canvas> is pixel-based JavaScript drawing; <svg> is declarative vector markup"},
            {"q": "What is the Open Graph meta tag protocol used for?", "o": ["Improving page load speed", "Controlling social media preview cards when a page is shared", "Setting the page's primary language", "Defining canonical URLs for SEO"], "a": "Controlling social media preview cards when a page is shared"},
            {"q": "Which meta tag prevents search engines from indexing a page?", "o": ["<meta name=\"noindex\" content=\"true\">", "<meta http-equiv=\"noindex\">", "<meta name=\"robots\" content=\"noindex\">", "<meta name=\"search\" content=\"false\">"], "a": "<meta name=\"robots\" content=\"noindex\">"},
            {"q": "Which attribute on <iframe> provides an accessible name for the embedded content?", "o": ["name", "label", "title", "alt"], "a": "title"},
            {"q": "Which attribute on <video> controls how much of the video is preloaded?", "o": ["buffer", "cache", "prefetch", "preload"], "a": "preload"},
        ],
    },
    {
        "order": 10,
        "title": "Final Review — Comprehensive HTML Assessment",
        "description": "A 100-question comprehensive quiz covering all nine lessons: document structure, text, links, images, lists, tables, forms, semantics, and media.",
        "duration_minutes": 60,
        "content": """Welcome to Lesson 10: Final Review — Comprehensive HTML Assessment

This is your final assessment covering everything from Lessons 1 through 9.

Topics included:
  1. HTML document structure & DOCTYPE
  2. Text content — headings, paragraphs, formatting
  3. Links, anchors, and navigation
  4. Images, figures, and responsive images
  5. Lists — ordered, unordered, description
  6. Tables — structure, spanning, accessibility
  7. Forms — inputs, validation, submission
  8. HTML5 semantic elements & page layout
  9. HTML5 media, embedding & advanced features

Take your time. You have 100 questions and 100 minutes.
A score of 70% or above is required to pass.

Good luck!
""",
        "quiz_title": "Final Quiz — Comprehensive HTML (100 Questions)",
        "quiz_description": "100-question comprehensive assessment covering all HTML topics from the entire course.",
        "time_limit": 100,
        "questions": [
            # Document Structure (1–12)
            {"q": "What does HTML stand for?", "o": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"], "a": "Hyper Text Markup Language"},
            {"q": "Which declaration must appear at the very first line of an HTML5 file?", "o": ["<html>", "<!DOCTYPE html>", "<!-- HTML5 -->", "<head>"], "a": "<!DOCTYPE html>"},
            {"q": "What is the root element that wraps the entire HTML document?", "o": ["<root>", "<page>", "<html>", "<body>"], "a": "<html>"},
            {"q": "Which element contains invisible metadata (title, meta, link, script)?", "o": ["<meta>", "<head>", "<header>", "<info>"], "a": "<head>"},
            {"q": "Which element contains the visible content of a web page?", "o": ["<main>", "<section>", "<body>", "<content>"], "a": "<body>"},
            {"q": "What is the correct syntax for an HTML comment?", "o": ["// comment", "/* comment */", "<!-- comment -->", "## comment"], "a": "<!-- comment -->"},
            {"q": "Which meta tag sets the document's character encoding?", "o": ["<meta charset=\"UTF-8\">", "<meta type=\"UTF-8\">", "<meta encoding=\"UTF-8\">", "<meta lang=\"UTF-8\">"], "a": "<meta charset=\"UTF-8\">"},
            {"q": "Which attribute on <html> specifies the document's language?", "o": ["locale", "language", "charset", "lang"], "a": "lang"},
            {"q": "Void elements in HTML5 cannot have which of the following?", "o": ["Attributes", "An id", "A closing tag", "Inline styles"], "a": "A closing tag"},
            {"q": "Which tag sets the text displayed in the browser tab?", "o": ["<caption>", "<label>", "<heading>", "<title>"], "a": "<title>"},
            {"q": "Where should <script> tags be placed for best performance?", "o": ["Inside <head>", "Before </html>", "Before </body>", "After <!DOCTYPE>"], "a": "Before </body>"},
            {"q": "Which element wraps inline content with no semantic meaning?", "o": ["<div>", "<section>", "<span>", "<inline>"], "a": "<span>"},
            # Text & Formatting (13–24)
            {"q": "Which heading tag produces the largest text?", "o": ["<h6>", "<h2>", "<heading>", "<h1>"], "a": "<h1>"},
            {"q": "Which heading tag produces the smallest text?", "o": ["<h1>", "<h3>", "<h5>", "<h6>"], "a": "<h6>"},
            {"q": "Which tag defines a paragraph of text?", "o": ["<para>", "<txt>", "<p>", "<pg>"], "a": "<p>"},
            {"q": "Which void tag inserts a line break within text?", "o": ["<lb>", "<break>", "<newline>", "<br>"], "a": "<br>"},
            {"q": "Which tag creates a thematic horizontal line?", "o": ["<divider>", "<line>", "<rule>", "<hr>"], "a": "<hr>"},
            {"q": "Which element marks text as bold with semantic importance?", "o": ["<b>", "<bold>", "<strong>", "<em>"], "a": "<strong>"},
            {"q": "Which element marks text as italic with semantic emphasis?", "o": ["<i>", "<italic>", "<b>", "<em>"], "a": "<em>"},
            {"q": "Which tag highlights relevant text (yellow background by default)?", "o": ["<highlight>", "<span>", "<mark>", "<yellow>"], "a": "<mark>"},
            {"q": "Which tag renders superscript text (e.g. for exponents)?", "o": ["<up>", "<super>", "<top>", "<sup>"], "a": "<sup>"},
            {"q": "Which tag renders subscript text (e.g. for chemical formulas)?", "o": ["<down>", "<low>", "<bottom>", "<sub>"], "a": "<sub>"},
            {"q": "Which element is used for a long block quotation?", "o": ["<q>", "<cite>", "<quote>", "<blockquote>"], "a": "<blockquote>"},
            {"q": "Which element preserves whitespace and line breaks in monospace font?", "o": ["<mono>", "<raw>", "<text>", "<pre>"], "a": "<pre>"},
            # Links (25–34)
            {"q": "Which tag creates a hyperlink?", "o": ["<link>", "<href>", "<url>", "<a>"], "a": "<a>"},
            {"q": "Which attribute specifies the hyperlink's destination URL?", "o": ["src", "link", "url", "href"], "a": "href"},
            {"q": "Which target value opens a link in a new browser tab?", "o": ["_new", "_tab", "_window", "_blank"], "a": "_blank"},
            {"q": "Which target value keeps the link in the same tab?", "o": ["_same", "_current", "_default", "_self"], "a": "_self"},
            {"q": "What scheme do you use to create an email link?", "o": ["email:", "mail:", "send:", "mailto:"], "a": "mailto:"},
            {"q": "What scheme do you use to create a phone number link?", "o": ["phone:", "call:", "dial:", "tel:"], "a": "tel:"},
            {"q": "How do you link to an element with id=\"contact\" on the same page?", "o": ["href=\"contact\"", "href=\"@contact\"", "href=\"*contact\"", "href=\"#contact\""], "a": "href=\"#contact\""},
            {"q": "Which attribute triggers a file download when clicking a link?", "o": ["save", "export", "file", "download"], "a": "download"},
            {"q": "Which security attribute should accompany target=\"_blank\" to prevent tab-napping?", "o": ["rel=\"nofollow\"", "rel=\"external\"", "rel=\"noopener noreferrer\"", "rel=\"unsafe\""], "a": "rel=\"noopener noreferrer\""},
            {"q": "Which rel value instructs search engines not to follow a link?", "o": ["rel=\"noindex\"", "rel=\"ignore\"", "rel=\"nopass\"", "rel=\"nofollow\""], "a": "rel=\"nofollow\""},
            # Images (35–44)
            {"q": "Which void tag embeds an image?", "o": ["<image>", "<photo>", "<picture>", "<img>"], "a": "<img>"},
            {"q": "Which attribute specifies the image source path or URL?", "o": ["href", "path", "url", "src"], "a": "src"},
            {"q": "Which attribute provides alternative text for an image?", "o": ["title", "caption", "desc", "alt"], "a": "alt"},
            {"q": "Which HTML5 element wraps an image with its caption?", "o": ["<gallery>", "<imgwrap>", "<section>", "<figure>"], "a": "<figure>"},
            {"q": "Which element provides the caption text inside a <figure>?", "o": ["<caption>", "<label>", "<description>", "<figcaption>"], "a": "<figcaption>"},
            {"q": "What does loading=\"lazy\" do on an image?", "o": ["Loads the image immediately", "Compresses the image", "Defers loading until the image nears the viewport", "Disables the image on mobile"], "a": "Defers loading until the image nears the viewport"},
            {"q": "Which element lets you serve different images based on screen size?", "o": ["<imgset>", "<responsive>", "<gallery>", "<picture>"], "a": "<picture>"},
            {"q": "Which attribute provides multiple image sources for different resolutions?", "o": ["sources", "mediasrc", "responsive", "srcset"], "a": "srcset"},
            {"q": "Which image format supports transparent backgrounds?", "o": ["JPG", "GIF", "BMP", "PNG"], "a": "PNG"},
            {"q": "Which image format is vector-based and resolution-independent?", "o": ["GIF", "PNG", "JPG", "SVG"], "a": "SVG"},
            # Lists (45–54)
            {"q": "Which tag creates an unordered (bulleted) list?", "o": ["<ol>", "<dl>", "<list>", "<ul>"], "a": "<ul>"},
            {"q": "Which tag creates an ordered (numbered) list?", "o": ["<ul>", "<numbered>", "<list>", "<ol>"], "a": "<ol>"},
            {"q": "Which tag defines a list item in <ul> or <ol>?", "o": ["<item>", "<entry>", "<it>", "<li>"], "a": "<li>"},
            {"q": "Which list type is designed for term–definition pairs?", "o": ["<ul>", "<ol>", "<tl>", "<dl>"], "a": "<dl>"},
            {"q": "Which tag defines a term in a description list?", "o": ["<term>", "<dd>", "<key>", "<dt>"], "a": "<dt>"},
            {"q": "Which tag defines a description in a description list?", "o": ["<dt>", "<def>", "<desc>", "<dd>"], "a": "<dd>"},
            {"q": "Which <ol> attribute sets the starting number?", "o": ["begin", "from", "first", "start"], "a": "start"},
            {"q": "Which type value on <ol> produces uppercase Roman numerals?", "o": ["type=\"R\"", "type=\"ROMAN\"", "type=\"upper-roman\"", "type=\"I\""], "a": "type=\"I\""},
            {"q": "Which attribute on <ol> reverses the count direction?", "o": ["descending", "countdown", "backwards", "reversed"], "a": "reversed"},
            {"q": "Where must <li> elements appear?", "o": ["Anywhere", "Inside <dl>", "Inside any block element", "Inside <ul> or <ol>"], "a": "Inside <ul> or <ol>"},
            # Tables (55–64)
            {"q": "Which tag creates a table?", "o": ["<grid>", "<chart>", "<tbl>", "<table>"], "a": "<table>"},
            {"q": "Which tag defines a table row?", "o": ["<td>", "<th>", "<row>", "<tr>"], "a": "<tr>"},
            {"q": "Which tag defines a standard table data cell?", "o": ["<tr>", "<tc>", "<th>", "<td>"], "a": "<td>"},
            {"q": "Which tag defines a header cell (bold and centred by default)?", "o": ["<thead>", "<td>", "<header>", "<th>"], "a": "<th>"},
            {"q": "Which element groups the header rows of a table?", "o": ["<th>", "<top>", "<header>", "<thead>"], "a": "<thead>"},
            {"q": "Which element groups the body rows?", "o": ["<body>", "<trows>", "<content>", "<tbody>"], "a": "<tbody>"},
            {"q": "Which element groups the footer rows?", "o": ["<footer>", "<tfooter>", "<bottom>", "<tfoot>"], "a": "<tfoot>"},
            {"q": "Which attribute merges a cell across multiple columns?", "o": ["span", "cols", "columns", "colspan"], "a": "colspan"},
            {"q": "Which attribute merges a cell across multiple rows?", "o": ["span", "rows", "rowmerge", "rowspan"], "a": "rowspan"},
            {"q": "Which element adds a visible title above a table?", "o": ["<title>", "<header>", "<label>", "<caption>"], "a": "<caption>"},
            # Forms (65–76)
            {"q": "Which tag defines an HTML form?", "o": ["<input>", "<submit>", "<field>", "<form>"], "a": "<form>"},
            {"q": "Which attribute specifies where form data is sent?", "o": ["method", "send", "target", "action"], "a": "action"},
            {"q": "Which HTTP method sends data in the request body?", "o": ["get", "send", "hidden", "post"], "a": "post"},
            {"q": "Which HTTP method appends data to the URL?", "o": ["post", "put", "send", "get"], "a": "get"},
            {"q": "Which input type validates an email address format?", "o": ["text", "mail", "contact", "email"], "a": "email"},
            {"q": "Which input type creates a checkbox?", "o": ["check", "bool", "tick", "checkbox"], "a": "checkbox"},
            {"q": "Which input type creates a radio button?", "o": ["option", "round", "select", "radio"], "a": "radio"},
            {"q": "Which tag creates a multi-line text input?", "o": ["<textbox>", "<input type=\"multiline\">", "<multiline>", "<textarea>"], "a": "<textarea>"},
            {"q": "Which tag creates a dropdown selection list?", "o": ["<dropdown>", "<list>", "<options>", "<select>"], "a": "<select>"},
            {"q": "Which attribute marks a field as required before form submission?", "o": ["mandatory", "must-fill", "validate", "required"], "a": "required"},
            {"q": "Which attribute shows placeholder hint text inside an input?", "o": ["hint", "title", "default", "placeholder"], "a": "placeholder"},
            {"q": "Which element groups related form fields with a border and label?", "o": ["<group>", "<section>", "<formgroup>", "<fieldset>"], "a": "<fieldset>"},
            # Semantics (77–88)
            {"q": "Which element defines the primary navigation links?", "o": ["<menu>", "<links>", "<navigate>", "<nav>"], "a": "<nav>"},
            {"q": "Which element defines the page or section header?", "o": ["<top>", "<head>", "<title>", "<header>"], "a": "<header>"},
            {"q": "Which element defines the page or section footer?", "o": ["<bottom>", "<foot>", "<end>", "<footer>"], "a": "<footer>"},
            {"q": "Which element holds the unique primary content of a page?", "o": ["<body>", "<content>", "<primary>", "<main>"], "a": "<main>"},
            {"q": "Which element represents a standalone, self-contained article or post?", "o": ["<div>", "<section>", "<content>", "<article>"], "a": "<article>"},
            {"q": "Which element groups thematically related content with a heading?", "o": ["<div>", "<part>", "<chapter>", "<section>"], "a": "<section>"},
            {"q": "Which element represents sidebar or tangentially related content?", "o": ["<extra>", "<sidebar>", "<note>", "<aside>"], "a": "<aside>"},
            {"q": "Which element creates a collapsible/expandable disclosure widget?", "o": ["<collapse>", "<expand>", "<toggle>", "<details>"], "a": "<details>"},
            {"q": "Which element labels a <details> widget?", "o": ["<label>", "<title>", "<caption>", "<summary>"], "a": "<summary>"},
            {"q": "Which element displays a scalar value within a defined range?", "o": ["<range>", "<scale>", "<gauge>", "<meter>"], "a": "<meter>"},
            {"q": "Which element shows task-completion progress?", "o": ["<bar>", "<loading>", "<meter>", "<progress>"], "a": "<progress>"},
            {"q": "How many <main> elements should an HTML page contain?", "o": ["As many as needed", "One per section", "Two maximum", "Only one"], "a": "Only one"},
            # Media & Embedding (89–100)
            {"q": "Which tag natively embeds video in HTML5?", "o": ["<movie>", "<media>", "<embed>", "<video>"], "a": "<video>"},
            {"q": "Which tag natively embeds audio in HTML5?", "o": ["<sound>", "<mp3>", "<music>", "<audio>"], "a": "<audio>"},
            {"q": "Which attribute displays browser-default media controls?", "o": ["showcontrols", "ui", "buttons", "controls"], "a": "controls"},
            {"q": "Which attribute mutes a video by default?", "o": ["silent", "noaudio", "volume=\"0\"", "muted"], "a": "muted"},
            {"q": "Which attribute sets the video thumbnail image shown before playback?", "o": ["thumbnail", "cover", "preview", "poster"], "a": "poster"},
            {"q": "Which tag specifies an alternative media source inside <video> or <audio>?", "o": ["<file>", "<media>", "<src>", "<source>"], "a": "<source>"},
            {"q": "Which tag provides subtitles or captions for a <video>?", "o": ["<subtitle>", "<caption>", "<text>", "<track>"], "a": "<track>"},
            {"q": "Which element embeds another HTML page inside the current page?", "o": ["<frame>", "<include>", "<embed>", "<iframe>"], "a": "<iframe>"},
            {"q": "Which attribute restricts what an embedded iframe can do?", "o": ["restrict", "limit", "permissions", "sandbox"], "a": "sandbox"},
            {"q": "Which element is used for pixel-based drawing via JavaScript?", "o": ["<draw>", "<graphic>", "<svg>", "<canvas>"], "a": "<canvas>"},
            {"q": "Which element is used for declarative vector graphics directly in HTML?", "o": ["<canvas>", "<vector>", "<graphic>", "<svg>"], "a": "<svg>"},
            {"q": "What is the purpose of Open Graph meta tags?", "o": ["Speed up page load", "Control social media preview cards", "Set canonical URLs", "Define the page language"], "a": "Control social media preview cards"},
        ],
    },
]


class Command(BaseCommand):
    help = "Create a detailed Introduction to HTML course: 9 content lessons each with a 20-question quiz, plus a 100-question final review."

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
            title="Introduction to HTML — Complete Beginner Course",
            instructor=tutor,
            defaults={
                "description": (
                    "A comprehensive, lesson-by-lesson introduction to HTML. "
                    "Starting from the very basics of document structure, you will progress through "
                    "text formatting, hyperlinks, images, lists, tables, forms, HTML5 semantic elements, "
                    "and media embedding. Each of the 9 content lessons is followed by a 20-question quiz "
                    "to reinforce your learning, and the course ends with a 100-question comprehensive assessment."
                ),
                "short_description": "Master HTML from scratch — 9 detailed lessons, 9 quizzes, and a 100-question final exam.",
                "category": category,
                "price": 0.00,
                "is_free": True,
                "difficulty": "beginner",
                "duration_hours": 6,
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
                    "content": lesson_data["content"],
                    "duration_minutes": lesson_data["duration_minutes"],
                    "is_published": True,
                },
            )
            lesson_action = "Created" if lesson_created else "Found"
            self.stdout.write(f"  {lesson_action} lesson {lesson_data['order']}: {lesson_data['title']}")

            quiz, quiz_created = Quiz.objects.get_or_create(
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
