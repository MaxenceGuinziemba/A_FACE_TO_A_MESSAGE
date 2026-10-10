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
# Data Overview

## Corpus Source

**Original Platform**: Singa's "Comme à la maison" (now "J'accueille")  
**Total Expected Messages**: ~20,000 text messages  
**Current Dataset**: ~9,069 messages (in provided Excel file)

---

## Dataset Structure

The data is organized in an Excel file with **3 sheets**:

### 1. Familles 1 (1,782 messages)
Period: From June 2015 onwards

**Columns**:
- `Trois types d'études`: Study period classification
- `CP`: Postal code (geographic location)
- `Motivations / Pourquoi CALM`: Why they want to host refugees
- `Type d'espace mis à disposition`: Type of space offered
- `Parlez nous de vous`: Personal description
- `Temps d'accueil`: Duration of hosting
- `avec enfants ?`: Can they host children?
- `Partage de réseau/métier ?`: Network/job sharing

### 2. Familles 2 (6,810 messages)
Period: From June 2015 to November 14, 2016, then onwards

**Columns**:
- `CP`: Postal code
- `Age`: Age of host
- `Motivations / Pourquoi CALM`: Hosting motivations
- `Type d'espace mis à disposition`: Space type
- `Taille`: Size in m²
- `Parlez nous de vous`: Personal description
- `Temps d'accueil`: Hosting duration
- `avec enfants ?`: Children accepted?
- `Enseignement métier / partage réseau`: Job teaching/network sharing
- `Capacité d'accueil`: Hosting capacity (number of people)
- `Autres infos`: Additional information

### 3. Nouvelle Plateforme (477 messages)
Period: New platform data

**Columns**:
- `CP`: Postal code
- `Date de naissance`: Birth date (format: YYYYMMDD)
- `Motivations / Pourquoi CALM`: Motivations
- `Type d'espace mis à disposition`: Space type
- `Taille`: Size in m²
- `Parlez nous de vous`: Personal description
- `Temps d'accueil`: Hosting duration
- `avec enfants ?`: Children accepted?
- `Enseignement métier`: Job teaching
- `Partage de réseau`: Network sharing
- `Capacité d'accueil`: Hosting capacity
- `Autres infos`: Additional information

---

## Key Text Fields for Analysis

### 1. Motivations / Pourquoi CALM
**Description**: Why the person/family wants to host refugees  
**Characteristics**: 
- Rich emotional content
- Personal stories and values
- Ranges from 1 sentence to several paragraphs
- Mix of practical and ideological motivations

**Example emotional themes**:
- Solidarity and humanitarianism
- Desire to help people in distress
- Cultural exchange interest
- Family history with migration
- Shock at current migration conditions

### 2. Parlez nous de vous (Tell us about yourself)
**Description**: Personal description of the host family  
**Characteristics**:
- Lifestyle descriptions
- Family composition
- Hobbies and interests
- Professional background
- Personality traits

**Common elements**:
- "Nous sommes une famille de..." (We are a family of...)
- Professional descriptions
- Activity preferences (sports, culture, etc.)
- Personal values and lifestyle choices

### 3. Autres infos (Other information)
**Description**: Additional contextual information  
**Characteristics**:
- Practical constraints
- Location details
- Specific requirements or preferences
- Transportation information

---

## Data Quality Observations

### Missing Values
- Many fields contain `NaN` (Not Available)
- "Parlez nous de vous" is often empty in Familles 1 and some entries in other sheets
- "Taille" (size) has missing values in some entries
- Age/birth date not consistently filled

### Text Characteristics

#### Language:
- Primarily **French**
- Occasional English phrases
- Some messages show multilingual families

#### Length:
- **Short**: Single sentence (e.g., "Aider, agir, partager")
- **Medium**: 2-5 sentences
- **Long**: Full paragraphs with detailed stories

#### Tone:
- Generally positive and welcoming
- Emotional and personal
- Sometimes urgent or passionate
- Often includes family context

#### Writing Style:
- Informal to semi-formal
- Personal pronouns (je, nous, on)
- Direct address to the platform/refugees
- Questions and reflections

---

## Hosting Characteristics

### Space Types
- **Chambre** (Room): Most common, usually 9-15 m²
- **Logement Autonome** (Autonomous housing): Full apartments/studios
- **Studio**: Independent small apartments (25-50 m²)
- **Canapé lit** (Sofa bed): In shared living spaces

### Hosting Duration
- **2 semaines** (2 weeks): Short-term emergency
- **3 mois** (3 months): Common medium-term
- **6-9 mois** (6-9 months): Longer term
- **Plus d'un an** (More than 1 year): Long-term commitment
- **Autant que nécessaire** (As long as necessary): Open-ended
- **Pas de limite** (No limit): Indefinite

### Geographic Distribution (CP - Postal Codes)
- **Paris region**: 75xxx (Paris), 92xxx, 93xxx, 94xxx (suburbs)
- **Major cities**: 69xxx (Lyon), 13xxx (Marseille), 59xxx (Lille)
- **Rural areas**: Various departments across France
- Wide geographic spread across French territory

### Capacity
- **1**: Single person
- **2**: Couple or person + child
- **3**: Small family
- Higher numbers for autonomous housing

---

## Emotional Content Examples

### Solidarity & Urgency:
> "Je suis choquée par les conditions d'accueil des migrants actuellement et nous aimerions pouvoir aider d'une façon ou d'une autre."

### Cultural Exchange:
> "nous aimerions pouvoir faire profiter de cet hébergement à quelqu'un qui aurait besoin de se reconstruire quelques temps et avec qui peut-être nous pourrions découvrir d'autres cultures"

### Personal History:
> "Mon pere etait refugié il y a 40 ans. On veut aider les gens et donner un peu d'espoir."

### Simple Humanity:
> "Je pense qu'il est indispensable d'aider son prochain (je ne suis pas spécialement catho) C'est une question d'humanisme..."

### Practical & Generous:
> "Nous avons de la place et des personnes victimes de la guerre civile dans leurs pays ont besoin d'un toit. Je serais ravie de pouvoir le leur fournir le temps nécessaire parce que nous en avons la possibilité et que c'est tout à fait naturel de le faire."

---

## Data Processing Needs

### For NLP & Emotion Analysis:
1. **Text extraction** from Excel sheets
2. **Cleaning**: Handle NaN values, normalize whitespace
3. **Language detection**: Primarily French, some English
4. **Tokenization**: French-specific tokenizers
5. **Emotion classification**: Multiple emotions per message
6. **Temporal emotion tracking**: How emotions evolve within longer messages

### For Voice Synthesis:
1. **Text normalization**: Expand abbreviations, handle special characters
2. **Sentence segmentation**: Proper pausing and phrasing
3. **Prosody mapping**: Match emotional profile to voice parameters
4. **Multilingual support**: Handle occasional English phrases

### For Avatar Generation:
1. **Demographic extraction**: Age, family composition hints
2. **Personality indicators**: Extract traits from self-descriptions
3. **Emotional state**: Map to facial expressions
4. **Interaction cues**: Determine avatar behavior patterns

---

## Suggested Data Pipeline

```
1. EXTRACTION
   └─ Read Excel sheets
   └─ Combine into unified dataset
   └─ Standardize column names

2. CLEANING
   └─ Handle missing values
   └─ Remove duplicates
   └─ Normalize text (encoding, whitespace)

3. ENRICHMENT
   └─ Add unique IDs
   └─ Parse dates consistently
   └─ Categorize space types
   └─ Standardize duration values

4. ANALYSIS
   └─ Emotion detection
   └─ Sentiment analysis
   └─ Topic modeling
   └─ Named entity recognition

5. PROFILE GENERATION
   └─ Create emotional profile per message
   └─ Map to voice parameters
   └─ Map to facial expressions
   └─ Define interaction behavior

6. EXPORT
   └─ Processed dataset for application
   └─ Metadata for each message
   └─ Emotional profiles
   └─ Voice parameters
```

---

## Ethical Considerations

### Privacy:
- Messages are **anonymous** (identity unknown to public)
- No personal identifying information should be displayed
- Postal codes provide general location only

### Representation:
- Avatars should reflect diversity
- Avoid stereotyping based on message content
- Consider cultural sensitivity in avatar design

### Authenticity:
- Preserve the emotional truth of messages
- Don't distort meaning through translation
- Maintain the spirit of solidarity and humanity

---

## Research Questions for the Data

1. **Emotional Distribution**: What are the most common emotions in the corpus?
2. **Geographic Patterns**: Do emotions vary by region?
3. **Temporal Evolution**: How do motivations change over time (2015-2026)?
4. **Length vs. Emotion**: Do longer messages contain more varied emotions?
5. **Family Context**: How does family composition affect message tone?
6. **Space Type Correlation**: Does the type of space offered correlate with emotional expression?

---

## Next Steps

- [ ] Load Excel data into Python/Pandas
- [ ] Perform exploratory data analysis (EDA)
- [ ] Visualize emotional content distribution
- [ ] Build text preprocessing pipeline
- [ ] Test emotion detection models
- [ ] Create sample emotional profiles
- [ ] Map emotions to voice/avatar parameters
