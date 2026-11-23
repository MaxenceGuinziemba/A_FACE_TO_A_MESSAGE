# A FACE TO A MESSAGE — Historique du projet

> **Vision** : Transformer 20 000 témoignages de solidarité en avatars émotionnels interactifs  
> **Installation** : Mur de visages 3D (4m × 1.15m) au Musée national de l'histoire de l'immigration  
> **Pipeline** : TEXTE → ÉMOTIONS → VOIX → VISAGE ANIMÉ → INTERACTION VISITEUR

---

## 🎯 Vision globale

Chaque témoignage devient un **visage sculptural** qui parle avec sa propre voix émotionnelle. Les visiteurs s'approchent du mur, un visage les interpelle, raconte son histoire. Le visage s'anime : la bouche bouge, les yeux expriment, les sourcils réagissent. L'émotion du témoignage se lit visuellement et s'entend vocalement.

**8 dimensions émotionnelles** mappées sur chaque avatar :
- Solidarité, Empathie, Chaleur, Espoir → expressions ouvertes, voix chaleureuses
- Urgence, Détermination, Indignation, Tristesse → expressions tendues, voix marquées

---

## 📚 Stack technique

### Core NLP & Emotion
- **XLM-RoBERTa** (Hugging Face) — validation multilingue zero-shot
- **Lexique contextuel français v2** — 8 dimensions, ~200 patterns (racines + phrases)
- **spaCy** — tokenisation, lemmatisation

### Text-to-Speech
- **Edge TTS** (Microsoft) — 4 voix adultes françaises (Vivienne, Denise, Remy, Henri)
- **pyspellchecker** — correction orthographique avec élisions françaises
- Prosodie SSML : pitch ±10Hz, speed ±15%, volume ±15%

### Avatar & Visuel
- **Three.js r128** — rendu 3D temps réel (WebGL)
- **SVG animé** — version 2D légère (MVP)
- Masques sculpturaux abstraits (style musée)

### Data & Infra
- **pandas, numpy** — traitement corpus (8 707 messages)
- **Jupyter** — notebooks interactifs
- **GitHub** — versioning, branche `data-management`

### Perspectives
- **Bark (Suno AI)** — TTS ultra-expressif (GPU required)
- **Unity/Blender** — avatars 3D photoréalistes (installation finale)
- **OpenCV/MediaPipe** — détection visiteurs

---

## 📅 Chronologie

### 🟢 Phase 1 : Setup & Données (Oct 10)
**Objectif** : Corpus propre, pipeline de base

✅ **Réalisé** :
- Repo GitHub structuré (`main` docs, `data-management` code)
- Corpus nettoyé : **8 707 messages** (3 sources Excel fusionnées)
- Notebooks Jupyter opérationnels
- Documentation complète (README, PROJECT, SETUP, DATA_PIPELINE)

📦 **Livrables** :
- `data/processed/corpus.parquet` (8 707 lignes)
- `notebooks/01_corpus.ipynb`

---

### 🔴 Phase 2 : Émotions v1 — Échec (Oct 10-19)
**Objectif** : Analyser émotions + générer paramètres avatar

❌ **Problèmes** :
1. **Modèle anglais sur texte français** → `disgust` et `anger` dominaient (absurde)
2. **Scores lexique trop faibles** → paramètres avatar figés à 0.0 / 0.5
3. **Bug normalisation** → `voice_speed = 4.2` (au lieu de max 1.5)

📊 **Stats v1 (bugguées)** :
- 64% positif, 18% neutre, 17% négatif ← faux négatifs massifs
- Couverture lexique : ~52% (faible)
- Paramètres avatar : variance = 0 (tous identiques)

---

### 🟢 Phase 3 : Émotions v2 — Correction (Oct 19 - Nov 22)
**Objectif** : Pipeline français fiable, paramètres qui varient

✅ **Corrections** :
1. **Modèle anglais supprimé** → remplacé par lexique v2 + validation XLM-RoBERTa
2. **Lexique v2 : 3× plus de patterns**
   - Racines (accueil → accueillir, accueilli, accueillant…)
   - Phrases multi-mots ("venir en aide", "ouvrir les portes")
   - ~25 racines + ~20 phrases par dimension
3. **Bug normalisation fixé**
   - v1 : défauts ajoutés au cumul → explosion des valeurs
   - v2 : cumul part de zéro, défauts seulement si aucune émotion
   - Clamping strict des plages

📊 **Stats v2 (corrigées)** :
- Couverture : **71.1%** (vs 52% en v1)
- Paramètres avatar : **variance > 0** pour tous les params
- Exemple : `voice_speed` ∈ [0.75, 1.20] (plage valide [0.5, 1.5])

📦 **Livrables** :
- `src/analysis/emotion_v2.py` — module réutilisable
- `notebooks/02_emotion.ipynb` — pipeline complet
- `data/processed/corpus_with_emotions.parquet`

---

### 🟢 Phase 4 : TTS v1-v3 (Nov 22)
**Objectif** : Voix françaises expressives, mapping émotions → prosodie

**TTS v1** (Nov 22 matin) :
- Edge TTS, 5 voix, prosodie large (pitch ±50Hz)
- ❌ **Problème** : voix sonnaient comme des enfants

**TTS v2** (Nov 22 après-midi) :
- Préparation texte (élisions, orthographe, genre)
- Détection genre (« mon mari » → voix féminine)
- ❌ **Problème** : troncature audio, découpage par phrases

**TTS v3** (Nov 22 soir) :
✅ **Solution finale** :
- Texte complet en un seul appel (plus de troncature)
- Prosodie **subtile** : pitch ±10Hz, speed ±15%
- 4 voix adultes (Eloise retirée, trop jeune)
- Correction orthographique des élisions (`l'imigration` → `l'immigration`)
- Voix réparties 11F/7M (hash des paramètres pour équilibre)

📦 **Livrables** :
- `src/tts/engine.py` — moteur TTS
- `src/tts/text_prep.py` — nettoyage + correction
- `data/audio/demo/` — 18 MP3 + player HTML interactif
- `scripts/build_player.py`

---

### 🟢 Phase 5 : Avatar 2D SVG (Nov 22 soir)
**Objectif** : MVP visage animé + audio

✅ **Réalisé** :
- 8 visages SVG (2×4 grid), un par dimension émotionnelle
- Animations : bouche suit la voix, clignements yeux, sourcils micro-mouvements
- Click → audio + animation synchronisée
- Panel texte slide-up avec témoignage

📦 **Livrables** :
- `data/audio/demo/wall.html` (975 KB avec audio embarqué)
- `scripts/build_wall.py`

---

### 🟢 Phase 6 : Avatar 3D Three.js (Nov 22-23)
**Objectif** : Mur de masques sculpturaux 3D photoréalistes

**v1** (Nov 22) :
- 8 masques 3D, halos colorés, fond noir immersif
- ❌ **Problème** : bouche et sourcils **invisibles** (géométrie z incorrecte)

**v2** (Nov 23) :
✅ **Corrections géométrie** :
- Tête aplatie (z-scale 0.55 vs 0.85) → features devant la surface
- Sourcils épais (0.05 vs 0.035), positionnés à z=0.58
- Bouche tube élargi (0.025 vs 0.02), z=0.58
- Yeux cavités creuses + pupilles lumineuses (z=0.62)
- Fix animation sourcils (baseY stocké, pas de drift)

✨ **Features** :
- Click → visage parle, bouche s'anime, halo pulse
- Idle breathing, float léger, rotation subtile
- Parallax camera (souris)
- Hover glow
- Rim lights (contour lumineux)

📦 **Livrables** :
- `data/audio/demo/wall_3d.html` (978 KB)
- `scripts/build_wall_3d.py`

---

## 🎨 Paramètres du système Avatar

### Voice (4 paramètres → TTS)
| Param | Plage | Mapping TTS | Exemple |
|-------|-------|-------------|---------|
| `voice_pitch` | [-1, 1] | ±10Hz | Urgence → +5Hz |
| `voice_speed` | [0.5, 1.5] | ±15% | Tristesse → 0.85 |
| `voice_energy` | [0, 1] | ±15% volume | Indignation → +12% |
| `voice_warmth` | [0, 1] | Pause 200-600ms | Chaleur → 550ms |

### Face (4 paramètres → Géométrie 3D)
| Param | Plage | Impact visuel | Exemple |
|-------|-------|---------------|---------|
| `face_eyebrows` | [-1, 1] | Hauteur + inclinaison | Tristesse → -0.3 (baissés) |
| `face_mouth` | [-1, 1] | Courbure (frown ↔ smile) | Espoir → +0.4 (sourire) |
| `face_eyes` | [0, 1] | Ouverture (fermés ↔ écarquillés) | Urgence → 0.9 (grands ouverts) |
| `face_gaze` | [0, 1] | Direction (bas ↔ haut) | Détermination → 1.0 (droit devant) |

### Mapping Émotions → Paramètres (poids)
Exemple : **Urgence**
```python
{
  'voice_pitch': +0.3,    # Voix plus aiguë
  'voice_speed': +0.2,    # Parle plus vite
  'voice_energy': +0.4,   # Volume élevé
  'face_eyebrows': +0.2,  # Sourcils levés
  'face_eyes': +0.5,      # Yeux écarquillés
  'face_gaze': +0.3       # Regard direct
}
```

---

## 🗓️ Roadmap

### ✅ Fait (Nov 23)
- [x] Corpus nettoyé (8 707 messages)
- [x] Pipeline émotions français fiable (v2)
- [x] TTS 4 voix françaises + prosodie subtile (v3)
- [x] Avatar 2D SVG animé (MVP)
- [x] Avatar 3D Three.js (mur de masques)
- [x] 18 démos audio + 2 players HTML
- [x] Audit sécurité (XSS fixé, code mort supprimé)
- [x] Système de contexte Claude (`.claude/` — instructions, context projet, skill update-history)

### 🔄 En cours
- [ ] **Notebook 03_tts.ipynb** — génération audio batch (8 707 messages, ~3h)
- [ ] **Mur 3D étendu** — passer de 8 visages à N visages (grille dynamique)

### 🎯 Prochaines étapes (court terme)
- [ ] Tests unitaires (pytest) pour `emotion_v2`, `text_prep`, `engine`
- [ ] Synchronisation labiale précise (phonèmes → visèmes)
- [ ] Variation des masques 3D (géométrie procédurale par message)
- [ ] Optimisation Three.js (LOD, instancing pour 100+ visages)

### 🚀 Vision long terme
- [ ] **Interaction visiteur** — détection présence (OpenCV/MediaPipe)
  - Visiteur approche → visages "s'éveillent"
  - Geste main → sélection visage
- [ ] **Bark TTS** (GPU) — voix ultra-expressives pour installation finale
- [ ] **Unity/Blender** — avatars 3D photoréalistes (si budget GPU)
- [ ] **Installation physique** — écran 4m × 1.15m, speakers spatialisés
- [ ] **Mode exposition** — playlist automatique, rotation messages
- [ ] **Analytics** — messages les plus écoutés, temps d'écoute moyen

---

## 🔬 Évolutions possibles

### Qualité audio
- **Bark (Suno AI)** — TTS state-of-the-art, émotions très marquées
  - Prérequis : GPU 8GB+ VRAM
  - Temps : ~8-10h pour 8 707 messages (vs 3h Edge TTS)
  - Qualité : voix presque humaines, intonations naturelles

### Visuel 3D
- **Unity HDRP** — rendu photoréaliste temps réel
  - Peau translucide, subsurface scattering
  - Morphing facial procédural (blend shapes)
- **Blender + Cycles** — pré-rendu vidéo haute qualité
  - 1 vidéo par message (lourd : ~10GB pour 8 707 vidéos)

### Interaction avancée
- **Kinect / RealSense** — tracking squelette visiteur
  - Visage "suit" du regard
  - Réaction à la distance (visiteur proche → visage parle plus fort)
- **Voice recognition** — visiteur peut poser questions
  - RAG (Retrieval-Augmented Generation) sur le corpus
  - LLM répond "en tant que" le message sélectionné

### Multi-sensorialité
- **Haptique** — vibrations sol (graves) pendant témoignages urgents
- **Lumière ambiante** — couleur pièce change selon émotion dominante
- **Olfactif** — diffusion subtile (controversé, à tester)

---

## 📊 Métriques du projet (Nov 23)

| Métrique | Valeur |
|----------|--------|
| **Messages corpus** | 8 707 |
| **Couverture émotionnelle** | 71.1% (1+ dimension détectée) |
| **Audio générés** | 18 démos (8 dimensions × 2-3 messages) |
| **Voix françaises** | 4 (Vivienne, Denise, Remy, Henri) |
| **Paramètres avatar** | 8 (4 voix + 4 face) |
| **Commits GitHub** | 10+ sur `data-management` |
| **Notebooks** | 2 (corpus + émotions) |
| **Modules Python** | 3 (`emotion_v2`, `engine`, `text_prep`) |
| **Librairies** | 15+ (transformers, edge-tts, three.js, pandas…) |
| **Lignes de code** | ~2 500 (Python + JS) |

---

## 🎓 Contexte académique

**Étudiant** : Maxence GUINZIEMBA-PROKOP  
**Institution** : Télécom Paris (Alternant IA/SD)  
**Année** : 2026-2027 (Semestre 1)  
**Type** : Projet recherche-création

**Encadrement** :
- Dana Diminescu — dana.diminescu@telecom-paris.fr
- Mickael Bouhier — mickael.bouhier@telecom-paris.fr

**Partenaires** :
- HI Paris! (centre interdisciplinaire Polytechnique-HEC)
- CNRS
- Musée national de l'histoire de l'immigration

**Corpus source** : Plateforme "Comme à la maison" (Singa)  
→ 20 000 témoignages anonymes de familles proposant d'héberger des réfugiés

---

## 🔗 Liens utiles

- **Repo GitHub** : `MaxenceGuinziemba/A_FACE_TO_A_MESSAGE`
- **Branch principale** : `data-management` (code + données)
- **Démos** :
  - `data/audio/demo/player.html` — player audio 18 cartes
  - `data/audio/demo/wall.html` — mur 2D SVG animé
  - `data/audio/demo/wall_3d.html` — mur 3D Three.js
- **Docs** :
  - `README.md` — vue d'ensemble
  - `SUIVI.md` — journal détaillé jour par jour
  - `docs/PROJECT.md` — contexte complet

---

*Document créé le 23 novembre 2026 — Dernière mise à jour : 23 novembre 2026*  
*Résumé historisé du projet A Face to a Message*
