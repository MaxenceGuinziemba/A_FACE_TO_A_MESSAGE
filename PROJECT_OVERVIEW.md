# A FACE TO A MESSAGE
### Donner un visage aux messages - Physicaliser des témoignages textuels avec l'IA

---

## 📋 Project Information

**Student**: Maxence GUINZIEMBA-PROKOP  
**Program**: Alternant IA/SD (AI/Data Science) - Télécom Paris  
**Academic Year**: 2026-2027 (Semester 1)  
**Project Type**: Projet recherche-création (Research-Creation Project)

### Supervisors
- **Dana Diminescu** - dana.diminescu@telecom-paris.fr
- **Mickael Bouhier** - mickael.bouhier@telecom-paris.fr

### Collaborators
- HI Paris!
- Quentin Lobbé – CNRS (to be confirmed)
- Musée national de l'histoire de l'immigration (Paris)

---

## 🎯 Project Context

We have a corpus of approximately **20,000 text messages** related to hospitality and hosting of refugees, from Singa's *"Comme à la maison"* platform (now renamed *"J'accueille"*).

These messages, written by people whose identity generally remains unknown to the public, constitute testimonies rich in linguistic and emotional information. The corpus has already been the subject of socio-computational analysis combining computer science and sociological methods, as well as interviews with hosted persons, host families, and associative actors.

**A first installation from this work is currently presented in the permanent collection of the Musée national de l'histoire de l'immigration in Paris.**

---

## 💡 Core Concept

**How to transform a text message into a presence capable of speaking, expressing emotions, and interacting with a visitor?**

The principle consists of building a transformation chain using different AI building blocks:

```
TEXT MESSAGE 
  ↓
Linguistic & Emotional Analysis
  ↓
Emotional Profile
  ↓
Synthetic Voice
  ↓
Animated Avatar
  ↓
Interaction with Visitor
```

The AI analyzes the text to extract emotional and linguistic characteristics. This information is used to generate a synthetic voice and control the avatar's facial expressions.

**The goal is not just to have a machine read text, but to transform an abstract testimony into a sensitive and interactive presence.**

---

## 🖼️ Installation: "The Wall of Faces"

The installation will take the form of a large wall of screens or video projection, with the possibility of exploiting the **4m × 1.15m touchscreen wall** available at Télécom Paris.

### Features:
- Multiple faces displayed simultaneously in a grid
- Each face corresponds to a message from the corpus
- Avatars present slight movements and observe their environment while waiting
- When a visitor approaches:
  - An avatar can detect their presence
  - The face can orient its gaze towards them
  - The message can be triggered automatically
  - The visitor can also select a face by touching it
  - The avatar then reads the message with a voice and expression corresponding to its emotional content

**The visitor becomes an actor in the consultation of the corpus.**

---

## 🎭 Giving Personality to Messages

The same message can be presented by different avatars.

The system must allow parametric variation of:
- Face typology
- Apparent age
- Morphological characteristics
- Voice
- Language
- Facial expressions
- Interaction dynamics

**Research dimension**: How does incarnation and interaction modify the emotional reception of a testimony?

### Example Research Question:
> Is a message perceived differently when expressed by a face that resembles us or by a face that is foreign to us?

The project will explore the role of perceived similarity between the emitter and the spectator, as well as the role of gaze, voice, and direct interaction.

---

## 🔧 Technical Objectives

### 1. Emotion Analysis
Develop a pipeline to automatically analyze messages from the corpus and extract an emotional profile.

The profile can be represented over time to track the evolution of emotions throughout the message.

It will be used to control:
- Voice prosody
- Facial expressions
- Certain avatar behaviors

### 2. Voice Synthesis
Implement a Text-to-Speech solution to automatically transform text into speech.

Emotional characteristics can be used to modify certain voice parameters:
- Rhythm
- Intonation
- Energy
- Pauses

### 3. Avatar and Facial Animation
Create or integrate an avatar capable of expressing different emotions.

Students must define a parametric representation of facial expressions allowing control of:
- Eyebrows
- Eyes
- Gaze
- Mouth
- Face orientation

**Animation must be synchronized with speech.**

### 4. Visitor Interaction
Set up a system to detect visitor presence and position.

Different technologies can be experimented with:
- Video tracking by camera
- Computer vision
- Position tracking
- Touchscreen
- Other detection or tracking technologies

The avatar can then look at the visitor, address them, and trigger their testimony.

### 5. Multilingualism
Explore the possibility of presenting the same message in multiple languages:

```
Original Text → Translation → Voice Synthesis → Facial Expression
```

**Objective**: Preserve as much as possible the tonality and emotional characteristics of the message when changing language.

---

## 🏗️ System Architecture

The project must result in a **modular architecture** allowing independent modification of different components:

```
┌─────────────────────────────────────────────────────────┐
│                        CORPUS                            │
│                  Message Selection                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                      IA / NLP                            │
│          Text Analysis & Emotion Extraction              │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                 EMOTIONAL PROFILE                        │
│                 Temporal Representation                  │
└──────────┬──────────────────────────────────┬───────────┘
           ↓                                  ↓
┌──────────────────────┐          ┌──────────────────────┐
│        TTS           │          │       AVATAR         │
│  Voice Generation    │          │ Animation & Expression│
└──────────────────────┘          └──────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                     INTERACTION                          │
│             Visitor Detection & Tracking                 │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│                   INSTALLATION                           │
│              Display on Screen Wall                      │
└─────────────────────────────────────────────────────────┘
```

This architecture will allow easy changes to:
- The corpus
- The language
- The typology of faces
- The behavior of the installation

---

## 💻 Technologies Considered

Technologies can be adapted to student choices and experimentation:

- **Python** for data processing and orchestration
- **AI / LLM models** for linguistic and emotional analysis
- **Text-to-Speech technologies**
- **Face animation or generation models**
- **Blender, Unity, Unreal Engine, or web technologies** for avatars
- **OpenCV and computer vision** for visitor tracking
- **Real-time technologies** for communication between different modules
- **Touchscreen / video projection / screen wall** for rendering

**Note**: It is not required to develop AI models from scratch. The challenge is to understand, integrate, and articulate different technological building blocks to build a coherent experience.

---

## 📊 Available Data

We have access to the refugee hosting messages corpus with the following structure:

### Dataset Statistics (from provided Excel file):
- **Familles 1 sheet**: 1,782 messages (from June 2015 onwards)
- **Familles 2 sheet**: 6,810 messages (from June 2015 to Nov 2016, then onwards)
- **Nouvelle Plateforme sheet**: 477 messages (new platform)
- **Total in current file**: ~9,069 messages

### Message Fields Include:
- **CP** (Postal Code): Geographic location
- **Age / Date of birth**: Age of host family
- **Motivations / Pourquoi CALM**: Why they want to host refugees
- **Type d'espace mis à disposition**: Type of space offered (room, apartment, etc.)
- **Taille**: Size of space (m²)
- **Parlez nous de vous**: Personal description of hosts
- **Temps d'accueil**: Duration of hosting (2 weeks to unlimited)
- **Avec enfants?**: Whether they can host children
- **Enseignement métier / Partage de réseau**: Job teaching/network sharing
- **Capacité d'accueil**: Hosting capacity
- **Autres infos**: Additional information

### Example Message:
```
CP: 7110
Motivation: "Je suis choquée par les conditions d'accueil des migrants 
actuellement et nous aimerions pouvoir aider d'une façon ou d'une autre. 
Nous vivons en Ardèche, avec mon mari et nos deux enfants de 2 et 4 ans, 
dans un petit village de montagne de 400 habitants, Valgorge, au milieu 
de la nature..."
Space: Chambre d'invité (lit 2 places) avec salle de bain privative
Duration: 3 à 9 mois
With children: Oui
```

---

## 🎓 Skills Sought

- Programming and software development
- Python and/or JavaScript
- Basics in artificial intelligence
- Natural Language Processing (NLP)
- Computer vision
- Human-machine interfaces
- Interest in 3D, animation, or real-time environments
- Software systems integration
- Curiosity for interactions between AI, art, design, and social sciences

**No prior expertise in all these areas is necessary.** The project is designed as a multidisciplinary exploration, allowing students to progressively build a prototype from existing technologies.

---

## 📦 Expected Result

The project must result in a **functional prototype** of the "Give a Face to Messages" installation.

During the final demonstration, a visitor should be able to:
1. Present themselves in front of the wall
2. Discover several testimonies embodied by avatars

### The system must demonstrate the complete chain:
```
MESSAGE → EMOTION → VOICE → FACE → INTERACTION
```

The project can also serve as a support for future experiments on how incarnation and interaction modify the emotional reception of a testimony.

---

## 📅 Timeline

- **Subject validation**: September 24, 2026
- **Semester**: S1 (2026-2027)
- **Final presentation**: End of semester (or within 15 days after end of period)

---

## 🔗 Related Work

A first installation from this research is currently exhibited at the **Musée national de l'histoire de l'immigration** in Paris as part of their permanent collection.

This project extends that work by adding voice, face, and interactive presence to the text messages.

---

## 📝 Notes

- The project is not in a company (individual research project)
- Team size: 2-3 students
- The identity of message authors generally remains unknown to the public
- Messages are rich in linguistic and emotional information
- Previous analysis combined computational and sociological methods
