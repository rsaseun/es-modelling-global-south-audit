"""Table 7. The 20 most prolific authors and the 20 most frequently acknowledged funders.

Inputs : data/processed/authors_top20.csv, data/processed/funders_top20.csv
Output : outputs/tables/Table7_authors_funders.{csv,md,json}

Run from the repository root:  python scripts/table07_authors_funders.py
"""
import pandas as pd

from _tables import DATA, thousands, write_table

CAPTION = "The 20 most prolific authors and the 20 most frequently acknowledged funders."
HEAD = ["Author", "Articles", "FWCI", "Funder", "Country", "Articles"]
NOTE = ("Author counts depend on OpenAlex name disambiguation and should be read as indicative. CNPq, CAPES and FAPESP are "
        "Brazilian federal and São Paulo state agencies; BMBF = German Federal Ministry of Education and Research; "
        "NASA = National Aeronautics and Space Administration.")
FUNDER = {"Fundamental Research Funds for the Central Universities": "Fundamental Research Funds for Central Universities",
          "Ministry of Science and Technology (PRC)": "Ministry of Science and Technology",
          "National Research Foundation (South Africa)": "National Research Foundation"}
COUNTRY = {"CN": "China", "BR": "Brazil", "US": "USA", "EU": "EU", "GB": "UK", "DE": "Germany", "INT": "International", "ZA": "South Africa"}


def main():
    a = pd.read_csv(DATA / "authors_top20.csv")
    f = pd.read_csv(DATA / "funders_top20.csv", keep_default_na=False)
    rows = [[ra["name"], thousands(ra["count"]), f"{ra.fwci:.2f}", FUNDER.get(rf["name"], rf["name"]), COUNTRY[rf.country], thousands(rf["count"])]
            for (_, ra), (_, rf) in zip(a.iterrows(), f.iterrows())]
    return write_table(7, "authors_funders", CAPTION, HEAD, rows, NOTE)


if __name__ == "__main__":
    main()
