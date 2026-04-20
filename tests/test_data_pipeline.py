import pandas as pd
import pytest
from pathlib import Path
import json
from tools.data_pipeline import load_data, clean_data, analyze_data, export_results, run_pipeline

def test_load_data_returns_dataframe():
    df = load_data("data/train.csv")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_clean_data_fills_numeric_nulls():
    df = pd.DataFrame({"A": [1.0, None, 3.0], "B": ["x", "y", None]})
    cleaned = clean_data(df)
    assert cleaned["A"].isnull().sum() == 0
    assert cleaned["A"].iloc[1] == 2.0

def test_clean_data_fills_string_nulls():
    df = pd.DataFrame({"A": [1.0, None, 3.0], "B": ["x", "y", None]})
    cleaned = clean_data(df)
    assert cleaned["B"].isnull().sum() == 0
    assert cleaned["B"].iloc[2] == 'Unknown'

def test_analyze_returns_correct_stats():
    df = pd.DataFrame({"A": [1.0, 2.0, 3.0]})
    d = analyze_data(df)
    assert d['A']['mean'] == 2.0
    assert d['A']['median'] == 2.0
    assert d['A']['std'] == 1.0
    assert d['A']['min'] == 1
    assert d['A']['max'] == 3

def test_export_creates_json_file():
    d = {'A': 0, 'B': 1}
    output_path = 'output/test.json'
    export_results(d, output_path)
    assert Path(output_path).exists()

    Path(output_path).unlink()

def test_run_pipeline_end_to_end():
    run_pipeline('data/train.csv', 'output/test_result.json')
    with open('output/test_result.json', "r") as f:
            test = json.load(f)

    assert 'metadata' in test
    assert 'statistics' in test

    Path('output/test_result.json').unlink()