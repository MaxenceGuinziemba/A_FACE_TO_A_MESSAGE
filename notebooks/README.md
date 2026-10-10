# Notebooks

Jupyter notebooks for the A FACE TO A MESSAGE project.

## 📓 Notebook Index

### 1. Data Exploration (`01_data_exploration.ipynb`)
**Status**: ✅ Ready  
**Purpose**: Initial exploration of the raw refugee hosting messages data

**What it does**:
- Loads Excel data from 3 sheets
- Analyzes text characteristics (length, language, patterns)
- Explores geographic distribution
- Identifies emotional keywords
- Generates basic statistics

**Run first** to understand the raw data structure.

---

### 2. Data Cleaning (`02_data_cleaning.ipynb`)
**Status**: ✅ Ready  
**Purpose**: Clean, unify, and prepare data for analysis

**What it does**:
- Loads all 3 Excel sheets
- Standardizes column names across sheets
- Cleans text (whitespace, encoding)
- Engineers features (department extraction, categorization)
- Calculates quality scores (0-100)
- Saves processed outputs

**Outputs**:
- `data/processed/messages_unified.csv` - Full dataset (gitignored)
- `data/processed/messages_unified.parquet` - Compressed format (gitignored)
- `data/processed/sample_messages_100.csv` - Small sample for demos (committed)
- `data/processed/dataset_statistics.json` - Statistics (committed)
- `data/processed/column_mapping.json` - Schema docs (committed)

**Run second** to create the clean dataset.

---

### 3. Random Message Viewer (`03_random_message_viewer.ipynb`)
**Status**: ✅ Ready  
**Purpose**: Interactive message exploration tool

**What it does**:
- Displays random messages with rich formatting
- Shows important metadata (location, age, hosting details)
- Interactive filters (quality, region, duration, space type)
- Batch viewing (1-5 messages at once)
- Export functionality for testing

**Features**:
- 🎲 Random selection
- 🔍 Multi-filter options
- 📊 Quality scoring
- 💾 Export for emotion analysis

**Run third** to explore the cleaned data interactively.

---

### 4. Emotion Analysis (`04_emotion_analysis.ipynb`)
**Status**: 🚧 To be created  
**Purpose**: Test and build emotion detection pipeline

**Planned features**:
- Test French emotion detection models
- Extract emotional profiles from messages
- Temporal emotion tracking within messages
- Map emotions to prosody parameters
- Create emotion dataset for TTS/avatar

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r ../requirements.txt

# 2. Download French language model (for NLP)
python -m spacy download fr_core_news_md

# 3. Launch Jupyter
jupyter notebook

# 4. Run notebooks in order:
#    - 01_data_exploration.ipynb
#    - 02_data_cleaning.ipynb
#    - 03_random_message_viewer.ipynb
```

## 📊 Data Pipeline

```
Raw Excel (data/raw/)
        ↓
01_data_exploration.ipynb → Understand structure
        ↓
02_data_cleaning.ipynb → Clean & unify
        ↓
Processed Data (data/processed/)
        ↓
03_random_message_viewer.ipynb → Explore interactively
        ↓
04_emotion_analysis.ipynb → Extract emotions
        ↓
Ready for TTS & Avatar Generation
```

## 📁 Output Files

### Committed to Git
- `data/processed/sample_messages_100.csv` - Demo sample
- `data/processed/dataset_statistics.json` - Corpus stats
- `data/processed/column_mapping.json` - Schema documentation

### Gitignored (Generated)
- `data/processed/messages_unified.csv` - Full dataset
- `data/processed/messages_unified.parquet` - Compressed version
- `data/processed/emotion_test_20.csv` - Test subset for emotion analysis

## 🎯 Data Schema

After cleaning, each message has:

**Core Fields**:
- `message_id` - Unique identifier (F1_0001, F2_0002, NP_0003)
- `source_sheet` - Origin sheet (Familles 1/2, Nouvelle Plateforme)

**Text Content**:
- `motivation_text` - Why they want to host (main field for emotion analysis)
- `personal_description` - Self-description
- `other_info` - Additional context

**Demographics**:
- `postal_code` - 5-digit code
- `department` - First 2 digits
- `age` / `birth_date` - Host age info

**Hosting Details**:
- `space_type` / `space_category` - Room/studio/apartment
- `space_size_m2` - Size in square meters
- `hosting_duration` / `duration_category` - How long (short/medium/long/unlimited)
- `hosting_capacity` - Number of people
- `accepts_children` - Boolean
- `teaches_job` / `shares_network` - Support offered

**Quality Metrics**:
- `quality_score` - 0-100 (completeness metric)
- `text_length` - Character count
- `has_motivation` / `has_description` - Boolean flags

## 🔍 Filtering Examples

### High-Quality Messages
```python
high_quality = df[
    (df['quality_score'] >= 70) &
    (df['has_motivation'] == True) &
    (df['text_length'] >= 100)
]
```

### Paris Region, Long-term Hosting
```python
paris_longterm = df[
    (df['department'].isin(['75', '92', '93', '94', '91', '77', '78', '95'])) &
    (df['duration_category'].isin(['long', 'unlimited']))
]
```

### For Emotion Analysis
```python
emotion_ready = df[
    (df['quality_score'] >= 60) &
    (df['text_length'] >= 50) &
    (df['motivation_text'].notna())
]
```

## 📈 Statistics

After running `02_data_cleaning.ipynb`, check:
- `data/processed/dataset_statistics.json` for full stats
- ~9,000 total messages
- ~70% have motivation text
- ~40% have personal description
- Average text length: ~200 characters
- Top regions: Paris, Lyon, Marseille, Nantes

## 🎨 Message Viewer Features

The `03_random_message_viewer.ipynb` provides:

**Interactive Filters**:
- Minimum quality score (0-100)
- Duration category (short/medium/long/unlimited)
- Space type (room/studio/autonomous/sofa)
- Region (Paris, Lyon, etc.)
- Number of messages to display (1-5)

**Display Format**:
```
┌─────────────────────────────────────┐
│ Message #F2_1234                    │
├─────────────────────────────────────┤
│ 📍 Paris (75)                        │
│ 👤 45 ans                            │
│ 🛏️ Room (15 m²)                      │
│ ⏱️ 3-6 mois                           │
├─────────────────────────────────────┤
│ 💭 MOTIVATION:                       │
│ "Nous voulons aider..."             │
├─────────────────────────────────────┤
│ 📊 Quality: ████████░░ 80/100        │
└─────────────────────────────────────┘
```

## 🔜 Next Steps

1. ✅ Data exploration complete
2. ✅ Data cleaning complete
3. ✅ Message viewer complete
4. 🚧 Create emotion analysis notebook
5. ⏳ Build TTS integration
6. ⏳ Design avatar system
7. ⏳ Implement interaction

See [DATA_MANAGEMENT_PLAN.md](../DATA_MANAGEMENT_PLAN.md) for the full data strategy.
