# CONTEXT — A FACE TO A MESSAGE

## 🎯 Vision du projet
Transformer 20 000 témoignages de solidarité en avatars émotionnels 3D interactifs pour le Musée de l'immigration.

**Pipeline** : TEXTE → ÉMOTIONS (8 dimensions) → VOIX (TTS) → VISAGE ANIMÉ (3D) → INTERACTION VISITEUR

---

## 📂 Structure du repo

```
A_FACE_TO_A_MESSAGE/
├── src/
│   ├── analysis/emotion_v2.py      — Analyse émotions (lexique FR v2)
│   ├── tts/engine.py               — Moteur TTS (Edge TTS, 4 voix)
│   └── tts/text_prep.py            — Nettoyage texte (élisions, orthographe)
├── notebooks/
│   ├── 01_corpus.ipynb             — Chargement et nettoyage corpus
│   └── 02_emotion.ipynb            — Pipeline émotions v2
├── scripts/
│   ├── build_emotion_notebook.py   — Génère 02_emotion.ipynb
│   ├── build_player.py             — Génère player HTML audio
│   ├── build_wall.py               — Génère mur 2D SVG
│   └── build_wall_3d.py            — Génère mur 3D Three.js
├── data/
│   ├── processed/corpus.parquet    — 8 707 messages nettoyés
│   └── audio/demo/                 — 18 MP3 + 3 HTML (player, wall, wall_3d)
├── PROJET_HISTORIQUE.md            — ⚠️ METTRE À JOUR AVANT CHAQUE COMMIT
├── SUIVI.md                        — Journal détaillé jour par jour
└── README.md                       — Vue d'ensemble
```

---

## 🔑 Règles importantes

### 1. Avant CHAQUE commit/push
**⚠️ OBLIGATOIRE : Mettre à jour PROJET_HISTORIQUE.md**

Vérifier/ajouter dans PROJET_HISTORIQUE.md :
- [ ] Nouvelle phase si grosse feature
- [ ] Livrables ajoutés
- [ ] Métriques mises à jour (nb commits, lignes code, etc.)
- [ ] Roadmap actualisée (fait ✅ / en cours 🔄)
- [ ] Date de dernière mise à jour

### 2. Convention de commits
```
Type: Description courte

Body avec détails si nécessaire

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

Types : `Add`, `Fix`, `Update`, `Refactor`, `Remove`

### 3. Branch strategy
- `main` → docs uniquement
- `data-management` → code + données (branche active)

---

## 🎨 Paramètres Avatar (référence)

### Voice (4 params)
- `voice_pitch` : [-1, 1] → ±10Hz
- `voice_speed` : [0.5, 1.5] → ±15%
- `voice_energy` : [0, 1] → ±15% volume
- `voice_warmth` : [0, 1] → pause 200-600ms

### Face (4 params)
- `face_eyebrows` : [-1, 1] → hauteur/inclinaison
- `face_mouth` : [-1, 1] → frown ↔ smile
- `face_eyes` : [0, 1] → fermés ↔ écarquillés
- `face_gaze` : [0, 1] → bas ↔ haut

---

## 📚 Stack technique (référence rapide)

**NLP** : XLM-RoBERTa, spaCy, lexique FR v2 (~200 patterns)  
**TTS** : Edge TTS (4 voix), pyspellchecker  
**3D** : Three.js r160 (ES modules), GLTFLoader, FaceCap GLB (52 morph targets ARKit), Web Audio API lip sync, SVG animé  
**Data** : pandas, numpy, Jupyter  
**Perspectives** : Bark (TTS GPU), Unity, OpenCV, wawa-lipsync (15 visèmes)

---

## 🚦 État actuel (Nov 23)

### ✅ FAIT
- Corpus 8 707 messages
- Émotions v2 (71.1% couverture)
- TTS v3 (4 voix adultes, prosodie subtile)
- Avatar 2D SVG + 3D Three.js
- 18 démos audio

### 🔄 EN COURS
- Notebook 03_tts.ipynb (batch 8 707 messages)
- Mur 3D étendu (N visages)

### 🎯 NEXT
- Tests unitaires (pytest)
- Sync labiale précise
- Optimisation Three.js (LOD, instancing)

---

## 🔍 Points d'attention

### Bugs connus à éviter
- ❌ Ne PAS ajouter les défauts avant division dans `compute_avatar_params`
- ❌ Ne PAS utiliser pitch ±50Hz (voix enfantines)
- ❌ Ne PAS découper texte par phrases pour TTS (troncature)
- ❌ Ne PAS oublier `html.escape()` dans les builders HTML (XSS)

### Best practices
- ✅ Toujours tester sur 2-3 messages avant batch
- ✅ Vérifier variance des params avatar après changement
- ✅ Nettoyer `__pycache__` avant régénération
- ✅ Commit petit et fréquent, pas de gros diff 2000+ lignes

---

*Context créé le 23 novembre 2026 — À lire au début de chaque session*
