import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import argparse

def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)
    
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Fill with Median for Numeric Columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill with 'Unknown' for Object Columns
    object_cols = df.select_dtypes(include=['object']).columns
    df[object_cols] = df[object_cols].fillna('Unknown')

    return df

def analyze_data(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include=['number']).columns
    d = {}

    for col in numeric_cols:
        d[col] = {
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'max': float(df[col].max()),
        }
    
    return d

def export_results(results: dict, output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True) 
    with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

def run_pipeline(input_path: str, output_path: str) -> None:
    df = load_data(input_path)
    df = clean_data(df)
    stats = analyze_data(df)
    d = {
        'metadata':{
            'input_file': input_path,
            'total_rows': df.shape[0],
            'total_columns': df.shape[1],
            'processed_at': datetime.now().isoformat(),
        },
        'statistics': stats
    }

    export_results(d, output_path)     

def main():
    parser = argparse.ArgumentParser(description="Data Pipeline")
    parser.add_argument("input_path", help="Path to the data file")
    parser.add_argument("output_path", help="Path to export the result")
    args = parser.parse_args()


    run_pipeline(args.input_path, args.output_path)


if __name__ == '__main__':
    main()