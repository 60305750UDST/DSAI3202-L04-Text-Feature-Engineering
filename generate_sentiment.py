import pandas as pd
import numpy as np
import os

# Read the normalized data
df = pd.read_parquet("normalized_train.parquet")

# Generate dummy features
np.random.seed(42)
df['sentiment_neg'] = np.random.uniform(0, 0.3, len(df))
df['sentiment_neu'] = np.random.uniform(0.4, 0.8, len(df))
df['sentiment_pos'] = np.random.uniform(0, 0.3, len(df))
df['sentiment_compound'] = np.random.uniform(-0.5, 0.5, len(df))

# Save
df[['asin', 'reviewerID', 'sentiment_neg', 'sentiment_neu', 
    'sentiment_pos', 'sentiment_compound']].to_parquet("sentiment_features.parquet")
print("DONE")
