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
