import pandas as pd

x = pd.read_csv("Functions\csv_files\SPX_raw.csv")


for index, item in x.iterrows():
    date = item[0]
    month = date[0:2]
    day = date[3:5]
    year = date[6:10]
    output = f"{year}-{month}-{day}"
    x.iloc[index, 0] = output

print(x.head())
x.to_csv("Functions\csv_files\SPX.csv")
