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
