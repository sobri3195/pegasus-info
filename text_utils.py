"""
Text Utility Module - helpers for cleaning article text
"""

import re


def sanitize_text(text: str) -> str:
    """
    Normalize text by removing URLs and collapsing whitespace.

    Args:
        text: Raw input string

    Returns:
        Cleaned text string
    """
    if not text:
        return ""

    without_urls = re.sub(r"https?://\S+", "", text)
    collapsed = re.sub(r"\s+", " ", without_urls)

    return collapsed.strip()
