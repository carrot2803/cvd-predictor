from bs4 import BeautifulSoup, ResultSet, Tag
import polars as pl
import requests

URL = "https://www.cdc.gov/brfss/annual_data/2023/llcp_varlayout_23_onecolumn.html"

page = requests.get(URL)
html = BeautifulSoup(page.content, "html.parser")

table: Tag = html.find(class_="table-responsive").find(name="tbody")

rows: ResultSet[Tag] = table.find_all(name="tr")

variables: list[dict[str, str]] = []

for row in rows:
    data: ResultSet[Tag] = row.find_all(name="td")
    layout: dict[str, str] = {
        "Starting_Column": data[0].text.strip(),
        "Variable_Name": data[1].text.strip(),
        "Field_Length": data[2].text.strip(),
    }
    variables.append(layout)

pl.DataFrame(variables).write_csv("data/raw/2023-variable-layout.csv")
