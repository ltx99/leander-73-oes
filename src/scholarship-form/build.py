"""Render form.html to PDF, then add fillable fields over each box.

Usage: python3 build.py OUTPUT.pdf
"""
import os
import sys
import pymupdf as fitz
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
OUT = sys.argv[1]
PX = 0.75  # CSS px -> PDF points (96 px per inch, 72 pt per inch)

MEASURE = '''() => {
  const out = [];
  document.querySelectorAll('.page').forEach((pgEl, i) => {
    const pr = pgEl.getBoundingClientRect();
    pgEl.querySelectorAll('[data-name],[data-check]').forEach(e => {
      const r = e.getBoundingClientRect();
      out.push({page: i, name: e.dataset.name || e.dataset.check, kind: e.dataset.check ? 'check' : 'text',
                lines: +(e.dataset.lines || 1), tip: e.dataset.tip,
                x0: r.left - pr.left, y0: r.top - pr.top, x1: r.right - pr.left, y1: r.bottom - pr.top});
    });
  });
  return out;
}'''

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 816, 'height': 1056})
    page.emulate_media(media='print')
    page.goto('file://' + HERE + 'form.html')
    page.wait_for_timeout(300)
    fields = page.evaluate(MEASURE)
    page.pdf(path=HERE + 'base.pdf', width='8.5in', height='11in', print_background=True,
             margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
    browser.close()

doc = fitz.open(HERE + 'base.pdf')
ink = (0.12, 0.10, 0.40)  # dark purple-navy for typed answers

for f in fields:
    r = fitz.Rect(f['x0'] * PX, f['y0'] * PX, f['x1'] * PX, f['y1'] * PX)
    w = fitz.Widget()
    w.field_name = f['name']
    w.field_label = f['tip']
    w.border_width = 0
    w.fill_color = None
    if f['kind'] == 'check':
        w.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
        w.rect = r
        w.text_color = ink
        w.field_value = False
    else:
        w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        w.rect = fitz.Rect(r.x0 + 4, r.y0 + 1.5, r.x1 - 4, r.y1 - 1.5)
        w.text_font = 'Helv'
        w.text_fontsize = 11
        w.text_color = ink
        if f['lines'] > 1:
            w.field_flags = fitz.PDF_TX_FIELD_IS_MULTILINE
    doc[f['page']].add_widget(w)

doc.set_metadata({'title': 'Vicky Jacoby Scholarship Application',
                  'author': 'Leander Chapter No. 73, Order of the Eastern Star',
                  'subject': 'Scholarship application for graduating seniors'})
doc.save(OUT, garbage=3, deflate=True)
print(len(fields), 'fields ->', OUT)
