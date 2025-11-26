import pandas as pd

def clean_dataframe(df: pd.DataFrame):
    report = {}

    # Missing values
    missing = df.isnull().sum()
    report["missing_values"] = missing.to_dict()

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    report["duplicates_removed"] = before - after

    # Convert categorical fields
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().str.lower()

    return df, report
