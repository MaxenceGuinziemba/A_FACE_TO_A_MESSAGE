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
