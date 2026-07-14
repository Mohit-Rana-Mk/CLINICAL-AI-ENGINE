import re
import logging

logger = logging.getLogger(__name__)


class DocumentCleaner:
    def __init__(self, extra_patterns: list = None):
        """
        Args:
            extra_patterns: Optional list of additional regex strings to treat
                            as header/footer noise and remove.
        """
        self.page_number_patterns = [
            r'(?i)\bpage\s+\d+\s+of\s+\d+\b',  # must come before the simpler pattern below
            r'(?i)\bpage\s+\d+\b',
            r'^\s*-\s*\d+\s*-\s*$',
        ]

        self.header_footer_patterns = [
            r'(?i)\bconfidential\b',
            r'(?i)\bpatient\s+record\b',
            r'(?i)\bmedical\s+history\b',
            r'^\s*-{3,}\s*$',  # standalone only — avoids matching |---| in markdown tables
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            r'\b\d{1,2}:\d{2}\s*(?:AM|PM)\b',
            r'(?i)\bregistered?\s+on\s*:',
            r'(?i)\bcollected\s+on\s*:',
            r'(?i)\breceived\s+on\s*:',
            r'(?i)\breported\s+on\s*:',
            r'(?i)\breg(?:istration)?\s*\.?\s*no\.?\s*:',
            r'(?i)\breferred\s+by\s*:',
        ]

        if extra_patterns:
            self.header_footer_patterns.extend(extra_patterns)

        self._markdown_cleanup = [
            (r'<[^>]+>',    ' '),
            (r'\*+',        ''),
            (r'^#{1,6}\s*', ''),
            (r'\|',         ' '),
        ]

    def clean_text(self, text: str) -> str:
        """
        Removes page numbers, headers/footers, Markdown formatting,
        non-ASCII characters, and normalizes whitespace.
        """
        if not text:
            return ""

        original_len = len(text)

        for pattern, replacement in self._markdown_cleanup:
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

        for pattern in self.page_number_patterns:
            text = re.sub(pattern, '', text, flags=re.MULTILINE)

        for pattern in self.header_footer_patterns:
            text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)

        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{2,}', '\n\n', text)

        result = text.strip()
        logger.debug(f"DocumentCleaner: removed {original_len - len(result)} chars.")
        return result
