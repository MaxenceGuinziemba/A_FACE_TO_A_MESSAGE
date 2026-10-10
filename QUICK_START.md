# Quick Start Guide

Welcome to **A FACE TO A MESSAGE**! This guide will get you up and running quickly.

## 🚀 5-Minute Setup

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Download French language model
python -m spacy download fr_core_news_md
```

### 2. Verify Data

```bash
# Check that data is available
ls -lh data/raw/
```

You should see the Excel file with refugee hosting messages.

### 3. Start Exploring

```bash
# Launch Jupyter
jupyter notebook
```

Open `notebooks/01_data_exploration.ipynb` and run the cells to explore the data.

## 📊 What You'll Find

### Data
- **~9,000 messages** in the current dataset (path to 20,000)
- **3 sheets**: Familles 1, Familles 2, Nouvelle Plateforme
- **Key fields**: Motivations, personal descriptions, hosting details

### Documentation
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project context and objectives
- **[DATA_OVERVIEW.md](DATA_OVERVIEW.md)** - Dataset structure and characteristics
- **[SETUP.md](SETUP.md)** - Detailed installation and configuration

## 🎯 Core Technical Pipeline

```
1. TEXT MESSAGE
   └─> Extract from Excel

2. EMOTION ANALYSIS
   └─> Use NLP/LLM to detect emotions
   └─> Create temporal emotional profile

3. VOICE SYNTHESIS
   └─> Text-to-Speech conversion
   └─> Apply emotional prosody

4. AVATAR ANIMATION
   └─> Map emotions to facial expressions
   └─> Sync with audio

5. VISITOR INTERACTION
   └─> Detect visitor presence
   └─> Trigger avatar response
```

## 🛠️ Project Modules

| Module | Location | Purpose |
|--------|----------|---------|
| **Analysis** | `src/analysis/` | NLP & emotion detection |
| **TTS** | `src/tts/` | Text-to-speech synthesis |
| **Avatar** | `src/avatar/` | Face animation & rendering |
| **Interaction** | `src/interaction/` | Visitor tracking & triggers |

## 💡 First Tasks

### 1. Data Exploration (30 min)
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```
- Load and explore the message corpus
- Analyze text characteristics
- Identify emotional patterns

### 2. Emotion Analysis Prototype (2-3 hours)
Create a new notebook: `02_emotion_analysis.ipynb`
- Test emotion detection models on French text
- Extract sentiment from sample messages
- Build emotional profile representation

### 3. Voice Synthesis Test (1-2 hours)
Create: `03_tts_experiments.ipynb`
- Test different TTS engines (gTTS, Coqui, etc.)
- Generate audio from sample messages
- Experiment with voice parameters

### 4. Avatar Concept (varies)
- Define facial expression parameters
- Choose avatar technology (Unity/Blender/Web)
- Create simple emotion-to-expression mapping

## 📖 Key Resources

### For NLP & Emotions:
- **CamemBERT**: French BERT model - https://huggingface.co/camembert-base
- **French Sentiment**: https://huggingface.co/models?language=fr&pipeline_tag=text-classification
- **spaCy French**: https://spacy.io/models/fr

### For TTS:
- **Coqui TTS**: https://github.com/coqui-ai/TTS
- **gTTS**: Simple Google TTS - https://gtts.readthedocs.io/

### For Avatar:
- **Ready Player Me**: Easy avatar generation - https://readyplayer.me/
- **Blender Python API**: https://docs.blender.org/api/current/
- **Unity ML-Agents**: https://unity.com/products/machine-learning-agents

## ⚡ Quick Commands

```bash
# Activate environment
source venv/bin/activate

# Run Jupyter
jupyter notebook

# Run tests (when available)
pytest tests/

# Format code
black src/

# Check code style
flake8 src/
```

## 🎓 Academic Context

- **Student**: Maxence GUINZIEMBA-PROKOP
- **Institution**: Télécom Paris
- **Supervisors**: Dana Diminescu, Mickael Bouhier
- **Duration**: Semester 1, 2026-2027

## 🤝 Getting Help

1. Check the documentation:
   - [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Full project details
   - [DATA_OVERVIEW.md](DATA_OVERVIEW.md) - Data structure
   - [SETUP.md](SETUP.md) - Installation help

2. Contact supervisors:
   - dana.diminescu@telecom-paris.fr
   - mickael.bouhier@telecom-paris.fr

## 🎬 Demo Goal

By the end of the project, you should be able to:

1. **Select** a message from the corpus
2. **Analyze** its emotional content automatically
3. **Generate** a voice reading with appropriate emotional tone
4. **Display** an animated avatar with matching facial expressions
5. **Interact** with a visitor who triggers the experience

The complete chain: **MESSAGE → EMOTION → VOICE → FACE → INTERACTION**

## 📅 Next Steps

- [ ] Complete environment setup
- [ ] Explore data in Jupyter notebook
- [ ] Test emotion detection on sample messages
- [ ] Experiment with TTS generation
- [ ] Design avatar expression system
- [ ] Plan visitor interaction mechanism
- [ ] Integrate all components
- [ ] Test full pipeline
- [ ] Prepare final demonstration

Good luck! 🚀
