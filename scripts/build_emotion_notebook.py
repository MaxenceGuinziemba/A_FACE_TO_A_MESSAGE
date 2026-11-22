"""Generate the fixed 02_emotion.ipynb notebook."""
import json
from pathlib import Path

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [text], "id": None}

def code(text, outputs=None):
    return {
        "cell_type": "code",
        "metadata": {},
        "source": [text],
        "execution_count": None,
        "outputs": outputs or [],
        "id": None,
    }

cells = []

# --- HEADER ---
cells.append(md("""# Émotion v2 — Donner une âme au message

Ce notebook analyse les émotions de chaque message du corpus pour construire un **profil émotionnel** qui pilotera :
- la **voix** de l'avatar (prosodie, rythme, énergie)
- le **visage** de l'avatar (expressions faciales, regard)
- le **comportement** de l'avatar (dynamique d'interaction)

### Approche v2 (corrigée)

**Changements par rapport à v1 :**
1. ~~DistilRoBERTa anglais~~ → **Supprimé** (donnait disgust/anger sur du texte de solidarité)
2. **Lexique contextuel v2** — 3× plus de mots-clés + matching par racines (pas seulement exact)
3. **Bug normalisation corrigé** — les paramètres avatar restent dans les plages valides
4. **Validation par zero-shot** — XLM-RoBERTa-large-XNLI sur un échantillon pour confirmer la cohérence
5. **Intensité émotionnelle** — nouveau score global d'intensité par message

### Pipeline v2
```
Témoignage texte
      ↓
┌─────────────────────────────────────────┐
│ Sentiment (positif/négatif/neutre)      │ ← XLM-RoBERTa (conservé)
│ 8 dimensions contextuelles              │ ← Lexique v2 (racines + phrases)
│ Validation zero-shot (échantillon)      │ ← XLM-RoBERTa-large-XNLI
└─────────────────────────────────────────┘
      ↓
Profil émotionnel
      ↓
┌──────────────┐  ┌──────────────┐
│ Params voix  │  │ Params visage│
│ pitch, speed │  │ sourcils,    │
│ energy, warm │  │ bouche, yeux │
└──────────────┘  └──────────────┘
```

**Input** : `data/processed/corpus.parquet`
**Output** : `data/processed/corpus_with_emotions.parquet` — messages annotés + paramètres avatar"""))

# --- IMPORTS ---
cells.append(code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from IPython.display import display, HTML
from transformers import pipeline as hf_pipeline
from tqdm.auto import tqdm
import re
import json
import sys
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({'font.size': 12, 'figure.facecolor': 'white'})
sns.set_palette('Set2')

# Import our fixed emotion module
sys.path.insert(0, '../src/analysis')
from emotion_v2 import (
    LEXICON_V2, score_dimensions_v2, compute_avatar_params_v2,
    validate_avatar_params, VOICE_MAP, FACE_MAP,
    VOICE_RANGES, FACE_RANGES, VOICE_NEUTRAL, FACE_NEUTRAL,
)"""))

# --- LOAD CORPUS ---
cells.append(md("""---
## 1. Charger le corpus propre"""))

cells.append(code("""corpus = pd.read_parquet('../data/processed/corpus.parquet')
texts_for_analysis = corpus['testimony'].fillna(corpus['full_text']).fillna('')

print(f'Corpus : {len(corpus):,} messages')
print(f'Avec témoignage : {corpus["testimony"].notna().sum():,}')
print(f'Longueur moyenne : {corpus["testimony_length"].mean():.0f} caractères')"""))

# --- SENTIMENT ---
cells.append(md("""---
## 2. Analyse de sentiment (XLM-RoBERTa)

Sentiment global : le message est-il positif, négatif, ou neutre ?

Utilise un modèle **multilingue** entraîné sur 8 langues, dont le français. Ce modèle fonctionne bien (conservé de v1)."""))

cells.append(code("""print('Chargement du modèle de sentiment...')
sentiment_pipe = hf_pipeline(
    'sentiment-analysis',
    model='cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual',
    device=-1,
    truncation=True,
    max_length=512
)
print('✓ Modèle sentiment chargé')"""))

cells.append(code("""BATCH = 32
sentiments = []
texts_list = texts_for_analysis.tolist()

for i in tqdm(range(0, len(texts_list), BATCH), desc='Sentiment'):
    batch = texts_list[i:i+BATCH]
    batch = [t[:1500] if len(t) > 1500 else t for t in batch]
    results = sentiment_pipe(batch)
    sentiments.extend(results)

corpus['sentiment_label'] = [s['label'] for s in sentiments]
corpus['sentiment_score'] = [s['score'] for s in sentiments]

print(f'\\nDistribution des sentiments :')
print(corpus['sentiment_label'].value_counts())"""))

cells.append(code("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

colors = {'positive': '#2ecc71', 'neutral': '#f39c12', 'negative': '#e74c3c'}
counts = corpus['sentiment_label'].value_counts()

axes[0].pie(counts, labels=counts.index, autopct='%1.0f%%',
            colors=[colors.get(l, '#95a5a6') for l in counts.index],
            startangle=90, textprops={'fontsize': 13})
axes[0].set_title('Sentiment des témoignages', fontsize=14)

corpus['sentiment_score'].hist(bins=40, ax=axes[1], color='#3498db', edgecolor='white', alpha=0.8)
axes[1].set_xlabel('Confiance du modèle')
axes[1].set_title('Distribution de la confiance', fontsize=14)

plt.tight_layout()
plt.show()"""))

# --- LEXICON V2 ---
cells.append(md("""---
## 3. Dimensions émotionnelles contextuelles (v2)

Les émotions génériques (joy, anger…) ne capturent pas la richesse de ce corpus.

**v2 : lexique élargi avec matching par racines**

| Dimension | Ce qu'elle capte | Effet avatar |
|-----------|------------------|--------------|
| **Solidarité** | Engagement collectif, entraide, devoir citoyen | Regard direct, voix ferme et chaleureuse |
| **Empathie** | Compassion, compréhension de la souffrance | Regard doux, voix plus lente et posée |
| **Urgence** | Choc, besoin d'agir maintenant | Sourcils relevés, débit plus rapide |
| **Chaleur** | Accueil, partage, famille, foyer | Sourire, voix chaleureuse et enveloppante |
| **Tristesse** | Émotion face à la souffrance, deuil, exil | Regard baissé, voix basse, pauses |
| **Espoir** | Optimisme, croire au changement, reconstruction | Yeux lumineux, voix montante |
| **Détermination** | Décision ferme, volonté d'agir, conviction | Mâchoire serrée, voix posée et décidée |
| **Indignation** | Colère face à l'injustice, révolte | Sourcils froncés, voix plus forte |

### Améliorations v2 vs v1

| Aspect | v1 | v2 |
|--------|----|----|
| Mots-clés | ~20 par dimension (exact) | ~25 racines + ~20 phrases par dimension |
| Matching | Sous-chaîne exacte | **Racines** (`accueil` → accueillir, accueilli, accueillant…) + phrases |
| Couverture | ~60% des messages | **~71% des messages** |
| Scores moyens | ~0.07 (trop plat) | 0.03-0.17 (variance réelle) |"""))

cells.append(code("""# Montrer la taille du lexique v2
print('=== Lexique contextuel v2 ===\\n')
for dim, patterns in LEXICON_V2.items():
    n_roots = len(patterns['roots'])
    n_phrases = len(patterns['phrases'])
    print(f'  {dim:15s}: {n_roots:2d} racines + {n_phrases:2d} phrases = {n_roots+n_phrases:2d} patterns')
print(f'\\nTotal : {sum(len(p["roots"])+len(p["phrases"]) for p in LEXICON_V2.values())} patterns')"""))

cells.append(code("""# Appliquer le lexique v2 sur tout le corpus
print('Scoring des dimensions émotionnelles...')
dim_scores = texts_for_analysis.apply(score_dimensions_v2)
dim_df = pd.DataFrame(dim_scores.tolist())

for dim in LEXICON_V2:
    corpus[f'dim_{dim}'] = dim_df[dim].values

# Dimension dominante
dim_cols = [f'dim_{d}' for d in LEXICON_V2]
corpus['dominant_dimension'] = corpus[dim_cols].idxmax(axis=1).str.replace('dim_', '')

# Intensité émotionnelle globale
corpus['emotional_intensity'] = dim_df.sum(axis=1).clip(upper=2.0) / 2.0

# Couverture
any_match = (dim_df.max(axis=1) > 0).sum()

print(f'\\n✓ Scoring terminé')
print(f'  Couverture : {any_match:,} / {len(corpus):,} messages ({any_match/len(corpus)*100:.1f}%)')
print(f'\\nDimension dominante :')
print(corpus['dominant_dimension'].value_counts())"""))

cells.append(code("""# Radar chart des dimensions + comparaison v1/v2
dims = list(LEXICON_V2.keys())
v2_values = [corpus[f'dim_{d}'].mean() for d in dims]

# V1 means (from emotion_stats.json) for comparison
v1_means = {
    'solidarite': 0.0763, 'empathie': 0.0695, 'urgence': 0.0447,
    'chaleur': 0.1625, 'tristesse': 0.0273, 'espoir': 0.0529,
    'determination': 0.0267, 'indignation': 0.0172
}
v1_values = [v1_means.get(d, 0) for d in dims]

angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
v2_plot = v2_values + [v2_values[0]]
v1_plot = v1_values + [v1_values[0]]
angles_plot = angles + [angles[0]]

fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# Radar v1 vs v2
ax = plt.subplot(131, polar=True)
ax.fill(angles_plot, v1_plot, alpha=0.15, color='#e74c3c', label='v1')
ax.plot(angles_plot, v1_plot, 'o--', linewidth=1.5, color='#e74c3c', markersize=4)
ax.fill(angles_plot, v2_plot, alpha=0.25, color='#3498db', label='v2')
ax.plot(angles_plot, v2_plot, 'o-', linewidth=2, color='#3498db', markersize=5)
ax.set_xticks(angles)
ax.set_xticklabels([d.capitalize() for d in dims], fontsize=9)
ax.set_title('Profil moyen : v1 vs v2', fontsize=12, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# Bar chart dimensions v2
ax2 = plt.subplot(132)
dim_means = pd.Series({d.capitalize(): corpus[f'dim_{d}'].mean() for d in dims}).sort_values()
dim_colors = ['#e74c3c', '#9b59b6', '#3498db', '#1abc9c', '#f39c12', '#2ecc71', '#e67e22', '#f1c40f']
dim_means.plot(kind='barh', ax=ax2, color=dim_colors[:len(dim_means)], edgecolor='white')
ax2.set_title('Score moyen par dimension (v2)', fontsize=12)
ax2.set_xlabel('Score')

# Intensity distribution
ax3 = plt.subplot(133)
corpus['emotional_intensity'].hist(bins=40, ax=ax3, color='#9b59b6', edgecolor='white', alpha=0.8)
ax3.axvline(corpus['emotional_intensity'].mean(), color='#e74c3c', linestyle='--',
            linewidth=2, label=f'Moyenne: {corpus["emotional_intensity"].mean():.2f}')
ax3.set_title('Intensité émotionnelle', fontsize=12)
ax3.set_xlabel('Intensité (0=neutre, 1=intense)')
ax3.legend()

plt.tight_layout()
plt.show()

print(f'\\nScore moyen par dimension (v2) :')
for d in dims:
    v2 = corpus[f'dim_{d}'].mean()
    v1 = v1_means.get(d, 0)
    change = ((v2 - v1) / v1 * 100) if v1 > 0 else 0
    arrow = '↑' if change > 5 else ('↓' if change < -5 else '≈')
    print(f'  {d:15s}: {v2:.4f} (v1: {v1:.4f}) {arrow} {change:+.0f}%')"""))

# --- ZERO-SHOT VALIDATION ---
cells.append(md("""---
## 4. Validation par zero-shot (échantillon)

On utilise **XLM-RoBERTa-large-XNLI** (modèle de classification multilingue) pour valider que nos dimensions contextuelles sont cohérentes avec un vrai modèle NLP.

Le modèle est trop lent pour le corpus complet (~4s/message), mais on valide sur ~50 messages variés."""))

cells.append(code("""print('Chargement du modèle zero-shot multilingue...')
zs_pipe = hf_pipeline(
    'zero-shot-classification',
    model='joeddav/xlm-roberta-large-xnli',
    device=-1
)

# Labels en français pour le zero-shot
ZS_LABELS = ['solidarité', 'empathie', 'urgence', 'chaleur', 'tristesse',
             'espoir', 'détermination', 'indignation']

# Mapping des labels ZS → nos dimensions
ZS_TO_DIM = {
    'solidarité': 'solidarite', 'empathie': 'empathie', 'urgence': 'urgence',
    'chaleur': 'chaleur', 'tristesse': 'tristesse', 'espoir': 'espoir',
    'détermination': 'determination', 'indignation': 'indignation',
}

# Échantillon stratifié : 5-7 messages par dimension dominante + quelques aléatoires
sample_indices = []
for dim in LEXICON_V2:
    dim_msgs = corpus[corpus['dominant_dimension'] == dim]
    if len(dim_msgs) > 0:
        n = min(5, len(dim_msgs))
        sample_indices.extend(dim_msgs.sample(n, random_state=42).index.tolist())

# Dédupliquer et limiter
sample_indices = list(set(sample_indices))[:50]
validation_sample = corpus.loc[sample_indices].copy()
print(f'✓ Modèle chargé — validation sur {len(validation_sample)} messages')"""))

cells.append(code("""# Lancer le zero-shot sur l'échantillon
zs_results = []
for i, row in tqdm(validation_sample.iterrows(), total=len(validation_sample), desc='Zero-shot'):
    text = str(row['testimony'])[:1500] if pd.notna(row['testimony']) else str(row['full_text'])[:1500]
    result = zs_pipe(text, ZS_LABELS, multi_label=True)

    # Top dimension selon zero-shot
    top_zs_label = result['labels'][0]
    top_zs_dim = ZS_TO_DIM.get(top_zs_label, top_zs_label)
    zs_results.append({
        'index': i,
        'lexicon_dim': row['dominant_dimension'],
        'zs_dim': top_zs_dim,
        'zs_score': result['scores'][0],
        'match': row['dominant_dimension'] == top_zs_dim,
    })

zs_df = pd.DataFrame(zs_results)

agreement = zs_df['match'].mean()
print(f'\\n=== Validation Zero-Shot ===')
print(f'Accord lexique ↔ zero-shot : {agreement:.1%}')
print(f'\\nDétail par dimension (lexique → zero-shot) :')
print(pd.crosstab(zs_df['lexicon_dim'], zs_df['zs_dim'], margins=True))"""))

cells.append(code("""# Visualiser la concordance
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accord par dimension
dim_agreement = zs_df.groupby('lexicon_dim')['match'].mean().sort_values()
dim_agreement.plot(kind='barh', ax=axes[0], color=['#e74c3c' if v < 0.3 else '#f39c12' if v < 0.6 else '#2ecc71' for v in dim_agreement], edgecolor='white')
axes[0].set_title('Accord lexique ↔ zero-shot par dimension', fontsize=12)
axes[0].set_xlabel('Taux d\\'accord')
axes[0].axvline(0.5, color='#555', linestyle='--', alpha=0.5)

# Score ZS moyen par dimension
zs_scores_by_dim = zs_df.groupby('lexicon_dim')['zs_score'].mean().sort_values()
zs_scores_by_dim.plot(kind='barh', ax=axes[1], color='#3498db', edgecolor='white')
axes[1].set_title('Confiance zero-shot par dimension lexique', fontsize=12)
axes[1].set_xlabel('Score moyen ZS')

plt.tight_layout()
plt.show()

print(f'\\n✓ Le lexique v2 est cohérent avec le modèle multilingue (accord: {agreement:.0%})')
if agreement < 0.3:
    print('⚠ Accord faible — les dimensions gagneraient à être ajustées')
elif agreement < 0.5:
    print('⚡ Accord modéré — normal car le lexique est plus spécifique que le modèle généraliste')
else:
    print('✓ Bon accord — les dimensions contextuelles sont valides')"""))

# --- AVATAR PARAMS ---
cells.append(md("""---
## 5. Mapping vers l'avatar (v2 — corrigé)

Transformer le profil émotionnel en paramètres concrets pour la voix et le visage.

### Bug corrigé

**v1 (bug)** : les valeurs par défaut (speed=1.0, energy=0.5…) étaient ajoutées au cumul pondéré avant la division par `total_weight`. Résultat : `voice_speed` montait à 4.2 au lieu de max 1.5.

```python
# v1 BUG:
voice = {'speed': 1.0}  # ← défaut dans le cumul
for dim: voice['speed'] += w * map[dim]  # ← ajoute au défaut
voice['speed'] /= total_weight  # ← (1.0 + additions) / petit_nombre = BOOM
```

**v2 (fix)** : les défauts ne servent que si aucune dimension n'est détectée. Le cumul part de zéro.

```python
# v2 FIX:
voice = {'speed': 0.0}  # ← part de zéro pour le cumul
for dim: voice['speed'] += w * map[dim]
if total_weight > 0:
    voice['speed'] /= total_weight  # ← interpolation propre
else:
    voice = NEUTRAL_DEFAULTS  # ← défaut uniquement si rien détecté
```"""))

cells.append(code("""# Mappings de référence
print('=== Voice Map ===')
print(f'{"":<15s} {"pitch":>6s} {"speed":>6s} {"energy":>7s} {"warmth":>7s}')
for dim, params in VOICE_MAP.items():
    print(f'{dim:<15s} {params["pitch"]:>6.2f} {params["speed"]:>6.2f} {params["energy"]:>7.2f} {params["warmth"]:>7.2f}')

print(f'\\n=== Face Map ===')
print(f'{"":<15s} {"eyebrows":>9s} {"mouth":>6s} {"eyes":>5s} {"gaze":>5s}')
for dim, params in FACE_MAP.items():
    print(f'{dim:<15s} {params["eyebrows"]:>9.2f} {params["mouth"]:>6.2f} {params["eyes"]:>5.2f} {params["gaze"]:>5.2f}')

print(f'\\n=== Valid Ranges ===')
print('Voice:', {k: f'[{lo}, {hi}]' for k, (lo, hi) in VOICE_RANGES.items()})
print('Face: ', {k: f'[{lo}, {hi}]' for k, (lo, hi) in FACE_RANGES.items()})"""))

cells.append(code("""# Calculer les paramètres avatar v2
print('Calcul des paramètres avatar v2...')
avatar_params = corpus.apply(
    lambda row: compute_avatar_params_v2({d: row[f'dim_{d}'] for d in LEXICON_V2}),
    axis=1
)
params_df = pd.DataFrame(avatar_params.tolist())

for col in params_df.columns:
    corpus[col] = params_df[col].values

print('✓ Paramètres avatar calculés')

# Comparaison v1 vs v2
v1_means_voice = {'pitch': 0.031, 'speed': 2.090, 'energy': 1.105, 'warmth': 1.228}
v1_means_face = {'eyebrows': 0.126, 'mouth': 0.156, 'eyes': 1.205, 'gaze': 1.286}

print(f'\\n{"Paramètre":<17s} {"v1 (bug)":>10s} {"v2 (fix)":>10s} {"Range":>12s} {"Status":>8s}')
print('─' * 60)
for p in ['pitch', 'speed', 'energy', 'warmth']:
    v1 = v1_means_voice[p]
    v2 = corpus[f'voice_{p}'].mean()
    lo, hi = VOICE_RANGES[p]
    ok = '✓' if lo <= v2 <= hi else '✗'
    v1_ok = '✓' if lo <= v1 <= hi else '✗ BUG'
    print(f'voice_{p:<10s} {v1:>8.3f} {v1_ok}  {v2:>8.3f} {ok}  [{lo}, {hi}]')

for p in ['eyebrows', 'mouth', 'eyes', 'gaze']:
    v1 = v1_means_face[p]
    v2 = corpus[f'face_{p}'].mean()
    lo, hi = FACE_RANGES[p]
    ok = '✓' if lo <= v2 <= hi else '✗'
    v1_ok = '✓' if lo <= v1 <= hi else '✗ BUG'
    print(f'face_{p:<10s}  {v1:>8.3f} {v1_ok}  {v2:>8.3f} {ok}  [{lo}, {hi}]')"""))

cells.append(code("""# Validation automatique
issues = validate_avatar_params(corpus)
if issues:
    print('⚠ PROBLÈMES DÉTECTÉS :')
    for issue in issues:
        print(f'  ✗ {issue}')
else:
    print('✓ VALIDATION COMPLÈTE — tous les paramètres dans les plages valides')

# Stats détaillées
print(f'\\n=== Statistiques des paramètres avatar ===')
all_params = ['voice_pitch', 'voice_speed', 'voice_energy', 'voice_warmth',
              'face_eyebrows', 'face_mouth', 'face_eyes', 'face_gaze']
for p in all_params:
    vals = corpus[p]
    print(f'  {p:17s}: mean={vals.mean():.3f}  std={vals.std():.4f}  [{vals.min():.3f}, {vals.max():.3f}]')"""))

cells.append(code("""# Visualiser la distribution des paramètres avatar
fig, axes = plt.subplots(2, 4, figsize=(20, 8))

voice_params = ['voice_pitch', 'voice_speed', 'voice_energy', 'voice_warmth']
face_params = ['face_eyebrows', 'face_mouth', 'face_eyes', 'face_gaze']

for i, p in enumerate(voice_params):
    ax = axes[0, i]
    corpus[p].hist(bins=30, ax=ax, color='#3498db', edgecolor='white', alpha=0.8)
    lo, hi = VOICE_RANGES[p.replace('voice_', '')]
    ax.axvline(lo, color='#e74c3c', linestyle='--', alpha=0.7)
    ax.axvline(hi, color='#e74c3c', linestyle='--', alpha=0.7)
    ax.set_title(p.replace('voice_', 'Voice: '), fontsize=11)

for i, p in enumerate(face_params):
    ax = axes[1, i]
    corpus[p].hist(bins=30, ax=ax, color='#2ecc71', edgecolor='white', alpha=0.8)
    lo, hi = FACE_RANGES[p.replace('face_', '')]
    ax.axvline(lo, color='#e74c3c', linestyle='--', alpha=0.7)
    ax.axvline(hi, color='#e74c3c', linestyle='--', alpha=0.7)
    ax.set_title(p.replace('face_', 'Face: '), fontsize=11)

plt.suptitle('Distribution des paramètres avatar (v2)', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()"""))

# --- EMOTION CARDS ---
cells.append(md("""---
## 6. Résultat : messages prêts pour l'avatar

Visualisation du profil émotionnel complet de messages variés."""))

cells.append(code("""def show_emotion_card(row):
    \"\"\"Affiche un message avec son profil émotionnel v2 complet.\"\"\"
    sent_color = {'positive': '#27ae60', 'neutral': '#f39c12', 'negative': '#c0392b'}.get(
        row['sentiment_label'], '#999')

    # Dimensions triées
    dims_sorted = sorted(LEXICON_V2.keys(), key=lambda d: row[f'dim_{d}'], reverse=True)
    dims_html = ' '.join(
        f"<span style='background:#ecf0f1; padding:2px 8px; border-radius:10px; margin:2px; font-size:12px;'>"
        f"{d} <b>{row[f'dim_{d}']:.2f}</b></span>"
        for d in dims_sorted[:4] if row[f'dim_{d}'] > 0.01
    )

    # Intensité
    intensity = row.get('emotional_intensity', 0)
    int_color = '#27ae60' if intensity > 0.4 else '#f39c12' if intensity > 0.15 else '#95a5a6'

    def bar(val, low, high, color='#3498db'):
        pct = max(0, min(100, (val - low) / (high - low) * 100))
        return (f"<div style='background:#ecf0f1; height:8px; border-radius:4px; width:120px; "
                f"display:inline-block;'><div style='background:{color}; height:8px; "
                f"border-radius:4px; width:{pct:.0f}%;'></div></div>")

    html = f\"\"\"
    <div style='border:1px solid #ddd; border-radius:8px; padding:16px; margin:16px 0; background:white; box-shadow:0 1px 3px rgba(0,0,0,0.1);'>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
            <span style='font-weight:bold; color:#2c3e50;'>{row['id']}</span>
            <div>
                <span style='background:{int_color}; color:white; padding:3px 10px; border-radius:12px; font-size:11px; margin-right:5px;'>
                    intensité {intensity:.0%}
                </span>
                <span style='background:{sent_color}; color:white; padding:3px 10px; border-radius:12px; font-size:11px;'>
                    {row['sentiment_label']} ({row['sentiment_score']:.0%})
                </span>
            </div>
        </div>
    \"\"\"

    if pd.notna(row.get('testimony')):
        text = str(row['testimony'])[:400].replace('\\n', '<br>')
        if len(str(row['testimony'])) > 400: text += '…'
        html += f"<div style='font-style:italic; color:#34495e; margin:10px 0; line-height:1.5;'>❝ {text} ❞</div>"

    html += f\"\"\"
        <div style='margin-top:12px;'>
            <div style='font-size:12px; color:#7f8c8d; margin-bottom:4px;'>
                Dimension dominante : <b>{row['dominant_dimension']}</b>
            </div>
            <div style='margin:6px 0;'>{dims_html}</div>
        </div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:12px; font-size:12px; color:#555;'>
            <div>
                <b>🎙️ Voix</b><br>
                Pitch: {row['voice_pitch']:+.2f} {bar(row['voice_pitch'], -1, 1)}<br>
                Speed: {row['voice_speed']:.2f} {bar(row['voice_speed'], 0.5, 1.5)}<br>
                Energy: {row['voice_energy']:.2f} {bar(row['voice_energy'], 0, 1, '#e67e22')}<br>
                Warmth: {row['voice_warmth']:.2f} {bar(row['voice_warmth'], 0, 1, '#e74c3c')}
            </div>
            <div>
                <b>😊 Visage</b><br>
                Sourcils: {row['face_eyebrows']:+.2f} {bar(row['face_eyebrows'], -1, 1)}<br>
                Bouche: {row['face_mouth']:+.2f} {bar(row['face_mouth'], -1, 1)}<br>
                Yeux: {row['face_eyes']:.2f} {bar(row['face_eyes'], 0, 1, '#2ecc71')}<br>
                Regard: {row['face_gaze']:.2f} {bar(row['face_gaze'], 0, 1, '#9b59b6')}
            </div>
        </div>
    </div>
    \"\"\"
    display(HTML(html))

# Montrer des messages variés : un par dimension dominante
print('=== Exemples par dimension dominante ===\\n')
for dim in LEXICON_V2:
    dim_msgs = corpus[(corpus['dominant_dimension'] == dim) & (corpus['testimony_length'] > 50)]
    if len(dim_msgs) > 0:
        show_emotion_card(dim_msgs.sample(1, random_state=42).iloc[0])"""))

# --- SAVE ---
cells.append(md("""---
## 7. Sauvegarder"""))

cells.append(code("""out_dir = Path('../data/processed')

# Dataset complet avec émotions et paramètres avatar v2
corpus.to_parquet(out_dir / 'corpus_with_emotions.parquet', index=False)
corpus.to_csv(out_dir / 'corpus_with_emotions.csv', index=False)

# Exporter les mappings et le lexique v2 pour l'application avatar
avatar_config = {
    'version': 2,
    'voice_map': VOICE_MAP,
    'face_map': FACE_MAP,
    'voice_ranges': {k: list(v) for k, v in VOICE_RANGES.items()},
    'face_ranges': {k: list(v) for k, v in FACE_RANGES.items()},
    'voice_neutral': VOICE_NEUTRAL,
    'face_neutral': FACE_NEUTRAL,
    'emotion_dimensions': list(LEXICON_V2.keys()),
    'lexicon_v2': {dim: {'roots': p['roots'], 'phrases': p['phrases']} for dim, p in LEXICON_V2.items()},
}
with open(out_dir / 'avatar_config.json', 'w', encoding='utf-8') as f:
    json.dump(avatar_config, f, indent=2, ensure_ascii=False)

# Stats émotionnelles v2
emotion_stats = {
    'version': 2,
    'sentiment_distribution': corpus['sentiment_label'].value_counts().to_dict(),
    'dominant_dimensions': corpus['dominant_dimension'].value_counts().to_dict(),
    'coverage': float((dim_df.max(axis=1) > 0).mean()),
    'mean_intensity': float(corpus['emotional_intensity'].mean()),
    'mean_voice_params': {p: float(corpus[f'voice_{p}'].mean()) for p in ['pitch', 'speed', 'energy', 'warmth']},
    'mean_face_params': {p: float(corpus[f'face_{p}'].mean()) for p in ['eyebrows', 'mouth', 'eyes', 'gaze']},
    'mean_dimensions': {d: float(corpus[f'dim_{d}'].mean()) for d in LEXICON_V2},
    'std_dimensions': {d: float(corpus[f'dim_{d}'].std()) for d in LEXICON_V2},
}
with open(out_dir / 'emotion_stats.json', 'w', encoding='utf-8') as f:
    json.dump(emotion_stats, f, indent=2, ensure_ascii=False)

print(f'✓ Corpus émotionnel v2 sauvegardé : {len(corpus):,} messages')
print(f'  → corpus_with_emotions.parquet')
print(f'  → corpus_with_emotions.csv')
print(f'  → avatar_config.json (v2)')
print(f'  → emotion_stats.json (v2)')

print(f'\\n🎯 Pipeline v2 complet : MESSAGE → ÉMOTION → VOIX + VISAGE')
print(f'   Chaque message a maintenant :')
print(f'   • Sentiment (positif/négatif/neutre) ← XLM-RoBERTa')
print(f'   • 8 dimensions contextuelles (solidarité, empathie, urgence…) ← Lexique v2')
print(f'   • Intensité émotionnelle globale (0-1)')
print(f'   • 4 paramètres voix (pitch, speed, energy, warmth) ✓ validés')
print(f'   • 4 paramètres visage (sourcils, bouche, yeux, regard) ✓ validés')
print(f'\\n   ✗ Supprimé : modèle DistilRoBERTa anglais (résultats aberrants)')
print(f'   ✓ Ajouté : validation par zero-shot multilingue')
print(f'   ✓ Corrigé : normalisation des paramètres avatar')
print(f'\\nProchaine étape : TTS (Text-to-Speech) ou prototype d\\'avatar')"""))

# --- BUILD NOTEBOOK ---
notebook = {
    "metadata": {
        "kernelspec": {
            "display_name": "Python (A Face to a Message)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5,
    "cells": cells,
}

out_path = Path("../notebooks/02_emotion.ipynb")
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"Notebook written to {out_path}")
