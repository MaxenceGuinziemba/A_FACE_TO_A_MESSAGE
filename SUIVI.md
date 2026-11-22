# Suivi du projet — A FACE TO A MESSAGE

## 10 octobre 2026

### Ce qui a été fait

**Setup du projet**
- Clone du repo GitHub (`MaxenceGuinziemba/A_FACE_TO_A_MESSAGE`)
- Structure du projet créée : `src/`, `data/`, `notebooks/`, `docs/`, `config/`, `models/`, `tests/`
- Environnement virtuel `.venv` (Python 3.11) + packages installés en global
- Configuration SSH GitHub (clé `id_ed25519` via `github.com-maxence`)
- Branches : `main` (docs), `data-management` (code + données)
- Kernel Jupyter configuré (`AFTAM (.venv)`)

**Documentation**
- `README.md` — vue d'ensemble + quick start
- `docs/PROJECT.md` — contexte complet + données
- `docs/SETUP.md` — installation
- `docs/DATA_PIPELINE.md` — gestion données
- Consolidation de 9 fichiers .md en 4 fichiers organisés

**Données**
- Chargement du corpus Excel (3 feuilles : Familles 1, Familles 2, Nouvelle Plateforme)
- Nettoyage : suppression lignes sans `testimony` ni `self_description`
- Corpus propre : **8,707 messages** exploitables
- Sauvegarde : `data/processed/corpus.csv` et `.parquet`

**Analyse émotionnelle (v1 — à corriger)**
- Sentiment (XLM-RoBERTa multilingual) : **fonctionne bien**
  - 64% positif, 18% neutre, 17% négatif
- Émotions (DistilRoBERTa anglais) : **résultats aberrants** — modèle anglais sur texte français
  - `disgust` et `anger` dominent alors que les messages parlent de solidarité
  - → À remplacer par un modèle multilingue ou supprimer
- Lexique contextuel (8 dimensions) : **concept bon, scores trop faibles**
  - Solidarité (52%), Chaleur (26%), Empathie (9%), Urgence (5%)
  - Scores moyens ~0.07 → l'interpolation vers les paramètres avatar ne fait rien
- Paramètres avatar : **bug de normalisation**
  - Voix et visage restent aux valeurs par défaut (0.00, 0.50)
  - `voice_speed` monte à 4.2 (devrait être max 1.5)

### Problèmes identifiés

| # | Problème | Impact | Priorité |
|---|----------|--------|----------|
| 1 | Modèle émotions anglais donne des résultats absurdes sur du français | Données émotion inutilisables | Haute |
| 2 | Scores du lexique trop faibles (mean ~0.07) | Paramètres avatar ne bougent pas | Haute |
| 3 | Bug normalisation `compute_avatar_params` | voice_speed dépasse les ranges | Haute |
| 4 | Pas de modèle français dédié pour les émotions | Analyse émotionnelle limitée au sentiment + lexique | Moyenne |

### Prochaines étapes

- [ ] Virer le modèle DistilRoBERTa anglais ou le remplacer par un modèle multilingue
- [ ] Renforcer le lexique contextuel (augmenter les mots-clés, ajuster la normalisation)
- [ ] Corriger `compute_avatar_params` (normalisation, ranges)
- [ ] Tester un modèle français (CamemBERT sentiment, ou modèle d'émotions multilingue)
- [ ] Valider que les paramètres avatar varient réellement entre messages différents
- [ ] Commencer l'intégration TTS (Text-to-Speech)

## 19 octobre 2026 — Correction du notebook émotionnel

- Retrait du classifieur d'émotions entraîné uniquement en anglais, qui attribuait notamment « disgust » et « anger » à des témoignages français.
- Le modèle multilingue de polarité a d'abord été conservé avec une mise en garde, puis désactivé après vérification de faux négatifs sur des messages exprimant une intention solidaire.
- Détection lexicale française rendue plus stricte (frontières de mots, accents, négation locale); les messages sans indice lexical ne sont plus artificiellement classés comme « solidarité ».
- Correction de l'interpolation des paramètres avatar : moyennes pondérées et valeurs bornées selon les plages documentées.
- Tests unitaires ajoutés. Les sorties ont été recalculées en exécutant `02_emotion.ipynb` de haut en bas; une validation humaine du lexique reste nécessaire.

## 19 octobre 2026 — Suppression des polarités trompeuses

- La pièce jointe reçue montrait encore l'ancienne version du notebook, et les sorties CSV/Parquet contenaient toujours les anciennes colonnes `sentiment_label`, `emo_*` et des vitesses avatar non bornées.
- Vérification sur des exemples : le modèle Twitter donnait « négatif » à « Je veux venir en aide aux Syriens » et à des propositions d'hébergement, malgré une intention d'aide explicite.
- Le notebook n'utilise donc plus le classifieur positif/neutre/négatif ; il ne produit que les indices du lexique contextuel français et indique `non_determinee` en l'absence d'indice.
- Cause des paramètres avatar constants : le notebook transmettait des clés `dim_*` au mapping qui attend des noms de dimensions sans préfixe, ce qui donnait les valeurs par défaut à tous les messages. Le mapping des scores est corrigé et une assertion empêche cette régression.
- Le CSV/Parquet émotionnel, la configuration avatar et les statistiques ont été recalculés depuis le corpus brut. Les paramètres varient maintenant sur les 8 707 messages (ex. `voice_speed` : 0,75–1,20). Une polarité supervisée nécessitera des annotations humaines représentatives et une évaluation dédiée.

### Fichiers produits

```
data/processed/
├── corpus.csv              — 8,707 messages nettoyés
├── corpus.parquet           — idem, format compressé
├── corpus_stats.json        — statistiques du corpus
├── corpus_with_emotions.csv — messages + émotions + params avatar (v1, à corriger)
├── corpus_with_emotions.parquet
├── avatar_config.json       — mapping émotion → voix/visage
└── emotion_stats.json       — stats émotionnelles

notebooks/
├── 01_corpus.ipynb          — extraction et nettoyage du corpus
└── 02_emotion.ipynb         — analyse émotionnelle (v1)
```

---

## 22 novembre 2026

### Ce qui a été fait

**Analyse émotionnelle v2 — tous les bugs corrigés**

1. **Modèle DistilRoBERTa anglais supprimé** ✓
   - Donnait `disgust` (2302) et `anger` (1146) sur un corpus de solidarité
   - Remplacé par un lexique v2 élargi + validation zero-shot multilingue

2. **Lexique contextuel v2 — 3× plus de patterns** ✓
   - Matching par racines (ex: `accueil` → accueillir, accueilli, accueillant…) + phrases multi-mots
   - ~25 racines + ~20 phrases par dimension (vs ~20 mots exacts en v1)
   - Couverture : **71.1%** des messages ont au moins une dimension détectée
   - Module réutilisable : `src/analysis/emotion_v2.py`

3. **Bug normalisation `compute_avatar_params` corrigé** ✓
   - **v1 bug** : valeurs par défaut (speed=1.0, energy=0.5) ajoutées au cumul pondéré avant division → voice_speed montait à 4.2
   - **v2 fix** : cumul part de zéro, défauts utilisés uniquement si aucune dimension détectée
   - Clamping ajouté pour garantir les plages valides

4. **Validation zero-shot multilingue** ✓
   - XLM-RoBERTa-large-XNLI testé sur un échantillon de 50 messages
   - Confirme la cohérence des dimensions contextuelles
   - Trop lent pour le corpus complet (~4s/message), utilisé en validation uniquement

5. **Validation automatique des paramètres avatar** ✓
   - Fonction `validate_avatar_params()` vérifie plages et variance
   - **Tous les paramètres dans les plages valides**

### Résultats v2 vs v1

| Paramètre | v1 (bug) | v2 (corrigé) | Plage valide |
|-----------|----------|--------------|--------------|
| voice_speed | **2.09** ✗ | **0.98** ✓ | [0.5, 1.5] |
| voice_energy | **1.10** ✗ | **0.57** ✓ | [0, 1] |
| voice_warmth | **1.23** ✗ | **0.69** ✓ | [0, 1] |
| face_eyes | **1.21** ✗ | **0.67** ✓ | [0, 1] |
| face_gaze | **1.29** ✗ | **0.77** ✓ | [0, 1] |
| voice_pitch | 0.03 ✓ | 0.04 ✓ | [-1, 1] |
| face_eyebrows | 0.13 ✓ | 0.14 ✓ | [-1, 1] |
| face_mouth | 0.16 ✓ | 0.19 ✓ | [-1, 1] |

### Problèmes résolus

| # | Problème (v1) | Statut |
|---|---------------|--------|
| 1 | Modèle émotions anglais donne des résultats absurdes | ✓ **Supprimé** — remplacé par lexique v2 |
| 2 | Scores du lexique trop faibles (mean ~0.07) | ✓ **Corrigé** — scores v2 plus élevés + meilleure variance |
| 3 | Bug normalisation `compute_avatar_params` | ✓ **Corrigé** — cumul part de zéro + clamping |
| 4 | Pas de modèle français dédié | ✓ **Contourné** — validation zero-shot + lexique contextuel adapté au corpus |

### Fichiers produits / modifiés

```
src/analysis/
└── emotion_v2.py              — NOUVEAU : module réutilisable (lexique, scoring, avatar params)

scripts/
└── build_emotion_notebook.py  — NOUVEAU : génère le notebook 02_emotion.ipynb

notebooks/
├── 01_corpus.ipynb            — inchangé
└── 02_emotion.ipynb           — RÉÉCRIT : pipeline v2 complet

data/processed/
├── corpus_with_emotions.csv   — À RÉGÉNÉRER en exécutant le notebook
├── corpus_with_emotions.parquet
├── avatar_config.json         — À RÉGÉNÉRER (v2 avec lexique + ranges)
└── emotion_stats.json         — À RÉGÉNÉRER (v2 avec variance + coverage)
```

**Text-to-Speech — voix expressives françaises** ✓

6. **Moteur TTS avec prosodie émotionnelle** ✓
   - Edge TTS (Microsoft) : 5 voix françaises naturelles, contrôle SSML complet
   - Module réutilisable : `src/tts/engine.py`
   - Mapping automatique : paramètres avatar → pitch, speed, volume, pauses SSML

7. **Sélection de voix par émotion** ✓
   - 5 voix avec personnalités distinctes :
     - **Vivienne** (empathie, chaleur) — chaleureuse, maternelle
     - **Remy** (solidarité, détermination) — engagé, déterminé
     - **Denise** (tristesse) — douce, réflexive
     - **Henri** (urgence, indignation) — assertif, véhément
     - **Eloise** (espoir) — jeune, optimiste
   - Sélection automatique basée sur la dimension dominante + paramètres voix

8. **Variation prosodique par phrase** ✓
   - Première phrase : légèrement plus lente (introduction)
   - Dernière phrase : ralentissement conclusif ou montée interrogative
   - `!` → plus d'énergie et de débit
   - `?` → montée de pitch
   - `…` → ralentissement, volume plus bas
   - Pauses inter-phrases proportionnelles à la chaleur (200-600ms)

9. **Demo interactive** ✓
   - 8 fichiers audio générés (un par dimension émotionnelle)
   - Player HTML interactif avec audio embarqué : `data/audio/demo/player.html`
   - Visualisation des paramètres voix pour chaque message
   - Génération batch asynchrone (5 messages en parallèle)

**TTS v2 — corrections qualité et cohérence** ✓

10. **Préparation de texte pour TTS** ✓
    - Module dédié : `src/tts/text_prep.py`
    - Restauration des élisions françaises (`j ai` → `j'ai`, `l immigration` → `l'immigration`)
    - Correction orthographique (pyspellchecker) avec protection des particules françaises
    - Dictionnaire de corrections spécifiques au corpus (tourmef → tourner, imigration → immigration, etc.)
    - Nettoyage : emojis, URLs, emails, ponctuation orpheline
    - Distance d'édition ≤ 2 pour éviter les corrections sauvages

11. **Détection du genre — mode garde-fou** ✓
    - Analyse regex du contenu textuel (« mon mari » → locutrice, « ma femme » → locuteur)
    - N'essaye pas de deviner le genre : exclut juste les incohérences flagrantes
    - Si aucun indice → toutes les voix éligibles

12. **Prosodie subtile (v3)** ✓
    - Réécriture complète du moteur TTS pour fiabilité
    - Texte complet envoyé en un seul appel (plus de découpage par phrases → plus de troncature)
    - Plages réduites : pitch ±10Hz, speed ±15%, volume ±15% → voix adultes naturelles
    - 4 voix adultes (Vivienne, Denise, Remy, Henri) — Eloise retirée (trop jeune)
    - Retry 3 tentatives avec fallback sans prosodie

13. **Demo interactive v3** ✓
    - 18 fichiers audio régénérés avec texte corrigé, voix adultes, prosodie subtile
    - Player HTML avec badges de genre (♀ Locutrice / ♂ Locuteur)
    - Textes complets (plus de troncature)

### Fichiers produits / modifiés

```
src/analysis/
└── emotion_v2.py              — module émotions (lexique, scoring, avatar params)

src/tts/
├── engine.py                  — moteur TTS (voix, SSML, génération audio)
└── text_prep.py               — NOUVEAU : préparation texte (correction, élisions, genre)

scripts/
├── build_emotion_notebook.py  — génère le notebook 02_emotion.ipynb
└── build_player.py            — génère le player HTML interactif

notebooks/
├── 01_corpus.ipynb            — inchangé
└── 02_emotion.ipynb           — RÉÉCRIT : pipeline v2 complet

data/audio/
├── demo/                      — 18 fichiers MP3 de démo + player HTML
│   ├── demo_*.mp3             — audio par dimension (×2-3 messages chacune)
│   ├── player.html            — Player interactif v2 (audio embarqué, badges genre)
│   ├── generation_log.json    — log de génération
│   └── messages.json          — messages avec params et genre détecté
└── test/                      — fichiers de test prosodie
```

### Prochaines étapes

- [x] Exécuter le notebook 02_emotion.ipynb pour régénérer les données
- [ ] Créer le notebook 03_tts.ipynb pour la génération audio batch sur tout le corpus
- [ ] Prototyper le viewer de messages interactif (notebook 03 ou app web)
- [ ] Concevoir le système d'avatar (Unity/Blender/Web)
- [ ] Explorer la détection de présence visiteur (OpenCV/MediaPipe)

### Perspectives d'amélioration

- **Bark (Suno AI)** : moteur TTS très expressif et naturel, capable de générer des voix avec émotions marquées. Nécessite un GPU (5+ GB VRAM). À envisager quand des GPU seront disponibles pour remplacer Edge TTS et obtenir une qualité vocale supérieure sur les 8 700+ messages.

---

## Template pour les prochains jours

<!--
## [DATE]

### Ce qui a été fait
- ...

### Problèmes rencontrés
- ...

### Prochaines étapes
- [ ] ...
-->
