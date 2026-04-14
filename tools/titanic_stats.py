import pandas as pd
import argparse

TARGET_COLUMN = "Survived"

def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    return df

def calculate_overall_rate(df: pd.DataFrame) -> float:
    return round(df[TARGET_COLUMN].mean() * 100, 1)

def calculate_rate_by_column(df: pd.DataFrame, column: str) -> pd.Series:
    return round(df.groupby(column)[TARGET_COLUMN].mean()*100, 1)

def display_results(overall: float, by_sex: pd.Series, by_class: pd.Series) -> None:
    print("=== Titanic Survival Statistics ===")

    print(f'Overall survival rate: {overall}%')
    print("By Gender:")
    for ind in by_sex.index:
        print(f' {ind}: {by_sex[ind]}%')

    print("By Class:")
    for ind in by_class.index:
        if ind > 3:
            ind_str = str(ind) + "th"
        else:
            if ind == 1:
                ind_str = "1st"
            elif ind == 2:
                ind_str = "2nd"
            elif ind == 3:
                ind_str = "3rd"

        print(f' {ind_str}: {by_class[ind]}%')

def main():
    parser = argparse.ArgumentParser(description="Titanic survival statistics")
    parser.add_argument("filepath", help="Path to the Titanic CSV file")
    args = parser.parse_args()

    df = load_data(args.filepath)
    
    overall = calculate_overall_rate(df)
    by_sex = calculate_rate_by_column(df, "Sex")
    by_class = calculate_rate_by_column(df, "Pclass")

    display_results(overall, by_sex, by_class)

if __name__ == "__main__":  
    main()