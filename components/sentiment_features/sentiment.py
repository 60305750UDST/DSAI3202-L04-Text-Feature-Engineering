import argparse
import os
import pandas as pd
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--out", type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_parquet(args.data)
    
    np.random.seed(42)
    df['sentiment_neg'] = np.random.uniform(0, 0.3, len(df))
    df['sentiment_neu'] = np.random.uniform(0.4, 0.8, len(df))
    df['sentiment_pos'] = np.random.uniform(0, 0.3, len(df))
    df['sentiment_compound'] = np.random.uniform(-0.5, 0.5, len(df))
    
    os.makedirs(args.out, exist_ok=True)
    df[['asin', 'reviewerID', 'sentiment_neg', 'sentiment_neu', 
        'sentiment_pos', 'sentiment_compound']].to_parquet(
        os.path.join(args.out, "data.parquet")
    )
    print(f"DUMMY sentiment features created for {len(df)} rows")

if __name__ == "__main__":
    main()
