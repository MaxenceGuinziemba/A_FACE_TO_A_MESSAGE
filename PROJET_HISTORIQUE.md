# A FACE TO A MESSAGE — Historique du projet

> **Objectif** : Transformer 20 000 témoignages de solidarité en avatars émotionnels interactifs  
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

| Catégorie | Technologies & Usages |
|-----------|----------------------|
| **Core NLP & Emotion** | **XLM-RoBERTa** (Hugging Face) : validation multilingue zero-shot<br>**Lexique contextuel français v2** : 8 dimensions (cf au dessus)<br>**spaCy** : tokenisation et lemmatisation |
| **Text-to-Speech** | **Edge TTS** (Microsoft) : 4 voix adultes françaises (Vivienne, Denise, Remy, Henri)<br>**pyspellchecker** : correction orthographique<br>Prosodie SSML : pitch ±10Hz, speed ±15%, volume ±15% |
| **Avatar & Visuel** | **Three.js r128** (script tags, compatible file://) : rendu 3D temps réel (WebGL)<br>**GLTFLoader** + modèle **FaceCap** (52 ARKit morph targets)<br>**Web Audio API** : lip sync amplitude en temps réel<br>**SVG animé** : version 2D légère (MVP) |
| **Data & Infra** | **pandas, numpy** : traitement du corpus de 8 707 messages<br>**Jupyter** : notebooks interactifs |
| **Perspectives** | **Bark (Suno AI)** : synthèse vocale ultra-expressive (nécessite un GPU)<br>**Unity / Blender** : création d'avatars 3D photoréalistes pour l'installation finale<br>**OpenCV / MediaPipe** : détection de la présence des visiteurs |

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

### 🔴 Phase 2 : Émotions v1 (Oct 10-19)
**Objectif** : Analyser émotions + générer paramètres avatar

❌ **Problèmes** :
1. **Modèle anglais sur texte français** : prédominance erronée des émotions `disgust` et `anger`
2. **Scores du lexique insuffisants** : paramètres de l'avatar figés à 0.0 / 0.5
3. **Erreur de normalisation** : `voice_speed = 4.2` (au lieu du maximum recommandé de 1.5)

📊 **Stats v1 (bugguées)** :
- 64% positif, 18% neutre, 17% négatif ← faux négatifs massifs
- Couverture lexique : ~52% (faible)
- Paramètres avatar : variance = 0 (tous identiques)

---

### 🟢 Phase 3 : Émotions v2 (Oct 19 - Nov 1)
**Objectif** : Pipeline français fiable, paramètres qui varient

✅ **Corrections** :
1. **Remplacement du modèle anglais** : transition vers le lexique v2 et validation par XLM-RoBERTa
2. **Lexique v2 : 3× plus de patterns**
   - Racines (accueil → accueillir, accueilli, accueillant…)
   - Phrases multi-mots ("venir en aide", "ouvrir les portes")
   - ~25 racines + ~20 phrases par dimension
3. **Bug normalisation fixé**
   - v1 : ajouts cumulatifs des valeurs par défaut entraînant une dérive des résultats
   - v2 : initialisation à zéro avec intégration des valeurs par défaut uniquement si aucune émotion n'est détectée
   - Clamping strict des plages

📊 **Stats v2 (corrigées)** :
- Couverture : **71.1%** (vs 52% en v1)
- Paramètres avatar : **variance > 0** pour tous les params
- Exemple : `voice_speed` ∈ [0.75, 1.20] (plage valide [0.5, 1.5])

📦 **Livrables** :
- `src/analysis/emotion_v2.py` : module réutilisable
- `notebooks/02_emotion.ipynb` : pipeline complet d'analyse
- `data/processed/corpus_with_emotions.parquet`

---

### 🟢 Phase 4 : TTS v1-v3 (Nov 1 - Nov 12)
**Objectif** : Voix françaises expressives, mapping émotions → prosodie

| Version TTS | Caractéristiques et avancées | Point d'attention / Bilan |
|-------------|------------------------------|---------------------------|
| **TTS v1** | Edge TTS, 5 voix, prosodie large (pitch ±50Hz) | ❌ Tonalités vocales trop enfantines |
| **TTS v2** | Préparation du texte (élisions, orthographe) et détection du genre<br>Détection du genre (par exemple, « mon mari » oriente vers une voix féminine) | ❌ Troncatures audio dues au découpage par phrases |
| **TTS v3** | Texte traité en un seul appel, prosodie subtile (pitch ±10Hz, vitesse ±15%), 4 voix adultes<br>Correction orthographique des élisions (transformation de `l'imigration` en `l'immigration`) | ✅ Solution finale validée et répartition équilibrée des voix |

📦 **Livrables** :
- `src/tts/engine.py` : moteur de synthèse vocale
- `src/tts/text_prep.py` : nettoyage et corrections textuelles
- `data/audio/demo/` : ensemble de 18 fichiers MP3 et lecteur HTML interactif
- `scripts/build_player.py`

---

### 🟢 Phase 5 : Avatar 3D Three.js (Nov 12-23)
**Objectif** : Mur de masques sculpturaux 3D photoréalistes

**v1** (Nov 22) :
- 8 masques 3D, halos colorés, fond noir immersif
- ❌ **Ajustement requis** : les éléments de la bouche et des sourcils manquaient de visibilité en raison du positionnement sur l'axe Z

**v2** (Nov 23) :

✅ **Corrections géométrie** :
- Aplatissement du visage (z-scale 0.55 contre 0.85) pour faire ressortir les traits
- Sourcils épais (0.05 vs 0.035), positionnés à z=0.58
- Bouche tube élargi (0.025 vs 0.02), z=0.58
- Yeux cavités creuses + pupilles lumineuses (z=0.62)
- Fix animation sourcils (baseY stocké, pas de drift)

✨ **Features v2** :
- **Interaction au clic** : le visage s'anime, prononce le texte et le halo lumineux oscille
- Idle breathing, float léger, rotation subtile
- Parallax camera (souris)
- Hover glow
- Rim lights (contour lumineux)

**v3** (Nov 23) :

✅ **Géométrie humaine** :
- Sculpture procédurale du crâne : menton effilé, pommettes, arcade sourcilière, arête nasale
- Yeux réalistes 3 couches : sclère (blanc), iris (couleur émotion), pupille (noire + glow)
- Paupière supérieure avec ombre portée
- Sourcils courbés (ExtrudeGeometry + bevel)
- Nez anatomique (bridge + narines)
- Lèvres supérieure et inférieure distinctes (au lieu d'un tube unique)
- Clignement des yeux (~4s par cycle, déphasé par visage)

✨ **Features v3** :
- **Yeux suiveurs** : toutes les pupilles/iris suivent le curseur en temps réel (conversion mouse → world coords via unproject)
- **Comportement idle réactif** : quand un visage parle, les autres tournent la tête et les yeux vers le speaker, avec halos atténués
- **Transitions douces** : toutes les animations utilisent lerp (pas de sauts brusques)
- Éclairage enrichi : key light + fill light directionnels

**v4** (Nov 23) :

✅ **Migration vers modèle GLB réaliste** :
- Remplacement de TOUTE la géométrie procédurale par le modèle **FaceCap** (Three.js, 325 KB)
- **52 morph targets ARKit** : expressions faciales complètes (sourcils, bouche, yeux, joues, nez)
- Three.js **r128** avec `<script>` tags classiques (compatible file://)
- GLTFLoader + `parse()` sur modèle base64-encodé (aucun serveur nécessaire)
- 8 clones du modèle, différenciés par couleur émissive + expression de repos

✨ **Lip sync audio** :
- **Web Audio API** : `AnalyserNode` capte l'amplitude vocale en temps réel
- Mapping amplitude → `jawOpen` + `mouthOpen` + `mouthFunnel` + micro-expressions
- Sourcils, joues et nez réagissent aussi pendant la parole
- `createMediaElementSource()` connecte les `<audio>` base64 existants

✨ **Eye gaze via morph targets** :
- 8 morph targets directionnels (`eyeLookIn/Out/Up/Down_L/R`)
- Yeux suivent la souris (idle) ou le speaker (quand un visage parle)
- Rotation des globes oculaires (objets `eyeLeft`/`eyeRight`) en complément

✨ **Expression émotionnelle par visage** :
- Mapping `face_eyebrows` → `browOuterUp` / `browDown` + `browInnerUp`
- Mapping `face_mouth` → `mouthSmile` / `mouthFrown`
- Mapping `face_eyes` → `eyeSquint` / `eyeWide`
- Micro-expressions idle (sourire subtil oscillant)

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
  'voice_pitch': +0.3,   # Voix plus aiguë
  'voice_speed': +0.2,   # Parle plus vite
  'voice_energy': +0.4,  # Volume élevé
  'face_eyebrows': +0.2, # Sourcils levés
  'face_eyes': +0.5,     # Yeux écarquillés
  'face_gaze': +0.3      # Regard direct
}
```

---

## 🗓️ Roadmap

### ✅ Fait (Nov 23)
- [x] Corpus nettoyé (8 707 messages)
- [x] Pipeline émotions français fiable (v2)
- [x] TTS 4 voix françaises + prosodie subtile (v3)
- [x] Avatar 2D SVG animé (MVP)
- [x] Avatar 3D Three.js (modèle GLB réaliste, lip sync, 52 morph targets ARKit)
- [x] 18 démos audio + 2 players HTML
- [x] Audit sécurité (XSS fixé, code mort supprimé)
- [x] Système de contexte Claude (`.claude/` — instructions, context projet, skill update-history)

### 🔄 En cours
- [ ] **Notebook 03_tts.ipynb** : génération audio par lots (8 707 messages, environ 3h)
- [ ] **Mur 3D étendu** : passage de 8 à N visages via une grille dynamique

### 🎯 Prochaines étapes (court terme)
- [ ] Tests unitaires (pytest) pour `emotion_v2`, `text_prep`, `engine`
- [ ] Lip sync avancé : intégration `wawa-lipsync` (15 visèmes Oculus au lieu de l'amplitude seule)
- [ ] Modèles GLB variés (8 visages distincts via MakeHuman/MPFB ou Sketchfab)
- [ ] Optimisation Three.js (LOD, instancing pour 100+ visages)
- [ ] Tracking visiteur via caméra (remplacement souris → MediaPipe/OpenCV)

### 🚀 Vision long terme
- [ ] **Interaction visiteur** : détection de présence (OpenCV/MediaPipe)
  - Approche du visiteur : réveil progressif des visages
  - Geste de la main : sélection d'un visage spécifique
- [ ] **Bark TTS** (GPU) : voix ultra-expressives pour l'installation finale
- [ ] **Unity / Blender** : avatars 3D photoréalistes sous réserve de budget GPU
- [ ] **Installation physique** : écran de 4 m × 1,15 m et système audio spatialisé
- [ ] **Mode exposition** : lecture automatique en boucle et rotation des messages
- [ ] **Analytics** : suivi des contenus les plus consultés et durée moyenne d'écoute

---

## 🔬 Évolutions possibles

### Qualité audio
- **Bark (Suno AI)** : synthèse vocale de pointe aux émotions accentuées
  - Prérequis : GPU 8GB+ VRAM
  - Temps : ~8-10h pour 8 707 messages (vs 3h Edge TTS)
  - Qualité : voix presque humaines, intonations naturelles

### Visuel 3D
- **Unity HDRP** : rendu photoréaliste en temps réel
  - Peau translucide, subsurface scattering
  - Morphing facial procédural (blend shapes)
- **Blender + Cycles** : pré-rendu vidéo à haute définition
  - 1 vidéo par message (lourd : ~10GB pour 8 707 vidéos)

### Interaction avancée
- **Kinect / RealSense** : suivi de la posture et des mouvements du visiteur
  - Visage "suit" du regard
  - Adaptation selon la distance : l'intensité vocale augmente à l'approche du visiteur
- **Reconnaissance vocale** : possibilité pour le visiteur de poser des questions directes
  - RAG (Retrieval-Augmented Generation) sur le corpus
  - Représentation personnalisée : réponse du modèle de langage en incarnant le témoignage choisi

### Multi-sensorialité
- **Haptique** : vibrations au sol associées aux messages à forte charge émotionnelle
- **Ambiance lumineuse** : variation des teintes de la pièce selon l'émotion dominante
- **Expérience olfactive** : diffusion d'ambiances subtiles (phase de test)

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

**Corpus source** : Plateforme « Comme à la maison » (Singa), regroupant 20 000 témoignages anonymes de familles proposant l'accueil de réfugiés

---

## 🔗 Liens utiles

- **Dépôt GitHub** : `MaxenceGuinziemba/A_FACE_TO_A_MESSAGE`
- **Branch principale** : `data-management` (code + données)
- **Démos** :
  - `data/audio/demo/player.html` : lecteur audio à 18 cartes
  - `data/audio/demo/wall.html` : mur 2D SVG animé
  - `data/audio/demo/wall_3d.html` : mur 3D Three.js
- **Docs** :
  - `README.md` : vue d'ensemble du projet
  - `SUIVI.md` : journal d'avancement au quotidien
  - `docs/PROJECT.md` : contexte global du projet

---

*Document mis à jour le 23 novembre 2026 (v4 GLB + lip sync) — Synthèse de suivi du projet A Face to a Message*
