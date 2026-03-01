import argparse
import os
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--out", type=str, required=True)
    return parser.parse_args()

def main():
    nltk.download('vader_lexicon', quiet=True)
    args = parse_args()
    df = pd.read_parquet(args.data)
    
    sia = SentimentIntensityAnalyzer()
    sentiments = df['reviewText_normalized'].apply(lambda x: sia.polarity_scores(str(x)))
    
    df['sentiment_neg'] = sentiments.apply(lambda x: x['neg'])
    df['sentiment_neu'] = sentiments.apply(lambda x: x['neu'])
    df['sentiment_pos'] = sentiments.apply(lambda x: x['pos'])
    df['sentiment_compound'] = sentiments.apply(lambda x: x['compound'])
    
    os.makedirs(args.out, exist_ok=True)
    df[['asin', 'reviewerID', 'sentiment_neg', 'sentiment_neu', 
        'sentiment_pos', 'sentiment_compound']].to_parquet(
        os.path.join(args.out, "data.parquet")
    )
    print(f"Sentiment features created for {len(df)} rows")

if __name__ == "__main__":
    main()
