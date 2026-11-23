# A FACE TO A MESSAGE — Instructions Claude

## 🎯 Projet
Transformer 20 000 témoignages de solidarité en avatars émotionnels 3D interactifs.  
Installation : Mur 4m × 1.15m au Musée de l'immigration.

**Pipeline** : TEXTE → ÉMOTIONS → VOIX → VISAGE ANIMÉ → INTERACTION VISITEUR

---

## 📖 Context à lire en début de session

**OBLIGATOIRE** : Lire `.claude/PROJECT_CONTEXT.md` pour :
- Structure du repo
- État actuel du projet
- Stack technique
- Bugs connus à éviter

---

## ⚠️ RÈGLE ABSOLUE : Mise à jour historique

**AVANT CHAQUE COMMIT/PUSH** :

1. **Invoquer** `/update-history` (ou le faire manuellement)
2. **Mettre à jour** `PROJET_HISTORIQUE.md` avec :
   - Nouvelle phase si grosse feature
   - Livrables ajoutés
   - Roadmap actualisée (fait ✅ / en cours 🔄)
   - Métriques du projet
   - Date de mise à jour
3. **Synchroniser** `PROJET_HISTORIQUE_GDOCS.md` si nécessaire
4. **Commit** avec message descriptif + attribution

---

## 🔧 Conventions

### Commits
```
Type: Description courte

Détails optionnels

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

Types : `Add`, `Fix`, `Update`, `Refactor`, `Remove`

### Branch
- `main` → docs uniquement
- `data-management` → code + données (branche active, toujours push dessus)

### Avant génération
- Nettoyer `__pycache__` : `find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null`
- Tester sur 2-3 messages avant batch complet

---

## 🚫 Bugs à éviter absolument

1. **Normalisation avatar params** : Ne PAS ajouter défauts avant division
2. **TTS pitch** : Ne PAS dépasser ±10Hz (risque voix enfantines)
3. **TTS texte** : Envoyer texte complet en un appel (pas de découpage)
4. **HTML builders** : TOUJOURS utiliser `html.escape()` (XSS)
5. **Three.js z-positions** : Features DEVANT la tête (z > z_head_front)

---

## 📂 Fichiers clés

| Fichier | Rôle | Fréquence mise à jour |
|---------|------|----------------------|
| `PROJET_HISTORIQUE.md` | Historique projet | **Avant chaque commit** |
| `PROJET_HISTORIQUE_GDOCS.md` | Version Google Docs | Si PROJET_HISTORIQUE.md modifié |
| `SUIVI.md` | Journal détaillé | Quotidien (journal brut) |
| `README.md` | Vue d'ensemble | Rarement (grandes étapes) |
| `.claude/PROJECT_CONTEXT.md` | Context de session | Après grosse feature |

---

## 🎨 Paramètres Avatar (référence rapide)

**Voice** (4) : pitch [-1,1], speed [0.5,1.5], energy [0,1], warmth [0,1]  
**Face** (4) : eyebrows [-1,1], mouth [-1,1], eyes [0,1], gaze [0,1]

**8 dimensions émotionnelles** :  
Solidarité, Empathie, Chaleur, Espoir, Urgence, Détermination, Indignation, Tristesse

---

## 🔄 Workflow typique

### Nouvelle feature
1. Lire `.claude/PROJECT_CONTEXT.md`
2. Coder + tester
3. Nettoyer `__pycache__`
4. **`/update-history`** ou mise à jour manuelle
5. `git add <fichiers>`
6. `git commit -m "..."`
7. `git push origin data-management`

### Debug/fix
1. Identifier le bug
2. Fixer + vérifier que ça marche
3. **Mettre à jour PROJET_HISTORIQUE.md** (section "Corrections" ou "Problèmes résolus")
4. Commit/push

### Ajout de démo
1. Générer les fichiers
2. Tester dans navigateur
3. **Mettre à jour** :
   - `PROJET_HISTORIQUE.md` → Livrables de la phase courante
   - Métriques (nb démos, taille fichiers)
4. Commit/push

---

## 📊 État actuel (référence rapide)

**Fait** :
- Corpus 8 707 messages
- Émotions v2 (71.1% couverture)
- TTS v3 (4 voix adultes)
- Avatar 2D SVG + 3D Three.js
- 18 démos audio

**En cours** :
- Notebook 03_tts.ipynb (batch complet)
- Mur 3D étendu (N visages)

**Next** :
- Tests unitaires
- Sync labiale précise
- Optimisation Three.js

---

*Instructions créées le 23 novembre 2026*  
*À suivre pour chaque session de travail sur A FACE TO A MESSAGE*
