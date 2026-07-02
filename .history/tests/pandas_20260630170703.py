import pandas as pd

df = pd.read_parquet("data/processed/2026-06-30_berlin.parquet")
print(df.shape)              # how many rows/columns
print(df.columns.tolist())   # confirm company/location columns exist
print(df[["login", "company", "location"]].head(10))
print(df["company"].notna().sum(), "rows have a company value")
print(df["location"].notna().sum(), "rows have a location value")