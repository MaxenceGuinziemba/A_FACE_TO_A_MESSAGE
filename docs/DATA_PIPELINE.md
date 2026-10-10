# Data Management Plan

## 🎯 Objectives

1. Clean and unify the message corpus from 3 Excel sheets
2. Create a standardized dataset for emotion analysis
3. Build a random message viewer for exploration
4. Prepare data pipeline for TTS and avatar generation

---

## 📊 Current Data Status

### Raw Data (3.3 MB Excel file)
- **Location**: `data/raw/`
- **Git Status**: ✓ In .gitignore (too large, contains personal data)
- **Sheets**: 
  - Familles 1: 1,782 messages
  - Familles 2: 6,810 messages  
  - Nouvelle Plateforme: 477 messages
  - **Total**: ~9,069 messages

### Key Fields
- **Text content**: Motivations, personal descriptions
- **Demographics**: Age, postal code, family composition
- **Hosting details**: Space type, duration, capacity
- **Preferences**: Children acceptance, job sharing, network

---

## 🧹 Data Cleaning Strategy

### 1. Unification
```
3 Excel sheets → Single unified DataFrame
- Standardize column names across sheets
- Add source sheet identifier
- Create unique message IDs
```

### 2. Text Cleaning
- Remove excessive whitespace and newlines
- Fix encoding issues (é, è, à, etc.)
- Standardize quotes and punctuation
- Keep original text authentic (don't over-normalize)
- Handle NaN values appropriately

### 3. Feature Engineering
- Extract department from postal code (first 2 digits)
- Parse age/birth date into consistent format
- Categorize hosting duration (short/medium/long/unlimited)
- Categorize space type (room/apartment/autonomous)
- Binary flags: has_children, accepts_children, shares_network

### 4. Data Quality
- Flag empty/very short messages
- Identify duplicates
- Mark messages with missing critical fields
- Create quality score per message

---

## 📁 What Goes in Git?

### ✅ COMMIT to Repository
```
data/processed/
├── sample_messages_100.csv          # Small sample (100 messages) for demos
├── data_statistics.json             # Dataset statistics
└── column_mapping.json              # Schema documentation

notebooks/
├── 01_data_exploration.ipynb        # Already created
├── 02_data_cleaning.ipynb          # NEW - Main cleaning pipeline
├── 03_random_message_viewer.ipynb  # NEW - Interactive viewer
└── README.md                        # Notebook index
```

### ❌ GITIGNORE (Already configured)
```
data/raw/*.xlsx                      # Original Excel (3.3MB)
data/processed/*.csv                 # Full cleaned dataset
data/processed/*.parquet             # Compressed format
data/processed/*.pkl                 # Pickle files
```

### Why?
- **Raw data**: Too large, may contain personal info
- **Full processed data**: Generated file, reproducible from raw
- **Sample data**: Small enough, useful for demos/tests
- **Statistics**: Metadata, useful for documentation

---

## 📋 Unified Dataset Schema

### Core Fields
```python
{
    'message_id': 'unique identifier (e.g., F1_0001, F2_0001, NP_0001)',
    'source_sheet': 'Familles 1 | Familles 2 | Nouvelle Plateforme',
    
    # Text Content (Main fields for emotion analysis & TTS)
    'motivation_text': 'Motivations / Pourquoi CALM',
    'personal_description': 'Parlez nous de vous', 
    'other_info': 'Autres infos',
    
    # Demographics
    'postal_code': 'CP (as string to preserve leading zeros)',
    'department': 'First 2 digits of postal code',
    'age': 'Age or birth year',
    
    # Hosting Details
    'space_type': 'Chambre | Studio | Logement Autonome | Canapé lit',
    'space_size_m2': 'Taille (numeric)',
    'hosting_duration': 'Temps d\'accueil (standardized)',
    'hosting_duration_category': 'short | medium | long | unlimited',
    'hosting_capacity': 'Number of people',
    
    # Preferences
    'accepts_children': 'boolean',
    'has_children': 'boolean (extracted from description)',
    'teaches_job': 'boolean',
    'shares_network': 'boolean',
    
    # Data Quality
    'text_length': 'Character count of motivation_text',
    'has_motivation': 'boolean',
    'has_description': 'boolean',
    'quality_score': '0-100 (completeness metric)'
}
```

---

## 🎲 Random Message Viewer Features

### Display Components
```
┌─────────────────────────────────────────────────────┐
│ Message #F2_1234 (Familles 2)                       │
├─────────────────────────────────────────────────────┤
│ 📍 Location: Paris (75) - Île-de-France             │
│ 👤 Age: 45 ans | 👨‍👩‍👧‍👦 With children: Oui              │
│ 🏠 Space: Chambre (15 m²)                            │
│ ⏱️  Duration: 3-6 mois                                │
│ 👶 Accepts children: Oui                             │
├─────────────────────────────────────────────────────┤
│ 💭 MOTIVATION:                                       │
│                                                      │
│ "Nous avons de la place et des personnes victimes  │
│  de la guerre civile dans leurs pays ont besoin    │
│  d'un toit. Je serais ravie de pouvoir le leur     │
│  fournir..."                                        │
│                                                      │
├─────────────────────────────────────────────────────┤
│ 🙋 PERSONAL DESCRIPTION:                             │
│                                                      │
│ "Nous sommes une famille de 4, dynamique, nous     │
│  aimons les activités culturelles..."              │
│                                                      │
├─────────────────────────────────────────────────────┤
│ 📊 Quality: ████████░░ 80/100                        │
│ 📝 Text length: 245 characters                       │
└─────────────────────────────────────────────────────┘

[Show Another] [Filter by Region] [Filter by Duration]
```

### Functionality
- Random message selection
- Filter by:
  - Region/Department
  - Hosting duration
  - Accepts children (yes/no)
  - Has personal description
  - Text length (short/medium/long)
- Export selected message for testing
- Batch view (show 5 random messages)

---

## 🔄 Data Pipeline

```
┌──────────────────┐
│   Raw Excel      │
│  (data/raw/)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Load & Parse    │ ← notebooks/02_data_cleaning.ipynb
│  - Read 3 sheets │
│  - Standardize   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Clean Text     │
│  - Whitespace    │
│  - Encoding      │
│  - NaN handling  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Feature Engineer │
│  - Extract dept  │
│  - Categorize    │
│  - Binary flags  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Quality Check    │
│  - Completeness  │
│  - Duplicates    │
│  - Score calc    │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────┐
│        Save Outputs              │
├──────────────────────────────────┤
│ ✓ data/processed/messages.csv    │ ← Full dataset (gitignored)
│ ✓ data/processed/messages.parquet│ ← Compressed (gitignored)
│ ✓ data/processed/sample_100.csv  │ ← Small sample (committed)
│ ✓ data/processed/stats.json      │ ← Statistics (committed)
└──────────────────────────────────┘
         │
         ▼
┌──────────────────┐
│  Ready for:      │
│  - Emotion ML    │
│  - TTS           │
│  - Avatar gen    │
└──────────────────┘
```

---

## 📈 Data Quality Metrics

### Completeness Score (0-100)
```python
quality_score = (
    has_motivation * 40 +           # Essential
    has_description * 20 +          # Important
    has_location * 10 +             # Useful
    has_age * 5 +                   # Nice to have
    has_space_info * 10 +           # Useful
    has_duration * 10 +             # Useful
    (text_length > 50) * 5          # Not too short
)
```

### Filtering for Emotion Analysis
```python
# High-quality messages for initial testing
messages_for_emotion = df[
    (df['quality_score'] >= 60) &          # Good completeness
    (df['text_length'] >= 100) &           # Substantial text
    (df['has_motivation'] == True) &       # Has main text
    (df['motivation_text'].notna())        # Not null
]
```

---

## 🎯 Immediate Next Steps

### Phase 1: Data Cleaning (Now)
1. Create `02_data_cleaning.ipynb`
2. Load raw Excel data
3. Unify and clean
4. Save processed outputs
5. Generate statistics

### Phase 2: Random Viewer (Now)
1. Create `03_random_message_viewer.ipynb`
2. Load cleaned data
3. Build interactive display
4. Add filtering options
5. Export functionality

### Phase 3: Emotion Analysis Prep (Next)
1. Select high-quality subset
2. Test emotion detection models
3. Create emotional profile structure
4. Build annotation pipeline

---

## 🔐 Privacy & Ethics

### Considerations
- Messages are **anonymous** (no names)
- Postal codes give **general location only** (not addresses)
- Keep **original wording intact** (authenticity)
- Don't expose **full dataset publicly** (keep in .gitignore)
- Use **samples** for demos (100 messages max)

### For Avatar Display
- Don't infer demographics from text
- Don't stereotype based on location
- Represent diversity in avatar generation
- Preserve emotional authenticity

---

## 📝 Success Criteria

After data cleaning, we should have:

✅ Single unified CSV/Parquet with ~9,000 messages  
✅ Standardized schema with 20+ fields  
✅ Quality scores for all messages  
✅ Sample dataset for demos (100 messages)  
✅ Statistics file documenting the corpus  
✅ Random message viewer notebook working  
✅ Ready for emotion analysis pipeline  

---

**Next**: Create the data cleaning notebook!
