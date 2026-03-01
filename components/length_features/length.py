import argparse
import os
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--out", type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    df = pd.read_parquet(args.data)
    
    df['review_length_words'] = df['reviewText_normalized'].str.split().str.len()
    df['review_length_chars'] = df['reviewText_normalized'].str.len()
    
    os.makedirs(args.out, exist_ok=True)
    df[['asin', 'reviewerID', 'review_length_words', 'review_length_chars']].to_parquet(
        os.path.join(args.out, "data.parquet")
    )
    print(f"Length features created for {len(df)} rows")

if __name__ == "__main__":
    main()
