import re
import unicodedata
from collections.abc import Mapping


LEXICON = {
    "solidarite": [
        "solidarité", "solidaire", "solidaires", "citoyen", "citoyenne",
        "citoyens", "citoyennes", "collectif", "collective", "communauté",
        "responsabilité", "contribuer", "engagement", "engagé", "engagée",
        "mobiliser", "agir", "action", "faire quelque chose", "concrètement",
        "participer", "bras ballants", "rester sans rien faire",
    ],
    "empathie": [
        "comprendre", "comprends", "comprend", "touché", "touchée", "ému",
        "émue", "sensible", "sensibles", "compassion", "souffrance", "douleur",
        "difficile", "épreuve", "parcours", "imagine", "imaginer",
        "à leur place", "humain", "humanité", "dignité", "humaniste", "prochain",
    ],
    "urgence": [
        "choqué", "choquée", "choc", "urgence", "urgent", "urgente",
        "insupportable", "inacceptable", "inadmissible", "catastrophe", "crise",
        "détresse", "immédiatement", "maintenant", "vite", "ne plus attendre",
        "ne faut plus attendre",
    ],
    "chaleur": [
        "accueil", "accueillir", "accueilli", "accueillie", "accueillons",
        "maison", "chez nous", "chez moi", "foyer", "chambre", "partage",
        "partager", "repas", "famille", "amitié", "convivialité", "ouvert",
        "ouverte", "bienvenue", "chaleureux", "chaleureuse", "bienveillance",
        "tendresse",
    ],
    "tristesse": [
        "triste", "tristes", "tristesse", "pleure", "pleurer", "larmes",
        "désolé", "désolée", "malheureux", "malheureuse", "terrible", "drame",
        "tragédie", "tragique", "mort", "mourir", "noyade", "noyé", "aylan",
        "guerre", "bombe", "destruction", "perdu", "perdue", "déraciné",
    ],
    "espoir": [
        "espoir", "espérer", "espère", "avenir", "futur", "possible", "mieux",
        "meilleur", "chance", "opportunité", "reconstruire", "reconstruction",
        "nouveau départ", "recommencer", "rêve", "rêver", "croire", "confiance",
        "optimiste", "positif", "positive",
    ],
    "determination": [
        "décidé", "décidée", "décision", "prêt", "prête", "prêts", "volonté",
        "résolu", "résolution", "fermement", "convaincu", "convaincue",
        "évidemment", "sans hésiter", "absolument", "totalement",
    ],
    "indignation": [
        "révolte", "révolté", "révoltée", "scandale", "scandaleux", "honte",
        "honteux", "intolérable", "injuste", "injustice", "colère", "furieux",
        "furieuse", "indigné", "indignée", "laisser faire", "abandon",
    ],
}

VOICE_MAP = {
    "solidarite": {"pitch": 0.1, "speed": 1.05, "energy": 0.7, "warmth": 0.7},
    "empathie": {"pitch": -0.1, "speed": 0.85, "energy": 0.4, "warmth": 0.9},
    "urgence": {"pitch": 0.3, "speed": 1.2, "energy": 0.85, "warmth": 0.3},
    "chaleur": {"pitch": 0.0, "speed": 0.9, "energy": 0.5, "warmth": 1.0},
    "tristesse": {"pitch": -0.3, "speed": 0.75, "energy": 0.3, "warmth": 0.6},
    "espoir": {"pitch": 0.2, "speed": 1.0, "energy": 0.6, "warmth": 0.8},
    "determination": {"pitch": 0.0, "speed": 0.95, "energy": 0.7, "warmth": 0.5},
    "indignation": {"pitch": 0.4, "speed": 1.15, "energy": 0.9, "warmth": 0.2},
}

FACE_MAP = {
    "solidarite": {"eyebrows": 0.3, "mouth": 0.3, "eyes": 0.8, "gaze": 1.0},
    "empathie": {"eyebrows": 0.1, "mouth": 0.0, "eyes": 0.6, "gaze": 0.8},
    "urgence": {"eyebrows": 0.6, "mouth": -0.2, "eyes": 1.0, "gaze": 1.0},
    "chaleur": {"eyebrows": 0.2, "mouth": 0.6, "eyes": 0.7, "gaze": 0.9},
    "tristesse": {"eyebrows": -0.3, "mouth": -0.5, "eyes": 0.3, "gaze": 0.3},
    "espoir": {"eyebrows": 0.4, "mouth": 0.4, "eyes": 0.9, "gaze": 0.7},
    "determination": {"eyebrows": -0.1, "mouth": 0.0, "eyes": 0.7, "gaze": 1.0},
    "indignation": {"eyebrows": -0.5, "mouth": -0.3, "eyes": 0.9, "gaze": 1.0},
}

NO_EVIDENCE = "non_determinee"

_NEGATION_TERMS = {
    "aucun", "aucune", "jamais", "ne", "ni", "n", "pas", "plus", "sans",
}
_TOKEN_PATTERN = re.compile(r"\w+")


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.casefold().replace("’", "'"))
    return "".join(char for char in decomposed if not unicodedata.combining(char))


_LEXICON_PATTERNS = {
    dimension: [
        re.compile(r"(?<!\w)" + re.escape(_normalize(keyword)) + r"(?!\w)")
        for keyword in sorted(set(keywords), key=len, reverse=True)
    ]
    for dimension, keywords in LEXICON.items()
}


def _is_negated(text: str, start: int) -> bool:
    if text.startswith(("ne plus attendre", "ne faut plus attendre"), start):
        return False
    preceding_tokens = _TOKEN_PATTERN.findall(text[max(0, start - 60):start])[-4:]
    return bool(_NEGATION_TERMS.intersection(preceding_tokens))


def score_dimensions(text: object) -> dict[str, float]:
    """Return heuristic [0, 1] context scores from French lexical evidence."""
    if not isinstance(text, str) or not text.strip():
        return {dimension: 0.0 for dimension in LEXICON}

    normalized = _normalize(text)
    scores = {}
    for dimension, patterns in _LEXICON_PATTERNS.items():
        matched_spans: list[tuple[int, int]] = []
        for pattern in patterns:
            for match in pattern.finditer(normalized):
                span = match.span()
                overlaps = any(
                    span[0] < end and span[1] > start
                    for start, end in matched_spans
                )
                if not overlaps and not _is_negated(normalized, span[0]):
                    matched_spans.append(span)
        hits = len(matched_spans)
        scores[dimension] = hits / (hits + 2.0) if hits else 0.0
    return scores


def dominant_dimension(scores: Mapping[str, float]) -> str:
    """Return the strongest dimension, or an explicit marker when none match."""
    if len(scores) == 0:
        return NO_EVIDENCE
    dimension, score = max(scores.items(), key=lambda item: item[1])
    return dimension if score > 0 else NO_EVIDENCE


def compute_avatar_params(scores: Mapping[str, float]) -> dict[str, float]:
    """Map lexical dimensions to bounded avatar controls using weighted means."""
    weights = {
        dimension: max(0.0, float(scores.get(dimension, 0.0)))
        for dimension in LEXICON
    }
    total_weight = sum(weights.values())
    if total_weight == 0:
        voice = {"pitch": 0.0, "speed": 1.0, "energy": 0.5, "warmth": 0.5}
        face = {"eyebrows": 0.0, "mouth": 0.0, "eyes": 0.5, "gaze": 0.5}
    else:
        voice = {
            parameter: sum(
                weights[dimension] * VOICE_MAP[dimension][parameter]
                for dimension in LEXICON
            ) / total_weight
            for parameter in VOICE_MAP["solidarite"]
        }
        face = {
            parameter: sum(
                weights[dimension] * FACE_MAP[dimension][parameter]
                for dimension in LEXICON
            ) / total_weight
            for parameter in FACE_MAP["solidarite"]
        }

    limits = {
        "voice_pitch": (-1.0, 1.0),
        "voice_speed": (0.5, 1.5),
        "voice_energy": (0.0, 1.0),
        "voice_warmth": (0.0, 1.0),
        "face_eyebrows": (-1.0, 1.0),
        "face_mouth": (-1.0, 1.0),
        "face_eyes": (0.0, 1.0),
        "face_gaze": (0.0, 1.0),
    }
    values = {
        **{f"voice_{key}": value for key, value in voice.items()},
        **{f"face_{key}": value for key, value in face.items()},
    }
    return {
        parameter: min(max(value, low), high)
        for parameter, value in values.items()
        for low, high in [limits[parameter]]
    }
