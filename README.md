# A FACE TO A MESSAGE

> Donner un visage aux messages - Physicaliser des témoignages textuels avec l'IA

![Project Type](https://img.shields.io/badge/Project-Research--Creation-blue)
![Institution](https://img.shields.io/badge/Institution-Télécom%20Paris-red)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

## 📖 Overview

We have ~20,000 anonymous messages about hosting refugees from Singa's *Comme à la maison* platform (now *J'accueille*). This project uses AI to analyze each message's emotions and language, then gives it a synthetic voice and an animated avatar, transforming written testimonies into expressive presences that can interact with visitors at the Musée national de l'histoire de l'immigration.

**The goal**: Transform text into embodied, emotional, interactive presence.

```
TEXT → EMOTION ANALYSIS → VOICE → ANIMATED FACE → VISITOR INTERACTION
```

## 🎯 Quick Links

- **[📋 Project Overview](PROJECT_OVERVIEW.md)** - Complete project documentation
- **[📊 Data Overview](DATA_OVERVIEW.md)** - Dataset structure and analysis
- **[🎓 Academic Context](#academic-context)** - Course and supervision info

## 🏗️ Project Structure

```
A_FACE_TO_A_MESSAGE/
├── data/
│   ├── raw/              # Original Excel files with messages
│   └── processed/        # Cleaned and processed datasets
├── src/
│   ├── analysis/         # NLP & emotion analysis modules
│   ├── tts/             # Text-to-Speech integration
│   ├── avatar/          # Avatar animation & rendering
│   └── interaction/     # Visitor detection & tracking
├── notebooks/           # Jupyter notebooks for experimentation
├── models/              # Trained models & configurations
├── config/              # Configuration files
├── tests/               # Unit tests
└── docs/                # Additional documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- [Additional requirements TBD]

### Installation

```bash
# Clone the repository
git clone git@github.com:MaxenceGuinziemba/A_FACE_TO_A_MESSAGE.git
cd A_FACE_TO_A_MESSAGE

# Install dependencies (to be created)
pip install -r requirements.txt
```

## 🔬 Technical Pipeline

### 1. **Emotion Analysis** (`src/analysis/`)
- Analyze text messages for emotional content
- Extract temporal emotional profiles
- Classify sentiment and emotions

### 2. **Voice Synthesis** (`src/tts/`)
- Text-to-Speech conversion
- Prosody modification based on emotions
- Multi-language support

### 3. **Avatar Animation** (`src/avatar/`)
- Parametric facial expressions
- Lip-sync with audio
- Real-time animation

### 4. **Visitor Interaction** (`src/interaction/`)
- Presence detection (camera, touchscreen)
- Gaze tracking
- Interaction triggers

## 📊 Dataset

- **~20,000 messages** from refugee hosting platform
- **Time period**: 2015 - present
- **Languages**: Primarily French, some English
- **Content**: Personal motivations, descriptions, hosting offers

See [DATA_OVERVIEW.md](DATA_OVERVIEW.md) for detailed information.

## 🎓 Academic Context

**Institution**: Télécom Paris  
**Program**: Alternant IA/SD  
**Year**: 2026-2027 (S1)  
**Project Type**: Projet recherche-création

### Supervisors
- Dana Diminescu - dana.diminescu@telecom-paris.fr
- Mickael Bouhier - mickael.bouhier@telecom-paris.fr

### Collaborators
- HI Paris!
- Quentin Lobbé - CNRS
- Musée national de l'histoire de l'immigration

## 🎨 Installation Concept

The final installation will feature a **wall of faces** - multiple animated avatars displayed on a large screen (4m × 1.15m touchscreen at Télécom Paris).

- Visitors approach the wall
- Avatars detect presence and make eye contact
- Visitors select an avatar (touch or proximity)
- Avatar speaks its message with emotional voice and expressions
- Interactive, embodied testimony experience

## 🛠️ Technologies (Planned)

- **Python** - Core orchestration
- **NLP/LLM** - Emotion & linguistic analysis
- **Text-to-Speech** - Voice generation
- **Computer Vision** - Visitor tracking (OpenCV)
- **3D/Animation** - Avatar rendering (Unity/Unreal/Blender/Web)
- **Real-time Systems** - Module communication

## 📈 Development Roadmap

- [x] Project setup and documentation
- [ ] Data loading and exploration
- [ ] Emotion analysis pipeline
- [ ] TTS integration
- [ ] Avatar design and animation
- [ ] Interaction system
- [ ] Integration and testing
- [ ] Final installation demo

## 🤝 Contributing

This is an academic research project. For questions or collaboration:
- Contact supervisors (see above)
- Open an issue for technical discussions

## 📄 License

[To be determined]

## 🙏 Acknowledgments

- **Singa** / **J'accueille** platform for the message corpus
- Musée national de l'histoire de l'immigration for collaboration
- All the anonymous hosts who shared their stories

---

*This project explores the intersection of AI, human testimony, and interactive art to create meaningful experiences around migration and hospitality.*
