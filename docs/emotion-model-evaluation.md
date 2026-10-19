# Évaluer un modèle d'émotions

Le fichier local `data/processed/emotion_eval_sample.csv` contient 100 phrases tirées au hasard de 100 témoignages distincts. Ce CSV est exclu du dépôt avec les autres données du corpus : ne pas l'ajouter à GitHub, car les témoignages peuvent contenir des informations sensibles. Il s'agit d'un échantillon pilote, pas d'une estimation statistique définitive. Annoter les colonnes `gold_*` avant de consulter les prédictions du modèle.

Pour chaque phrase, renseigner indépendamment chaque colonne d'émotion avec `1` (émotion exprimée dans le texte) ou `0` (non exprimée). Plusieurs émotions peuvent être présentes. Si aucune des six émotions n'est exprimée, mettre `0` dans les six colonnes.

- `gold_love` : amour, affection ou attachement exprimé explicitement. Une proposition d'aide ou de solidarité ne suffit pas, à elle seule, à conclure à l'amour.
- `gold_anger` : colère ou irritation exprimée.
- `gold_disgust` : dégoût exprimé.
- `gold_joy` : joie ou plaisir exprimé.
- `gold_fear` : peur ou inquiétude exprimée.
- `gold_sadness` : tristesse ou chagrin exprimé.

Annoter ce qui est dit, sans déduire l'état intérieur de l'auteur à partir du seul sujet décrit. Utiliser `confidence` avec `haute`, `moyenne` ou `faible`, et expliquer les cas ambigus dans `notes`. Laisser les champs d'annotation vides jusqu'à ce que la phrase soit évaluée.

Le modèle GREMO-LING est entraîné sur des entretiens cliniques transcrits, pas sur ce corpus. Sa fiche rapporte un F1 macro de 0,58 pour les catégories émotionnelles. Le résultat de cette évaluation locale devra donc être interprété comme exploratoire. Les textes restent locaux : ne pas les envoyer à un service d'inférence externe.
