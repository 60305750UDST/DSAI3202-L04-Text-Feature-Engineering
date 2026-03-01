import argparse
import os
import pandas as pd
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--out", type=str, required=True)
    return parser.parse_args()

def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    args = parse_args()
    df = pd.read_parquet(args.data)
    df['reviewText_normalized'] = df['reviewText'].apply(normalize_text)
    df = df[df['reviewText_normalized'].str.len() >= 10]
    
    os.makedirs(args.out, exist_ok=True)
    df.to_parquet(os.path.join(args.out, "data.parquet"))
    print(f"Normalized {len(df)} rows")

if __name__ == "__main__":
    main()
