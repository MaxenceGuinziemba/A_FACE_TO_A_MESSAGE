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
