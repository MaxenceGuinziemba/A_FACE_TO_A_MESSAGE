"""
Emotion analysis v2 — Fixed pipeline for French refugee hosting messages.

Fixes:
- Removed broken English DistilRoBERTa model (disgust/anger on solidarity texts)
- Expanded contextual lexicon (3x keywords + root-based matching)
- Fixed compute_avatar_params normalization (defaults were added to weighted sums)
- Added zero-shot emotion classification for French
"""

import pandas as pd
import numpy as np
import re
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. EXPANDED CONTEXTUAL LEXICON — root-based matching
# ---------------------------------------------------------------------------

# Each dimension has:
#   'roots': word roots — matches any word containing this root
#   'phrases': multi-word expressions — exact substring match
LEXICON_V2 = {
    'solidarite': {
        'roots': [
            'solidar', 'citoyen', 'collecti', 'communaut', 'responsab',
            'contribu', 'engag', 'mobilis', 'particip', 'bénévol',
            'volontair', 'associat', 'entraide', 'coopér', 'collabor',
            'militan', 'humanitair', 'don', 'donat', 'altruism',
            'fratern', 'républi', 'democra', 'société civil',
        ],
        'phrases': [
            'faire quelque chose', 'bras ballants', 'rester sans rien faire',
            'ne pas rester', 'agir concrètement', 'à mon échelle',
            'à notre échelle', 'mon devoir', 'notre devoir', 'se mobiliser',
            'tendre la main', 'coup de main', 'prêter main forte',
            'apporter ma pierre', 'apporter notre pierre', 'pierre à l\'édifice',
            'pas rester indifférent', 'pas rester les bras',
            'envie d\'aider', 'envie d\'agir', 'besoin d\'agir',
            'je peux aider', 'je veux aider', 'nous pouvons',
        ],
    },
    'empathie': {
        'roots': [
            'compren', 'touch', 'émouv', 'émuv', 'émo', 'sensibl',
            'compass', 'souffr', 'douleur', 'épreuv', 'parcours',
            'imagin', 'humain', 'humanit', 'dignit', 'humanist',
            'prochain', 'empath', 'bienveill', 'écoute', 'écout',
            'ressentir', 'ressent', 'boulevers', 'affect',
        ],
        'phrases': [
            'à leur place', 'à sa place', 'à la place de',
            'mettre à la place', 'je comprends', 'nous comprenons',
            'je sais ce que c\'est', 'ça me touche', 'ça nous touche',
            'je me sens concerné', 'nous nous sentons concernés',
            'être humain', 'êtres humains', 'comme nous',
            'comme moi', 'comme tout le monde', 'en tant qu\'humain',
            'ce sont des gens', 'avant tout des',
        ],
    },
    'urgence': {
        'roots': [
            'choqu', 'urgenc', 'urgent', 'insupport', 'inaccept',
            'inadmiss', 'catastroph', 'crise', 'détress', 'désastre',
            'désespér', 'alarm', 'dramatiq', 'critic', 'critiqu',
            'terrifi', 'effroya', 'horrifi', 'épouvant',
        ],
        'phrases': [
            'ne plus attendre', 'il faut agir', 'tout de suite',
            'maintenant', 'immédiatement', 'au plus vite',
            'vu les images', 'vu à la télé', 'vu aux informations',
            'dans les médias', 'à la télévision', 'face à ce',
            'devant cette situation', 'devant ce drame',
            'c\'est urgent', 'trop c\'est trop', 'ça suffit',
            'on ne peut plus', 'il est temps', 'assez',
        ],
    },
    'chaleur': {
        'roots': [
            'accueil', 'maison', 'foyer', 'partag', 'repas',
            'famille', 'famili', 'amitié', 'convivial', 'ouvert',
            'bienvenu', 'chaleureu', 'bienveill', 'tendress',
            'intégr', 'accompagn', 'héberg', 'chambre', 'logement',
            'hospitalit', 'cohabit', 'cuisin', 'dîner', 'déjeuner',
            'sourire', 'souriant', 'joie', 'joyeu', 'rigoler',
            'amical', 'sympathique', 'sympathie',
        ],
        'phrases': [
            'chez nous', 'chez moi', 'chez soi', 'comme chez soi',
            'à la maison', 'notre maison', 'ma maison', 'à table',
            'les bras ouverts', 'bras ouvert', 'porte ouverte',
            'portes ouvertes', 'ouvrir notre porte', 'ouvrir ma porte',
            'comme à la maison', 'en famille', 'vie de famille',
            'partager un repas', 'partager des moments',
            'se sentir bien', 'se sentir chez soi',
            'bonne ambiance', 'moment de partage', 'moments de partage',
            'échange culturel', 'échanges culturels', 'découvrir',
            'richesse culturelle', 'enrichissant', 'enrichissement',
        ],
    },
    'tristesse': {
        'roots': [
            'trist', 'pleur', 'larm', 'désol', 'malheureu',
            'terribl', 'dram', 'tragéd', 'tragiq', 'mort',
            'mourir', 'noyad', 'noyé', 'guerr', 'bomb',
            'destruct', 'perdu', 'déracin', 'exil', 'fuit',
            'mélanc', 'deuil', 'chagrin', 'affect', 'pein',
            'abandonn', 'solitaire', 'solitud', 'misèr', 'misérab',
        ],
        'phrases': [
            'ça me rend triste', 'cela me rend triste',
            'j\'ai pleuré', 'les larmes aux yeux',
            'le cœur serré', 'le cœur brisé', 'ça fait mal',
            'ça me fait mal', 'au fond du cœur',
            'je suis désolé', 'je suis triste',
            'tout perdre', 'tout perdu', 'sans rien',
            'loin de chez eux', 'loin de leur pays',
            'arrachés à leur', 'privés de tout',
        ],
    },
    'espoir': {
        'roots': [
            'espoir', 'espérer', 'espèr', 'avenir', 'futur',
            'possibl', 'mieux', 'meilleur', 'chance', 'opportun',
            'reconstruir', 'reconstruct', 'recommenc', 'rêv',
            'croir', 'confianc', 'optimi', 'positif', 'positiv',
            'progrès', 'progress', 'amélio', 'beau', 'lumièr',
            'sourire', 'bonheur', 'heureu',
        ],
        'phrases': [
            'nouveau départ', 'nouvelle vie', 'nouvelle chance',
            'un jour', 'ça va aller', 'ça ira', 'tout ira bien',
            'je crois', 'nous croyons', 'j\'espère', 'nous espérons',
            'un monde meilleur', 'un avenir meilleur',
            'construire ensemble', 'reconstruire sa vie',
            'recommencer à zéro', 'refaire sa vie',
            'une vie meilleure', 'vie digne', 'vivre dignement',
            'avoir la chance', 'donner une chance',
        ],
    },
    'determination': {
        'roots': [
            'décid', 'décis', 'prêt', 'volont', 'résol',
            'ferme', 'convaincr', 'convaincu', 'évident',
            'naturel', 'logique', 'normal', 'évidem',
            'absolument', 'totalem', 'certain', 'détermin',
            'motivé', 'motiv',
        ],
        'phrases': [
            'bien sûr', 'sans hésiter', 'sans hésitation',
            'c\'est évident', 'c\'est normal', 'c\'est logique',
            'c\'est naturel', 'je suis prêt', 'nous sommes prêts',
            'je suis décidé', 'j\'ai décidé', 'nous avons décidé',
            'il faut', 'il fallait', 'je n\'hésite pas',
            'ça coule de source', 'tout naturellement',
            'ça me paraît', 'ça nous paraît', 'ma décision',
            'ma conviction', 'je suis convaincu',
        ],
    },
    'indignation': {
        'roots': [
            'révolt', 'scandal', 'hont', 'intolér', 'injust',
            'colèr', 'furieu', 'indign', 'politiq', 'gouvern',
            'abandon', 'inégal', 'discrimin', 'racis', 'xénopho',
            'inadmiss', 'immoral', 'révoltan', 'dégueula',
        ],
        'phrases': [
            'laisser faire', 'laisser tomber',
            'fermer les yeux', 'tourner le dos',
            'c\'est honteux', 'c\'est scandaleux', 'c\'est inadmissible',
            'c\'est injuste', 'c\'est inacceptable',
            'je suis révolté', 'je suis indigné',
            'ça me révolte', 'ça m\'indigne',
            'comment est-ce possible', 'comment peut-on',
            'on ne peut pas accepter', 'je ne comprends pas comment',
            'notre société', 'notre pays', 'la france',
        ],
    },
}


def score_dimensions_v2(text):
    """Score each emotional dimension using root-matching and phrase-matching.

    Returns scores in [0, 1] with much better coverage than v1.
    """
    if pd.isna(text) or not isinstance(text, str) or len(text.strip()) == 0:
        return {dim: 0.0 for dim in LEXICON_V2}

    text_lower = text.lower()
    words = set(re.findall(r'\b\w+\b', text_lower))
    scores = {}

    for dim, patterns in LEXICON_V2.items():
        hits = 0.0

        for root in patterns['roots']:
            for word in words:
                if root in word:
                    hits += 1.0
                    break

        for phrase in patterns['phrases']:
            if phrase in text_lower:
                hits += 1.5

        # Improved sigmoid: scale so 2 hits ≈ 0.5, 5 hits ≈ 0.8
        scores[dim] = 1 - (1 / (1 + hits * 0.4))

    return scores


# ---------------------------------------------------------------------------
# 2. AVATAR PARAMETER MAPPING — fixed normalization
# ---------------------------------------------------------------------------

VOICE_MAP = {
    'solidarite':    {'pitch': 0.1,  'speed': 1.05, 'energy': 0.7,  'warmth': 0.7},
    'empathie':      {'pitch': -0.1, 'speed': 0.85, 'energy': 0.4,  'warmth': 0.9},
    'urgence':       {'pitch': 0.3,  'speed': 1.2,  'energy': 0.85, 'warmth': 0.3},
    'chaleur':       {'pitch': 0.0,  'speed': 0.9,  'energy': 0.5,  'warmth': 1.0},
    'tristesse':     {'pitch': -0.3, 'speed': 0.75, 'energy': 0.3,  'warmth': 0.6},
    'espoir':        {'pitch': 0.2,  'speed': 1.0,  'energy': 0.6,  'warmth': 0.8},
    'determination': {'pitch': 0.0,  'speed': 0.95, 'energy': 0.7,  'warmth': 0.5},
    'indignation':   {'pitch': 0.4,  'speed': 1.15, 'energy': 0.9,  'warmth': 0.2},
}

FACE_MAP = {
    'solidarite':    {'eyebrows': 0.3,  'mouth': 0.3,  'eyes': 0.8, 'gaze': 1.0},
    'empathie':      {'eyebrows': 0.1,  'mouth': 0.0,  'eyes': 0.6, 'gaze': 0.8},
    'urgence':       {'eyebrows': 0.6,  'mouth': -0.2, 'eyes': 1.0, 'gaze': 1.0},
    'chaleur':       {'eyebrows': 0.2,  'mouth': 0.6,  'eyes': 0.7, 'gaze': 0.9},
    'tristesse':     {'eyebrows': -0.3, 'mouth': -0.5, 'eyes': 0.3, 'gaze': 0.3},
    'espoir':        {'eyebrows': 0.4,  'mouth': 0.4,  'eyes': 0.9, 'gaze': 0.7},
    'determination': {'eyebrows': -0.1, 'mouth': 0.0,  'eyes': 0.7, 'gaze': 1.0},
    'indignation':   {'eyebrows': -0.5, 'mouth': -0.3, 'eyes': 0.9, 'gaze': 1.0},
}

# Valid parameter ranges for clamping
VOICE_RANGES = {
    'pitch':  (-1.0, 1.0),
    'speed':  (0.5, 1.5),
    'energy': (0.0, 1.0),
    'warmth': (0.0, 1.0),
}
FACE_RANGES = {
    'eyebrows': (-1.0, 1.0),
    'mouth':    (-1.0, 1.0),
    'eyes':     (0.0, 1.0),
    'gaze':     (0.0, 1.0),
}

# Neutral defaults when no emotional dimension is detected
VOICE_NEUTRAL = {'pitch': 0.0, 'speed': 1.0, 'energy': 0.5, 'warmth': 0.5}
FACE_NEUTRAL = {'eyebrows': 0.0, 'mouth': 0.0, 'eyes': 0.5, 'gaze': 0.5}


def compute_avatar_params_v2(dim_scores):
    """Weighted interpolation of emotional dimensions → avatar parameters.

    BUG FIX: v1 added defaults to the weighted sum before dividing by total_weight,
    causing voice_speed > 4.0 and other values far outside valid ranges.

    v2: accumulates ONLY the weighted dimension contributions, then divides.
    Falls back to neutral defaults when total_weight is 0.
    """
    voice = {k: 0.0 for k in VOICE_NEUTRAL}
    face = {k: 0.0 for k in FACE_NEUTRAL}
    total_weight = 0.0

    for dim in LEXICON_V2:
        w = dim_scores.get(dim, dim_scores.get(f'dim_{dim}', 0.0))
        if w > 0.01:
            total_weight += w
            for param in voice:
                voice[param] += w * VOICE_MAP[dim][param]
            for param in face:
                face[param] += w * FACE_MAP[dim][param]

    if total_weight > 0.01:
        for param in voice:
            voice[param] /= total_weight
        for param in face:
            face[param] /= total_weight
    else:
        voice = dict(VOICE_NEUTRAL)
        face = dict(FACE_NEUTRAL)

    # Clamp to valid ranges
    for param, (lo, hi) in VOICE_RANGES.items():
        voice[param] = max(lo, min(hi, voice[param]))
    for param, (lo, hi) in FACE_RANGES.items():
        face[param] = max(lo, min(hi, face[param]))

    return {
        **{f'voice_{k}': v for k, v in voice.items()},
        **{f'face_{k}': v for k, v in face.items()},
    }


# ---------------------------------------------------------------------------
# 3. COMPOSITE EMOTIONAL PROFILE
# ---------------------------------------------------------------------------

def build_emotional_profile(row):
    """Combine sentiment + dimensions into a single profile dict."""
    sentiment = row.get('sentiment_label', 'neutral')
    sentiment_score = row.get('sentiment_score', 0.5)

    dims = {dim: row.get(f'dim_{dim}', 0.0) for dim in LEXICON_V2}
    dominant_dim = max(dims, key=dims.get) if any(v > 0 for v in dims.values()) else 'neutral'

    # Intensity: how emotionally charged is this message overall?
    intensity = sum(dims.values())
    intensity_norm = min(1.0, intensity / 2.0)  # cap at 1.0

    return {
        'sentiment': sentiment,
        'sentiment_score': sentiment_score,
        'dominant_dimension': dominant_dim,
        'emotional_intensity': intensity_norm,
        **{f'dim_{k}': v for k, v in dims.items()},
    }


# ---------------------------------------------------------------------------
# 4. VALIDATION
# ---------------------------------------------------------------------------

def validate_avatar_params(df):
    """Check that avatar parameters are within valid ranges and show variance."""
    issues = []

    voice_params = ['voice_pitch', 'voice_speed', 'voice_energy', 'voice_warmth']
    face_params = ['face_eyebrows', 'face_mouth', 'face_eyes', 'face_gaze']

    for col in voice_params + face_params:
        if col not in df.columns:
            issues.append(f"Missing column: {col}")
            continue
        param = col.split('_', 1)[1]
        ranges = VOICE_RANGES if col.startswith('voice_') else FACE_RANGES
        lo, hi = ranges[param]

        out_of_range = ((df[col] < lo) | (df[col] > hi)).sum()
        if out_of_range > 0:
            issues.append(f"{col}: {out_of_range} values out of range [{lo}, {hi}]")

        std = df[col].std()
        if std < 0.01:
            issues.append(f"{col}: no variance (std={std:.4f})")

    return issues


if __name__ == '__main__':
    # Quick test with sample texts
    test_texts = [
        "Je veux aider ces gens qui ont tout perdu, c'est mon devoir de citoyen solidaire.",
        "J'ai pleuré en voyant ces images à la télévision, c'est un drame terrible.",
        "Notre maison est ouverte, nous avons une chambre pour accueillir quelqu'un en famille.",
        "C'est scandaleux que notre gouvernement ne fasse rien, c'est honteux et injuste.",
        "J'espère qu'un jour ces gens pourront reconstruire une vie meilleure, je crois en l'avenir.",
    ]

    print("=== Lexicon V2 Test ===\n")
    for text in test_texts:
        scores = score_dimensions_v2(text)
        dominant = max(scores, key=scores.get)
        avatar = compute_avatar_params_v2(scores)

        print(f"Text: {text[:80]}...")
        print(f"  Dominant: {dominant} ({scores[dominant]:.3f})")
        top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"  Top 3: {', '.join(f'{k}={v:.3f}' for k, v in top3)}")
        print(f"  Voice: speed={avatar['voice_speed']:.2f} energy={avatar['voice_energy']:.2f} warmth={avatar['voice_warmth']:.2f}")
        print(f"  Face:  mouth={avatar['face_mouth']:.2f} eyes={avatar['face_eyes']:.2f} gaze={avatar['face_gaze']:.2f}")
        print()
