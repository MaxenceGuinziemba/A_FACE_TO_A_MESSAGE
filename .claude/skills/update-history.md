---
name: update-history
description: Met à jour PROJET_HISTORIQUE.md avant commit/push
---

# Update History Skill

**Usage** : `/update-history` ou `/update-history "description des changements"`

Ce skill met à jour automatiquement `PROJET_HISTORIQUE.md` avec les derniers changements du projet.

## Étapes

1. **Lire git status/diff** pour identifier les fichiers modifiés
2. **Lire PROJET_HISTORIQUE.md** pour connaître l'état actuel
3. **Identifier les sections à mettre à jour** :
   - Nouvelle phase si grosse feature
   - Ajout de livrables dans la phase courante
   - Mise à jour roadmap (fait ✅ / en cours 🔄)
   - Métriques du projet
   - Date de dernière mise à jour

4. **Proposer les modifications** et demander validation
5. **Appliquer les modifications** si validé
6. **Rappeler** de commit avec les bonnes conventions

## Instructions pour Claude

Quand ce skill est invoqué :

1. Lance `git status -s` pour voir les fichiers modifiés
2. Lance `git diff --stat` pour voir l'ampleur des changements
3. Lis `PROJET_HISTORIQUE.md` (en particulier la dernière phase et la roadmap)
4. Lis `.claude/PROJECT_CONTEXT.md` pour le contexte

5. Détermine si :
   - **Nouvelle phase** requise (grosse feature : nouveau module, nouvelle capacité majeure)
   - **Mise à jour phase courante** (ajout livrables, corrections)
   - **Roadmap à actualiser** (tâche passée de "en cours" à "fait")
   - **Métriques à mettre à jour** (nb commits, lignes code, nb démos)

6. Propose les modifications en montrant :
   - Section(s) à modifier
   - Ancien vs Nouveau texte
   - Justification

7. Si l'utilisateur valide, applique les modifications

8. Rappelle :
   ```
   Prochaines étapes :
   1. Vérifier PROJET_HISTORIQUE.md
   2. git add <fichiers>
   3. git commit -m "..."
   4. git push origin data-management
   ```

## Exemples de mise à jour

### Nouvelle phase (grosse feature)
```markdown
### Phase 7 : Interaction visiteur (Nov 24-25) — FAIT

**Objectif** : Détection présence et réaction des avatars

**Réalisé** :
- Intégration MediaPipe pour tracking visiteur
- Avatars "s'éveillent" quand visiteur approche
- Geste main → sélection visage

**Livrables** :
- `src/interaction/visitor_tracking.py`
- Demo interactive avec webcam
```

### Ajout de livrables (phase courante)
```markdown
📦 **Livrables** :
- `data/audio/demo/wall_3d.html` (978 KB)
- `scripts/build_wall_3d.py`
- `data/audio/full/` — 8 707 MP3 (batch complet)  ← NOUVEAU
- `notebooks/03_tts.ipynb` — génération batch        ← NOUVEAU
```

### Roadmap actualisée
```markdown
### ✅ Fait (Nov 24)
- [x] Notebook 03_tts.ipynb — génération audio batch  ← DÉPLACÉ de "EN COURS"
- [x] Tests unitaires (pytest) pour modules core      ← AJOUTÉ

### 🔄 En cours
- [ ] Mur 3D étendu — N visages dynamiques
- [ ] Synchronisation labiale précise                 ← NOUVEAU
```

### Métriques
```markdown
| Métrique | Valeur |
|----------|--------|
| **Commits GitHub** | 15+ sur `data-management` |  ← WAS: 10+
| **Lignes de code** | ~3 200 (Python + JS) |      ← WAS: ~2 500
| **Audio générés** | 8 725 (18 démos + 8 707 corpus) | ← WAS: 18 démos
```

## Points d'attention

- **Ne pas** réécrire tout le document, juste les sections nécessaires
- **Conserver** l'historique des phases précédentes intact
- **Dater** les mises à jour ("*Document mis à jour le XX novembre 2026*")
- **Être concis** : bullet points, pas de paragraphes longs
- **Vérifier** que la version GDOCS existe aussi et proposer de la mettre à jour

## Après mise à jour

Toujours rappeler à l'utilisateur :
1. Vérifier que PROJET_HISTORIQUE.md et PROJET_HISTORIQUE_GDOCS.md sont cohérents
2. Commit avec message descriptif
3. Push sur `data-management`
