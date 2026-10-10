# Démarrer Jupyter avec le .venv

## ✅ Installation terminée !

Tous les packages sont installés et le kernel Jupyter est configuré.

## 🚀 Lancer Jupyter

```bash
source activate.sh
jupyter notebook
```

Ou directement :

```bash
source .venv/bin/activate
jupyter notebook
```

## 📒 Utiliser le bon kernel dans les notebooks

### Ouvrir un notebook existant

1. Clique sur un notebook (ex: `01_data_exploration.ipynb`)
2. En haut à droite, vérifie le kernel affiché
3. Si ce n'est pas **"Python (A Face to a Message)"** :
   - Menu : **Kernel → Change kernel**
   - Sélectionne : **Python (A Face to a Message)**

### Créer un nouveau notebook

1. Dans Jupyter, clique sur **New**
2. Sélectionne : **Python (A Face to a Message)**
3. ✅ Le nouveau notebook utilise le .venv !

## 🔍 Vérifier dans le notebook

Première cellule à exécuter :

```python
import sys
print(f"Python: {sys.executable}")
print(f"✅ Utilise le .venv" if '.venv' in sys.executable else "❌ N'utilise PAS le .venv")

# Test des packages
import pandas as pd
import numpy as np
import transformers
import spacy
print(f"\n✅ Packages disponibles:")
print(f"  • pandas {pd.__version__}")
print(f"  • numpy {np.__version__}")
print(f"  • transformers {transformers.__version__}")
print(f"  • spacy {spacy.__version__}")
```

Tu devrais voir :
```
Python: /home/user/LOCAL_TEST/A_FACE_TO_A_MESSAGE/.venv/bin/python
✅ Utilise le .venv

✅ Packages disponibles:
  • pandas 3.0.6
  • numpy 2.4.6
  • transformers 5.19.0
  • spacy 3.8.16
```

## 📋 Notebooks prêts à utiliser

### 1. Exploration des données
```bash
notebooks/01_data_exploration.ipynb
```
Exploration initiale du corpus de messages

### 2. Nettoyage des données  
```bash
notebooks/02_data_cleaning.ipynb
```
**À EXÉCUTER EN PREMIER** - Nettoie et unifie les 3 feuilles Excel

**Important** : Ce notebook va créer :
- `data/processed/messages_unified.csv` - Dataset complet
- `data/processed/sample_messages_100.csv` - Échantillon
- `data/processed/dataset_statistics.json` - Statistiques

### 3. Visualiseur de messages
```bash
notebooks/03_random_message_viewer.ipynb
```
Exploration interactive avec filtres (région, durée, qualité, etc.)

## 🎯 Workflow recommandé

1. **Lancer Jupyter** :
   ```bash
   source activate.sh
   jupyter notebook
   ```

2. **Exécuter le nettoyage** :
   - Ouvrir `02_data_cleaning.ipynb`
   - Sélectionner le kernel **Python (A Face to a Message)**
   - Exécuter toutes les cellules : **Cell → Run All**
   - Attendre la fin (~1-2 minutes)

3. **Explorer les messages** :
   - Ouvrir `03_random_message_viewer.ipynb`
   - Exécuter les cellules pour voir des messages aléatoires
   - Utiliser les filtres interactifs

4. **Analyser les émotions** (prochaine étape) :
   - Notebook `04_emotion_analysis.ipynb` à créer
   - Testera les modèles NLP français

## 💡 Conseils

- **Kernel** : Toujours vérifier que "Python (A Face to a Message)" est sélectionné
- **Ordre** : Exécuter `02_data_cleaning.ipynb` avant `03_random_message_viewer.ipynb`
- **Erreurs** : Si un package manque, vérifie que tu utilises le bon kernel
- **Performance** : Les premières exécutions peuvent prendre plus de temps (chargement des modèles)

## 🐛 Problèmes courants

### "ModuleNotFoundError: No module named 'pandas'"
→ Mauvais kernel sélectionné. Change pour "Python (A Face to a Message)"

### Le kernel affiche "Python 3" au lieu de "Python (A Face to a Message)"
→ Menu : Kernel → Change kernel → Python (A Face to a Message)

### Jupyter ne démarre pas
→ Vérifie que le .venv est activé :
```bash
source .venv/bin/activate
which python  # Doit afficher : .../A_FACE_TO_A_MESSAGE/.venv/bin/python
jupyter notebook
```

## ✨ C'est parti !

```bash
source activate.sh
jupyter notebook
```

Puis ouvre `02_data_cleaning.ipynb` et lance l'analyse ! 🚀
