#!/bin/bash
# Setup Jupyter kernel for A FACE TO A MESSAGE project

echo "🔧 Configuration du kernel Jupyter pour le .venv..."
echo ""

# Activer l'environnement virtuel
source .venv/bin/activate

# Vérifier que ipykernel est installé
if ! python -c "import ipykernel" 2>/dev/null; then
    echo "⚠️  ipykernel n'est pas installé. Installation en cours..."
    pip install ipykernel
fi

# Installer le kernel Jupyter
echo "📦 Installation du kernel Jupyter..."
python -m ipykernel install --user --name=afacetoamessage --display-name="Python (A Face to a Message)"

echo ""
echo "✅ Kernel Jupyter installé avec succès!"
echo ""
echo "Kernels disponibles:"
jupyter kernelspec list
echo ""
echo "───────────────────────────────────────────────────────────"
echo "📖 Comment utiliser:"
echo ""
echo "1. Lancer Jupyter:"
echo "   jupyter notebook"
echo ""
echo "2. Dans un notebook, aller dans:"
echo "   Kernel → Change kernel → Python (A Face to a Message)"
echo ""
echo "3. Ou créer un nouveau notebook avec ce kernel:"
echo "   New → Python (A Face to a Message)"
echo ""
echo "✨ Le kernel utilisera maintenant le .venv avec tous les packages installés!"
echo "───────────────────────────────────────────────────────────"
