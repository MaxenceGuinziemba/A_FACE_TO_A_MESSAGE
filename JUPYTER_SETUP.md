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
