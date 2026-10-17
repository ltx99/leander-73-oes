# Scholarship application source

`form.html` is the design and wording of `vicky-jacoby-scholarship-application.pdf`.
`build.py` turns it into the fillable PDF (renders the page, then adds the typing
fields and Yes/No checkboxes over each box).

To update the form (for example, a new contact person):

1. Edit the wording in `form.html` (the contact appears in the callout box and in item 7).
2. Rebuild:

   ```
   pip install playwright pymupdf && playwright install chromium
   python3 src/scholarship-form/build.py vicky-jacoby-scholarship-application.pdf
   ```

Uses the Inter and Caladea fonts; install them first for an exact match.
Older versions of the PDF are kept in `archive/`.
