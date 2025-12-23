# signals.py
# This file defines probiotics-related signals and scoring rules

PROBIOTICS_KEYWORDS = [
    "probiotic",
    "probiotics",
    "live culture",
    "cfu",
    "gut health",
    "microbiome"
]

STRAIN_KEYWORDS = [
    "lactobacillus",
    "bifidobacterium",
    "streptococcus",
    "saccharomyces"
]

REGULATORY_KEYWORDS = [
    "gmp",
    "iso",
    "fssai",
    "pharma",
    "clinical"
]

APPLICATION_KEYWORDS = [
    "digestive",
    "gut",
    "immunity",
    "nutrition",
    "supplement"
]


def score_signals(found_signals):
    """
    Takes detected signals and calculates a probiotics involvement score.
    """

    score = 0

    if found_signals["core_product"]:
        score += 3

    if found_signals["strain_level"]:
        score += 2

    if found_signals["r_and_d"]:
        score += 2

    if found_signals["regulatory"]:
        score += 1

    if found_signals["marketing_only"]:
        score += 1

    if found_signals["vague_only"]:
        score -= 1

    if not found_signals["any_probiotic_mention"]:
        score -= 2

    return score
