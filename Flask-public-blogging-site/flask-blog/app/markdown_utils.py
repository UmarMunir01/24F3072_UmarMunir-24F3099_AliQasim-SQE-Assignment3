from markdown import markdown
from markupsafe import Markup
import bleach
import re

# Allowed tags/attributes for bleach (extend as needed)
ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre',
    'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'p', 'br', 'hr', 'img', 'table', 'thead',
    'tbody', 'tr', 'th', 'td', 'del', 'kbd', 's', 'sup', 'sub'
]
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'title', 'rel', 'target'],
    'img': ['src', 'alt', 'title'],
    'code': ['class']
}

# existing full-content filter (keep as-is)
def markdown_to_html(text: str) -> Markup:
    if not text:
        return Markup('')
    html = markdown(
        text,
        extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'nl2br',
            'sane_lists'
        ],
        extension_configs={
            'codehilite': {'guess_lang': False, 'use_pygments': True}
        },
        output_format='html5'
    )
    cleaned = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
    linked = bleach.linkify(cleaned)
    return Markup(linked)

# new: a lightweight title filter that only allows inline formatting and removes outer <p>
def markdown_title(text: str) -> Markup:
    if not text:
        return Markup('')
    # render markdown (may produce <p>...</p> for plain inline markdown)
    html = markdown(text, extensions=['extra', 'sane_lists'], output_format='html5')
    # strip a single enclosing <p>...</p> so titles don't become wrapped paragraphs
    html = re.sub(r'^\s*<p>(.*)</p>\s*$', r'\1', html, flags=re.DOTALL)
    # allow only safe inline tags for titles
    inline_tags = ['a', 'strong', 'em', 'code', 'span', 'del', 'sup', 'sub', 'kbd']
    inline_attrs = {'a': ['href', 'title', 'target', 'rel']}
    cleaned = bleach.clean(html, tags=inline_tags, attributes=inline_attrs, strip=True)
    linked = bleach.linkify(cleaned)
    return Markup(linked)