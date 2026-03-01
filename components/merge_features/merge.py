import argparse
import os
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=str, required=True)
    parser.add_argument("--sentiment", type=str, required=True)
    parser.add_argument("--out", type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    
    length_df = pd.read_parquet(os.path.join(args.length, "data.parquet"))
    sentiment_df = pd.read_parquet(os.path.join(args.sentiment, "data.parquet"))
    
    merged_df = length_df.merge(sentiment_df, on=['asin', 'reviewerID'], how='inner')
    
    os.makedirs(args.out, exist_ok=True)
    merged_df.to_parquet(os.path.join(args.out, "data.parquet"))
    print(f"Merged {len(merged_df)} rows with {len(merged_df.columns)} columns")

if __name__ == "__main__":
    main()
