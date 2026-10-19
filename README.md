# A FACE TO A MESSAGE

> Donner un visage aux messages - Give a face to messages

![Project Type](https://img.shields.io/badge/Project-Research--Creation-blue)
![Institution](https://img.shields.io/badge/Institution-Télécom%20Paris-red)

**Transforming ~20,000 refugee hosting messages into interactive, emotional avatars using AI.**

```
TEXT → EMOTION ANALYSIS → VOICE → ANIMATED FACE → VISITOR INTERACTION
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Activate virtual environment
source activate.sh

# Launch Jupyter
jupyter notebook
```

### 2. Process Data

Open and run: `notebooks/02_data_cleaning.ipynb`
- Kernel: **Python (A Face to a Message)**
- Unifies 9,000+ messages from 3 Excel sheets
- Creates standardized dataset

### 3. Explore Messages

Open: `notebooks/03_random_message_viewer.ipynb`
- Interactive message browser
- Filter by quality, region, duration
- Export samples for testing

---

## 📖 Documentation

| File | Description |
|------|-------------|
| **[docs/PROJECT.md](docs/PROJECT.md)** | Complete project context, objectives, and data structure |
| **[docs/SETUP.md](docs/SETUP.md)** | Full installation guide (Python, packages, Jupyter) |
| **[docs/DATA_PIPELINE.md](docs/DATA_PIPELINE.md)** | Data management and processing strategy |
| **[notebooks/README.md](notebooks/README.md)** | Notebook index and workflow |

---

## 🎯 Project Overview

**Context**: ~20,000 anonymous messages from Singa's "Comme à la maison" platform about hosting refugees.

**Goal**: Transform text into embodied, emotional, interactive presence for the Musée national de l'histoire de l'immigration.

**Technical Pipeline**:
1. **Emotion Analysis** - Extract emotional profiles from French text
2. **Voice Synthesis** - Generate speech with emotional prosody  
3. **Avatar Animation** - Animated faces with synchronized expressions
4. **Visitor Interaction** - Detect presence and trigger responses

**Current analysis note**: `notebooks/02_emotion.ipynb` does not assign positive/neutral/negative sentiment: the generic Twitter model tested on the corpus gave misleading negative labels for messages expressing a wish to help. Its current French contextual lexicon provides exploratory signals only and still requires human validation.

**Installation**: Wall of faces (4m × 1.15m touchscreen) - avatars react to visitors

---

## 📊 Dataset

- **~9,000 messages** in current dataset (path to 20,000)
- **3 sources**: Familles 1, Familles 2, Nouvelle Plateforme
- **Content**: Motivations, personal descriptions, hosting details
- **Language**: Primarily French

**Key fields**: Motivation text, location, age, space type, hosting duration, children acceptance

See [docs/PROJECT.md](docs/PROJECT.md) for detailed data structure.

---

## 🏗️ Project Structure

```
A_FACE_TO_A_MESSAGE/
├── data/
│   ├── raw/              # Original Excel (gitignored)
│   └── processed/        # Cleaned datasets
├── src/
│   ├── analysis/         # NLP & emotion detection
│   ├── tts/             # Text-to-speech
│   ├── avatar/          # Avatar animation
│   └── interaction/     # Visitor tracking
├── notebooks/           # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb      ⭐ Start here
│   └── 03_random_message_viewer.ipynb
├── docs/                # Documentation
├── .venv/               # Virtual environment (gitignored)
└── requirements.txt     # Python dependencies
```

---

## 🛠️ Technologies

- **Python 3.11** - Core language
- **NLP**: transformers, spacy, nltk (French models)
- **Data**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Jupyter**: Interactive notebooks
- **Computer Vision**: OpenCV (visitor tracking)

**Next phases**: TTS engines, 3D avatars (Unity/Blender), real-time systems

---

## 📅 Academic Context

**Student**: Maxence GUINZIEMBA-PROKOP  
**Institution**: Télécom Paris (Alternant IA/SD)  
**Year**: 2026-2027 (Semester 1)  
**Project Type**: Projet recherche-création

**Supervisors**:
- Dana Diminescu - dana.diminescu@telecom-paris.fr
- Mickael Bouhier - mickael.bouhier@telecom-paris.fr

**Collaboration**: HI Paris!, CNRS, Musée de l'immigration

---

## 🎯 Current Status

- [x] Repository setup and documentation
- [x] Virtual environment configured
- [x] Data exploration complete
- [x] Data cleaning pipeline ready
- [x] Interactive message viewer ready
- [ ] Emotion analysis (in progress)
- [ ] Voice synthesis integration
- [ ] Avatar system design
- [ ] Visitor interaction prototype

---

## 🤝 Contributing

This is an academic research project. For collaboration:
- Contact supervisors (see above)
- Open issues for technical discussions

---

## 📄 License

[To be determined]

---

**Repository**: https://github.com/MaxenceGuinziemba/A_FACE_TO_A_MESSAGE  
**Branches**:
- `main` - Documentation only
- `data-management` - Code + notebooks + data

---

*Exploring the intersection of AI, human testimony, and interactive art to create meaningful experiences around migration and hospitality.*
