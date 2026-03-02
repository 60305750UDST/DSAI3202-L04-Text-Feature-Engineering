# DSAI3202 — Lab 4: Text Feature Engineering with Azure ML

**Course:** DSAI3202 - Cloud Computing for Data Science and AI  
**Semester:** Winter 2026  
**Student ID:** 60305750  
**Branch:** `lab4_feature_engineering`

---

## Overview

This lab implements a text feature engineering pipeline for Amazon Electronics product reviews using Azure Machine Learning. The pipeline processes a sampled Gold dataset (~300k reviews) and generates structured numerical features for downstream machine learning tasks.

---

## Repository Structure

```
DSAI3202-L04-Text-Feature-Engineering/
├── components/
│   ├── split_dataset/              # Train/val/test split (70/15/15)
│   ├── normalize_text/             # Text cleaning and normalization
│   ├── length_features/            # Word and character count features
│   ├── sentiment_features/         # Sentiment score features (dummy VADER-style)
│   └── merge_features/             # Merges length + sentiment on asin + reviewerID
├── data/
│   └── features_v1_sampled.yml     # Azure ML data asset definition
├── datastores/
│   └── curated_adls.yml            # Azure Blob datastore pointing to curated container
├── feature_store/
│   └── entity_amazon_review.yml    # Feature store entity (asin + reviewerID)
├── pipelines/
│   └── feature_pipeline.yml        # Full pipeline definition
└── README.md
```

---

## Infrastructure

| Resource          | Name                                    |
|-------------------|-----------------------------------------|
| Resource Group    | `rg-60305750`                           |
| ML Workspace      | `Amazon-Electronics-Lab-60305750`       |
| Compute Cluster   | `cpu-cluster` (Standard_DS3_v2, 0–2 nodes) |
| Storage Account   | `amazondatalake60305750`                |
| Container         | `curated`                               |
| Data Asset        | `amazon_electronics_features_v1_sampled:1` |
| Datastore         | `blobkey`                               |

---

## Pipeline Components

### 1. `split_dataset`

Splits the input parquet data into train (70%), validation (15%), and test (15%) sets using `sklearn.model_selection.train_test_split` with `seed=42`.

### 2. `normalize_text`

Cleans raw review text: lowercases, removes URLs, numbers, and punctuation, then filters out reviews shorter than 10 characters.

### 3. `length_features`

Extracts two numerical features per review:

- `review_length_words` — word count
- `review_length_chars` — character count

### 4. `sentiment_features`

Generates four sentiment scores per review using a dummy implementation (seeded random values simulating VADER output):

- `sentiment_neg`
- `sentiment_neu`
- `sentiment_pos`
- `sentiment_compound`

> **Note:** Real VADER (`nltk.sentiment.vader`) can replace the dummy implementation by swapping in `SentimentIntensityAnalyzer` on the `reviewText_normalized` column.

### 5. `merge_features`

Inner-joins length features and sentiment features on `['asin', 'reviewerID']` to produce a unified feature table.

---

## Skipped Components

### `tfidf_features` and `sbert_embeddings`

These components were not implemented due to time spent debugging the `sentiment_features` custom environment. Both folders exist as placeholders. The pipeline was restructured to run successfully without them.

**TF-IDF:** Would use `sklearn.TfidfVectorizer` fit only on training split, applied to val/test. Settings: `max_features=5000`, `stop_words='english'`, `ngram_range=(1,2)`.

**SBERT:** Would use `sentence-transformers` to generate dense semantic embeddings per review capturing contextual meaning beyond word frequency.

--- 

## Environment Fix — Sentiment Component

All other components (`split_dataset`, `normalize_text`, `length_features`, `merge_features`) used the pre-built `AzureML-sklearn-1.1-ubuntu20.04-py38-cpu@latest` environment, which already includes pandas and numpy.

The `sentiment_features` component required a custom environment due to additional pip dependencies. Despite having `pandas=1.5.3` declared in `conda.yml`, the initial environment registration (`sentiment_env:1`) was created without a base Docker image — meaning it was registered but never built, causing a `ModuleNotFoundError: No module named 'pandas'` at runtime.

### Fix

**1. Create `components/sentiment_features/env.yml`** — a proper Azure ML environment spec referencing both a base image and the conda file:

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
name: sentiment_env
version: 2
image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest
conda_file: conda.yml
description: "Environment for sentiment analysis with pandas, nltk, and textblob."
```

**2. Register the environment** using the correct file flag:

```bash
az ml environment create --file components/sentiment_features/env.yml
```

**3.** Register `sentiment_features` component version 2 pointing to `sentiment_env:2`.

**4.** Update `pipelines/feature_pipeline.yml` to reference `azureml:sentiment_features:2`.

### Root Cause

Azure ML CLI v2 requires a base Docker image when creating custom environments. A conda file alone is not sufficient — the environment must be wrapped in an Azure ML environment YAML spec that specifies `image:` alongside `conda_file:`.

---

## Setup & Deployment

### Prerequisites

- Azure ML CLI v2 (`az ml`)
- Access to workspace `Amazon-Electronics-Lab-60305750`

### One-time Setup

```bash
# Set defaults
az configure --defaults group="rg-60305750" workspace="Amazon-Electronics-Lab-60305750"

# Register datastore
az ml datastore create --file datastores/curated_adls.yml

# Register data asset
az ml data create --file data/features_v1_sampled.yml

# Register all components
az ml component create --file components/split_dataset/component.yml
az ml component create --file components/normalize_text/component.yml
az ml component create --file components/length_features/component.yml
az ml environment create --file components/sentiment_features/env.yml
az ml component create --file components/sentiment_features/component.yml --version 2
az ml component create --file components/merge_features/component.yml
```

### Run the Pipeline

```bash
az ml job create --file pipelines/feature_pipeline.yml
```

### Monitor

```bash
az ml job show --name  --query status
az ml job stream --name 
```

---

## Successful Pipeline Run

| Job Name                    | Status          |
|-----------------------------|-----------------|
| `dynamic_sail_n02ww0wwqt`   | **Completed** ✅ |

![alt text](screenshots/successful_pipeline.png)

All steps completed in order:

```
split → normalize_train/val/test → length_train + sentiment_train → merge_all
```

---

## Feature Store

- **Entity:** `AmazonReview` (index columns: `asin`, `reviewerID`)
- Defined in `feature_store/entity_amazon_review.yml`
- Feature store: `amazon-electronics-fs-60305750` (Qatar Central)
