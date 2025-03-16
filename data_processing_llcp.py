import pandas as pd

"""
Run variable layout script first this is a python port of 
the original data_processing_llcp.R written in R.
"""

columns: pd.DataFrame = pd.read_csv("data/2023-variable-layout.csv")
columns["File_Width"] = columns["Starting_Column"].diff().fillna(1).astype(int)
columns = columns[columns["File_Width"] > 0]  # Ensure only positive widths

pd.read_fwf(
    "data/LLCP2023ASC/LLCP2023.ASC",
    widths=columns["File_Width"].tolist(),
    names=columns["Variable_Name"].tolist(),
).to_csv("LLCP2023-original.csv")
