"""Shared offline renderer for AI text; formulas remain editable/searchable."""
import re
from html import unescape
from PySide6.QtGui import QTextDocument

_SUP = str.maketrans('0123456789+-=()in', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁱⁿ')
_SUB = str.maketrans('0123456789+-=()', '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎')

def math_text(expr):
    expr = expr.strip()
    expr = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', expr)
    expr = re.sub(r'\\sqrt\{([^{}]+)\}', r'√(\1)', expr)
    symbols = {'Delta':'Δ','delta':'δ','alpha':'α','beta':'β','theta':'θ','pi':'π','infty':'∞','times':'×','cdot':'·','leq':'≤','geq':'≥','le':'≤','ge':'≥','neq':'≠','log':'log','ln':'ln','pm':'±','rightarrow':'→','sum':'∑'}
    expr = re.sub(r'\\([A-Za-z]+)', lambda m: symbols.get(m[1], m[0]), expr)
    expr = re.sub(r'\^(?:\{([0-9+=()in-]+)\}|([0-9in]))', lambda m: (m[1] or m[2]).translate(_SUP), expr)
    expr = re.sub(r'_(?:\{([0-9+=()-]+)\}|([0-9]))', lambda m: (m[1] or m[2]).translate(_SUB), expr)
    return expr

def normalize(text):
    text = unescape(str(text or ''))
    text = re.sub(r'^\s*Oto (?:gotowa |krótka )?notatka[^\n]*:\s*\n', '', text, flags=re.I)
    text = re.sub(r'^\s*```(?:markdown|md)\s*\n(.*?)\n```\s*$', r'\1', text, flags=re.S|re.I)
    # Preserve fenced and inline code verbatim.
    chunks = re.split(r'(```[\s\S]*?```|`[^`\n]+`)', text)
    for i in range(0, len(chunks), 2):
        s = chunks[i]
        for pattern, block in [(r'\$\$(.*?)\$\$', True), (r'\\\[(.*?)\\\]', True), (r'\\\((.*?)\\\)', False), (r'(?<!\$)\$([^$\n]+)\$(?!\$)', False)]:
            s = re.sub(pattern, lambda m: ('\n\n' if block else '') + math_text(m[1]) + ('\n\n' if block else ''), s, flags=re.S)
        s = re.sub(r'\\([*`_\[\].!])', r'\1', s)
        chunks[i] = s
    return ''.join(chunks)

def render_markdown(text):
    from themes.theme import CURRENT
    from PySide6.QtGui import QFont
    doc = QTextDocument()
    font = QFont("Segoe UI")
    font.setPixelSize(int(CURRENT.get("font_size", 14)))
    doc.setDefaultFont(font)
    doc.setMarkdown(normalize(text), QTextDocument.MarkdownFeature.MarkdownDialectGitHub | QTextDocument.MarkdownFeature.MarkdownNoHTML)
    html = doc.toHtml()
    match = re.search(r'<body[^>]*>(.*)</body>', html, re.S)
    return match[1] if match else html

def set_markdown(widget, text):
    widget.setHtml(render_markdown(text))
