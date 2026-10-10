# Setup Guide

## Prerequisites

- **Python**: 3.9 or higher
- **Git**: For version control
- **pip**: Python package manager

## Installation Steps

### 1. Clone the Repository

```bash
git clone git@github.com:MaxenceGuinziemba/A_FACE_TO_A_MESSAGE.git
cd A_FACE_TO_A_MESSAGE
```

### 2. Create a Virtual Environment

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download Language Models (for NLP)

For French language support with spaCy:

```bash
python -m spacy download fr_core_news_md
```

Or for more accurate results:

```bash
python -m spacy download fr_core_news_lg
```

### 5. Verify Installation

```bash
python -c "import pandas; import numpy; import transformers; print('All core packages installed successfully!')"
```

## Data Setup

The main dataset should be in `data/raw/`. The Excel file with refugee hosting messages is already included (if cloned from the complete repository).

**File location:**
```
data/raw/Te?le?com Paristech Re?cup ération des données.xlsx
```

## Project Structure Overview

```
A_FACE_TO_A_MESSAGE/
├── data/
│   ├── raw/              # Original data files (Excel)
│   │   └── .gitkeep
│   └── processed/        # Processed and cleaned data
│       └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── analysis/         # NLP & emotion analysis
│   │   └── __init__.py
│   ├── tts/             # Text-to-Speech
│   │   └── __init__.py
│   ├── avatar/          # Avatar animation
│   │   └── __init__.py
│   └── interaction/     # Visitor interaction
│       └── __init__.py
├── notebooks/           # Jupyter notebooks for exploration
├── models/              # Saved models
├── config/              # Configuration files
├── tests/               # Unit tests
├── docs/                # Documentation
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # Project overview
├── PROJECT_OVERVIEW.md # Detailed project documentation
├── DATA_OVERVIEW.md    # Dataset documentation
└── SETUP.md            # This file
```

## Running Jupyter Notebooks

```bash
jupyter notebook
```

Navigate to the `notebooks/` directory and create a new notebook, or open existing ones.

## Development Workflow

### 1. Activate Virtual Environment
Always activate the virtual environment before working:
```bash
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 2. Create a New Branch
For new features or experiments:
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
Work in the appropriate module:
- NLP/Emotion analysis → `src/analysis/`
- Voice synthesis → `src/tts/`
- Avatar work → `src/avatar/`
- Interaction → `src/interaction/`

### 4. Test Your Code
```bash
pytest tests/
```

### 5. Format Code
```bash
black src/
```

### 6. Commit and Push
```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

## Quick Start: Data Exploration

Create a notebook in `notebooks/` and start exploring:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data_path = '../data/raw/Te?le?com Paristech Re?cup ération des données.xlsx'
familles_1 = pd.read_excel(data_path, sheet_name='Familles 1')
familles_2 = pd.read_excel(data_path, sheet_name='Familles 2')
nouvelle_platform = pd.read_excel(data_path, sheet_name='Nouvelle Plateforme')

# Display basic info
print(f"Familles 1: {len(familles_1)} messages")
print(f"Familles 2: {len(familles_2)} messages")
print(f"Nouvelle Plateforme: {len(nouvelle_platform)} messages")
print(f"Total: {len(familles_1) + len(familles_2) + len(nouvelle_platform)} messages")

# Explore motivations
motivations = familles_2['Motivations / Pourquoi CALM'].dropna()
print(f"\nSample motivation:\n{motivations.iloc[0]}")
```

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Make sure you've activated the virtual environment and installed requirements:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Excel file not found
**Solution**: Check that the data file is in `data/raw/`. If not, copy it manually:
```bash
cp /path/to/excel/file.xlsx data/raw/
```

### Issue: spaCy model not found
**Solution**: Download the French language model:
```bash
python -m spacy download fr_core_news_md
```

### Issue: Memory error when loading data
**Solution**: If the Excel file is very large, read it in chunks or use specific columns:
```python
df = pd.read_excel(file_path, usecols=['CP', 'Motivations / Pourquoi CALM'])
```

## Additional Tools (Optional)

### For 3D/Avatar Work:
- **Blender** 3.6+ (https://www.blender.org/)
- **Unity** or **Unreal Engine** (for real-time rendering)

### For Audio Processing:
- **Audacity** (for audio editing)
- **ffmpeg** (for audio conversion)

```bash
# Install ffmpeg (Linux)
sudo apt-get install ffmpeg

# Install ffmpeg (Mac)
brew install ffmpeg
```

## Next Steps

1. ✅ Complete setup
2. 📊 Explore the data in Jupyter notebooks
3. 🤖 Start with emotion analysis pipeline
4. 🎤 Experiment with TTS
5. 👤 Design avatar system
6. 🤝 Implement interaction

See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for detailed technical objectives.

## Getting Help

- Check the documentation in `docs/`
- Review [DATA_OVERVIEW.md](DATA_OVERVIEW.md) for data structure
- Contact supervisors:
  - Dana Diminescu: dana.diminescu@telecom-paris.fr
  - Mickael Bouhier: mickael.bouhier@telecom-paris.fr

## Resources

### NLP & Emotion Analysis:
- Hugging Face Transformers: https://huggingface.co/docs/transformers
- spaCy: https://spacy.io/
- French emotion models: Search on https://huggingface.co/models

### Text-to-Speech:
- Coqui TTS: https://github.com/coqui-ai/TTS
- gTTS: https://github.com/pndurette/gTTS
- Microsoft Azure TTS
- Google Cloud TTS

### Avatar & Animation:
- Unity ML-Agents: https://unity.com/products/machine-learning-agents
- Blender Python API: https://docs.blender.org/api/current/
- Ready Player Me: https://readyplayer.me/ (avatar generation)

### Computer Vision:
- OpenCV: https://opencv.org/
- MediaPipe: https://google.github.io/mediapipe/
# Virtual Environment (.venv) Usage

## ✅ Setup Complete

Un environnement virtuel Python a été créé dans `.venv/` et est déjà dans `.gitignore`.

## 🚀 Activation

### Linux / Mac
```bash
source .venv/bin/activate
```

Ou utilise le script d'activation :
```bash
source activate.sh
```

### Windows
```bash
.venv\Scripts\activate
```

## 📦 Installation des dépendances

Les dépendances sont en cours d'installation automatiquement. Pour vérifier :

```bash
source .venv/bin/activate
pip list
```

Pour installer/réinstaller :
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 🛠️ Utilisation

### Lancer Jupyter
```bash
source .venv/bin/activate
jupyter notebook
```

### Lancer un script Python
```bash
source .venv/bin/activate
python src/analysis/emotion_detector.py
```

### Installer un nouveau package
```bash
source .venv/bin/activate
pip install nom-du-package
pip freeze > requirements.txt  # Mettre à jour requirements.txt
```

## 🔴 Désactivation

Pour sortir de l'environnement virtuel :
```bash
deactivate
```

## 📋 Packages installés

Après installation complète, l'environnement contiendra :

- **Data Science** : pandas, numpy, scipy
- **NLP** : transformers, torch, spacy, nltk
- **Visualization** : matplotlib, seaborn, plotly
- **Jupyter** : jupyter, ipykernel, ipywidgets
- **Testing** : pytest, pytest-cov
- **Dev tools** : black, flake8, mypy

## 🔍 Vérifier l'installation

```bash
source .venv/bin/activate
python -c "import pandas; import numpy; import transformers; print('✓ Core packages OK')"
python -m spacy download fr_core_news_md  # Télécharger le modèle français
```

## 🗑️ Supprimer et recréer

Si besoin de repartir à zéro :
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 💡 Bonnes pratiques

1. **Toujours activer** le .venv avant de travailler :
   ```bash
   source .venv/bin/activate
   ```

2. **Vérifier** qu'on est dans le venv (le prompt commence par `(.venv)`) :
   ```bash
   (.venv) user@machine:~/A_FACE_TO_A_MESSAGE$
   ```

3. **Ne jamais commit** le dossier .venv (déjà dans .gitignore)

4. **Mettre à jour requirements.txt** après installation de nouveaux packages :
   ```bash
   pip freeze > requirements.txt
   git add requirements.txt
   git commit -m "Update dependencies"
   ```

## 🐛 Problèmes courants

### "Command 'python' not found"
Utilise `python3` :
```bash
python3 -m venv .venv
```

### "Permission denied"
Rends le script exécutable :
```bash
chmod +x activate.sh
```

### "Module not found" dans Jupyter
Assure-toi que Jupyter utilise le bon kernel :
```bash
source .venv/bin/activate
python -m ipykernel install --user --name=afacetoamessage
```

Puis dans Jupyter : Kernel → Change kernel → afacetoamessage
# Configuration Jupyter pour .venv

## 🎯 Objectif

Configurer Jupyter pour utiliser l'environnement virtuel `.venv` lors de l'exécution des notebooks.

## ⚡ Installation rapide

### Étape 1 : Attendre la fin de l'installation des packages

L'installation des dépendances est en cours. Vérifie qu'elle est terminée :

```bash
# Vérifier si pip install est toujours en cours
ps aux | grep "pip install" | grep -v grep

# Si rien ne s'affiche, l'installation est terminée
```

### Étape 2 : Configurer le kernel Jupyter

Une fois l'installation terminée, exécute le script de configuration :

```bash
./setup_jupyter_kernel.sh
```

Ou manuellement :

```bash
source .venv/bin/activate
python -m ipykernel install --user --name=afacetoamessage --display-name="Python (A Face to a Message)"
```

### Étape 3 : Vérifier l'installation

```bash
jupyter kernelspec list
```

Tu devrais voir :
```
Available kernels:
  afacetoamessage    /home/user/.local/share/jupyter/kernels/afacetoamessage
  python3            /home/user/.local/share/jupyter/kernels/python3
  ...
```

## 🚀 Utilisation dans Jupyter

### Lancer Jupyter

```bash
source .venv/bin/activate
jupyter notebook
```

### Sélectionner le kernel dans un notebook existant

1. Ouvrir le notebook (ex: `01_data_exploration.ipynb`)
2. Menu : **Kernel → Change kernel**
3. Sélectionner : **Python (A Face to a Message)**
4. ✅ Le notebook utilise maintenant le .venv !

### Créer un nouveau notebook avec le bon kernel

1. Dans Jupyter, cliquer sur **New**
2. Sélectionner : **Python (A Face to a Message)**
3. ✅ Nouveau notebook avec le .venv !

## 🔍 Vérifier que le bon kernel est utilisé

Dans une cellule du notebook, exécute :

```python
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

# Vérifier qu'on est bien dans le .venv
assert '.venv' in sys.executable, "❌ Pas dans le .venv!"
print("✅ Kernel utilise bien le .venv")
```

Tu devrais voir quelque chose comme :
```
Python executable: /home/user/LOCAL_TEST/A_FACE_TO_A_MESSAGE/.venv/bin/python
Python version: 3.11.17 ...
✅ Kernel utilise bien le .venv
```

## 📦 Vérifier les packages disponibles

Dans une cellule du notebook :

```python
import pandas as pd
import numpy as np
import transformers
import spacy

print(f"✓ pandas {pd.__version__}")
print(f"✓ numpy {np.__version__}")
print(f"✓ transformers {transformers.__version__}")
print(f"✓ spacy {spacy.__version__}")
```

## 🔧 Configuration avancée

### Renommer le kernel

```bash
jupyter kernelspec list
# Identifier le chemin du kernel

# Éditer le fichier kernel.json
nano ~/.local/share/jupyter/kernels/afacetoamessage/kernel.json

# Modifier "display_name"
```

### Supprimer le kernel

```bash
jupyter kernelspec remove afacetoamessage
```

Puis réinstaller avec `setup_jupyter_kernel.sh`

### Kernel global vs utilisateur

Par défaut, le kernel est installé pour l'utilisateur (`--user`).

Pour un kernel global (nécessite sudo) :
```bash
source .venv/bin/activate
sudo python -m ipykernel install --name=afacetoamessage --display-name="Python (A Face to a Message)"
```

## 🐛 Problèmes courants

### "No module named 'ipykernel'"

L'installation des packages n'est pas terminée. Attends quelques minutes puis réessaye.

Ou installe manuellement :
```bash
source .venv/bin/activate
pip install ipykernel
```

### Le kernel n'apparaît pas dans Jupyter

1. Vérifier qu'il est installé :
   ```bash
   jupyter kernelspec list
   ```

2. Redémarrer Jupyter :
   ```bash
   # Ctrl+C dans le terminal où Jupyter tourne
   jupyter notebook
   ```

3. Rafraîchir la page du navigateur (F5)

### "Kernel died" au démarrage

Le .venv contient peut-être une erreur. Vérifie les logs :

```bash
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
python -c "import ipykernel"
```

Si erreur, réinstalle ipykernel :
```bash
pip install --force-reinstall ipykernel
./setup_jupyter_kernel.sh
```

### Les packages ne sont pas trouvés dans le notebook

Assure-toi que :
1. Le bon kernel est sélectionné (**Python (A Face to a Message)**)
2. Les packages sont installés dans le .venv :
   ```bash
   source .venv/bin/activate
   pip list | grep pandas
   ```

## 📋 Checklist complète

- [ ] Installation des packages terminée (`ps aux | grep pip`)
- [ ] Script `setup_jupyter_kernel.sh` exécuté
- [ ] Kernel visible dans `jupyter kernelspec list`
- [ ] Jupyter lancé avec `.venv` activé
- [ ] Kernel **Python (A Face to a Message)** sélectionné dans le notebook
- [ ] Test `import pandas` fonctionne
- [ ] `sys.executable` pointe vers `.venv/bin/python`

## ✨ Tout fonctionne !

Une fois configuré, tu peux :

1. **Lancer Jupyter** :
   ```bash
   source activate.sh  # Active le .venv
   jupyter notebook
   ```

2. **Ouvrir un notebook** :
   - `01_data_exploration.ipynb`
   - `02_data_cleaning.ipynb`
   - `03_random_message_viewer.ipynb`

3. **Vérifier le kernel** : Doit afficher "Python (A Face to a Message)" en haut à droite

4. **Exécuter les cellules** avec tous les packages du .venv disponibles !

Bon développement ! 🚀
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
