# classifier.py
# Main probiotics classification logic

import sys
from urllib.parse import urljoin

from scraper_utils import fetch_page, extract_visible_text
from signals import (
    PROBIOTICS_KEYWORDS,
    STRAIN_KEYWORDS,
    REGULATORY_KEYWORDS,
    APPLICATION_KEYWORDS,
    score_signals
)

PAGES_TO_CHECK = [
    "",
    "/products",
    "/science",
    "/research",
    "/technology",
    "/about"
]


def classify_company(base_url):
    errors = []
    combined_text = ""
    pages_checked = []

    # -----------------------
    # Step 1: Collect text
    # -----------------------
    for path in PAGES_TO_CHECK:
        page_url = urljoin(base_url, path)
        html = fetch_page(page_url, errors)

        if not html:
            continue

        pages_checked.append(page_url)
        combined_text += " " + extract_visible_text(html).lower()

    # -----------------------
    # Step 2: Detect signals
    # -----------------------
    found_signals = {
        "any_probiotic_mention": False,
        "core_product": False,
        "strain_level": False,
        "r_and_d": False,
        "regulatory": False,
        "marketing_only": False,
        "vague_only": False
    }

    # Basic probiotics presence
    for word in PROBIOTICS_KEYWORDS:
        if word in combined_text:
            found_signals["any_probiotic_mention"] = True

    # Strain-level detection
    for strain in STRAIN_KEYWORDS:
        if strain in combined_text:
            found_signals["strain_level"] = True

    # R&D / science
    if "research" in combined_text or "science" in combined_text:
        found_signals["r_and_d"] = True

    # Regulatory
    for reg in REGULATORY_KEYWORDS:
        if reg in combined_text:
            found_signals["regulatory"] = True

    # Application areas
    for app in APPLICATION_KEYWORDS:
        if app in combined_text:
            found_signals["core_product"] = True

    # Marketing-only heuristic
    if found_signals["any_probiotic_mention"] and not (
        found_signals["strain_level"] or found_signals["r_and_d"]
    ):
        found_signals["marketing_only"] = True

    if found_signals["any_probiotic_mention"] and not found_signals["core_product"]:
        found_signals["vague_only"] = True

    # -----------------------
    # Step 3: Score & classify
    # -----------------------
    score = score_signals(found_signals)

    if score >= 7:
        classification = "Probiotics-focused"
    elif score >= 3:
        classification = "Probiotics-adjacent"
    else:
        classification = "Not relevant"

    # -----------------------
    # Final output
    # -----------------------
    return {
        "classification": classification,
        "score": score,
        "signals_detected": found_signals,
        "pages_checked": pages_checked,
        "errors": errors
    }


# -----------------------
# Entry point
# -----------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python classifier.py <company_website_url>")
        sys.exit(1)

    website = sys.argv[1]
    result = classify_company(website)

    from pprint import pprint
    pprint(result)
