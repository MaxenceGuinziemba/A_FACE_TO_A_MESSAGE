"""
Text preparation for TTS — clean, correct, and analyze French text
before sending it to the speech engine.
"""

import re
from spellchecker import SpellChecker

_spell = SpellChecker(language='fr')

# Common corpus-specific corrections (manual overrides)
KNOWN_CORRECTIONS = {
    'tourmef': 'tourner',
    'imigration': 'immigration',
    'oportunité': 'opportunité',
    'réfugiées': 'réfugiées',  # keep as-is (valid)
    'acceuilir': 'accueillir',
    'acceuillir': 'accueillir',
    'acceuil': 'accueil',
    'bénévolat': 'bénévolat',  # keep
    'bénévol': 'bénévole',
    'solidairé': 'solidarité',
    'humanitère': 'humanitaire',
    'hospitalié': 'hospitalité',
    'hébergment': 'hébergement',
    'apartement': 'appartement',
    'apartment': 'appartement',
}

# French single-letter words and elision prefixes — never "correct" these
FRENCH_PARTICLES = {
    'j', 'l', 'n', 'd', 's', 'm', 't', 'c', 'y', 'a', 'à', 'ô', 'é',
    'qu', 'jusqu', 'lorsqu', 'puisqu', 'quelqu',
}

# Words to never correct (proper nouns, abbreviations, domain-specific)
SKIP_WORDS = {
    'calm', 'singa', 'france', 'paris', 'syrie', 'calais',
    'inter', 'etc', 'km', 'm2', 'ok', 'ps', 'nb',
    'internet', 'google', 'facebook', 'twitter',
}


def restore_elisions(text: str) -> str:
    """Restore French elisions that may have been stripped.

    "j ai" → "j'ai", "l immigration" → "l'immigration", etc.
    """
    # Pattern: single elision letter + space + vowel-starting word
    text = re.sub(
        r"\b([jlndsmtc])\s+([aeéèêëiïoôuùûyh])",
        r"\1'\2",
        text,
        flags=re.IGNORECASE,
    )
    # "qu il" → "qu'il", "jusqu à" → "jusqu'à"
    text = re.sub(
        r"\b(qu|jusqu|lorsqu|puisqu|quelqu)\s+([aeéèêëiïoôuùûyh])",
        r"\1'\2",
        text,
        flags=re.IGNORECASE,
    )
    return text


def correct_spelling(text: str) -> str:
    """Correct spelling errors while protecting French language features."""
    words = re.findall(r"[\w']+|[^\w\s]", text)
    result = []

    for word in words:
        lower = word.lower().strip("'")

        # Skip: punctuation, short words, particles, known-good words
        if len(lower) <= 2 or lower in FRENCH_PARTICLES or lower in SKIP_WORDS:
            result.append(word)
            continue

        # Check manual corrections first
        if lower in KNOWN_CORRECTIONS:
            corrected = KNOWN_CORRECTIONS[lower]
            # Preserve original capitalization
            if word[0].isupper():
                corrected = corrected[0].upper() + corrected[1:]
            result.append(corrected)
            continue

        # For elided words (l'imigration), correct the part after the apostrophe
        if "'" in word:
            parts = word.split("'", 1)
            if len(parts) == 2 and len(parts[1]) >= 4:
                suffix = parts[1].lower()
                if suffix in KNOWN_CORRECTIONS:
                    result.append(f"{parts[0]}'{KNOWN_CORRECTIONS[suffix]}")
                    continue
                if suffix not in _spell:
                    corr = _spell.correction(suffix)
                    if corr and corr != suffix and _edit_distance(suffix, corr) <= 2:
                        result.append(f"{parts[0]}'{corr}")
                        continue
            result.append(word)
            continue

        # Only correct words the spell checker flags AND has a good candidate for
        if lower not in _spell and len(lower) >= 4:
            correction = _spell.correction(lower)
            if correction and correction != lower:
                # Only accept if edit distance is small (avoid wild corrections)
                dist = _edit_distance(lower, correction)
                if dist <= 2:
                    if word[0].isupper():
                        correction = correction[0].upper() + correction[1:]
                    result.append(correction)
                    continue

        result.append(word)

    # Rejoin without adding spaces before punctuation
    out = []
    for word in result:
        if out and word and word[0] not in '.,;:!?…)]\'"' and (not out or out[-1] not in '(\'"'):
            out.append(' ')
        out.append(word)
    return ''.join(out)


def _edit_distance(a: str, b: str) -> int:
    """Simple Levenshtein distance."""
    if len(a) < len(b):
        return _edit_distance(b, a)
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(
                prev[j + 1] + 1,
                curr[j] + 1,
                prev[j] + (0 if ca == cb else 1),
            ))
        prev = curr
    return prev[len(b)]


def clean_for_tts(text: str) -> str:
    """Full text cleaning pipeline for TTS."""
    if not text or not isinstance(text, str):
        return ''

    # Remove emojis and special Unicode
    text = re.sub(
        r'[\U00010000-\U0010ffff]|[☀-➿]|[⌀-⏿]|'
        r'[⭐-⭕]|[‍️]|[❝❞❤️✓✗⭐🎯🏗️🛠️📊📖📅🤝💡🎭]',
        '', text
    )

    # Remove URLs and emails
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\S+@\S+\.\S+', '', text)

    # Normalize quotes
    text = text.replace('«', '').replace('»', '').replace('"', '').replace('"', '')
    text = text.replace("''", "'")

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Restore elisions
    text = restore_elisions(text)

    # Correct spelling
    text = correct_spelling(text)

    # Clean up punctuation spacing
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    text = re.sub(r'([.,;:!?])(\w)', r'\1 \2', text)

    # Remove orphan punctuation
    text = re.sub(r'^\s*[.,;:!?]\s*', '', text)

    # Ensure text ends with punctuation (better TTS cadence)
    text = text.strip()
    if text and text[-1] not in '.!?…':
        text += '.'

    return text


# ---------------------------------------------------------------------------
# Gender detection
# ---------------------------------------------------------------------------

FEMALE_PATTERNS = [
    r'\bmon mari\b', r'\bmon conjoint\b', r'\bmon compagnon\b', r'\bmon copain\b',
    r'\ben tant que mère\b', r'\ben tant que maman\b', r'\ben tant que femme\b',
    r'\bje suis (une |la )?mère\b', r'\bje suis (une |la )?maman\b',
    r'\bje suis une femme\b', r'\bje suis enceinte\b',
    r'\bmaman\b.*\benfants?\b',
    r'\bmon homme\b',
]

MALE_PATTERNS = [
    r'\bma femme\b', r'\bma conjointe\b', r'\bma compagne\b', r'\bma copine\b',
    r'\ben tant que père\b', r'\ben tant que papa\b', r'\ben tant qu\'homme\b',
    r'\bje suis (un |le )?père\b', r'\bje suis (un |le )?papa\b',
    r'\bje suis un homme\b',
    r'\bma chérie\b',
]


def detect_speaker_gender(text: str) -> str:
    """Detect likely speaker gender from text content.

    Returns: 'female', 'male', or 'unknown'
    """
    if not text:
        return 'unknown'

    text_lower = text.lower()

    female_score = sum(1 for p in FEMALE_PATTERNS if re.search(p, text_lower))
    male_score = sum(1 for p in MALE_PATTERNS if re.search(p, text_lower))

    if female_score > male_score:
        return 'female'
    elif male_score > female_score:
        return 'male'
    return 'unknown'


def prepare_for_tts(text: str) -> dict:
    """Full preparation pipeline: clean text + detect gender.

    Returns dict with 'text' (cleaned) and 'gender' (detected).
    """
    gender = detect_speaker_gender(text)
    cleaned = clean_for_tts(text)
    return {
        'text': cleaned,
        'gender': gender,
        'original_length': len(text) if text else 0,
        'cleaned_length': len(cleaned),
    }
