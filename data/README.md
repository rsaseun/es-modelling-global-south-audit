# Data

All inputs are aggregates computed with the open OpenAlex index (CC0 licence) through
OpenAlex Query Language (OQL) calculations on the screened corpus of 7,972 articles
(retrieved October 2026). No article-level or personal data are stored.

## `queries/`
| File | Content |
|---|---|
| `OQL_queries.txt` | Identification query (before screening) and final screened-corpus query, ready to paste into the OpenAlex OQL tab |
| `R0.oql` | Four-facet retrieval query (9,632 records) |
| `C3.oql` | Final screened-corpus query (7,972 articles) |
| `publishers_c1.txt` | Publishers in the corpus checked against the Stop Predatory Journals list (`name\|records`); the 12 matched publishers are excluded by OpenAlex ID in `C3.oql` |

## `processed/`
| File | Used by | Content |
|---|---|---|
| `year_overall.txt` | Fig. 2, Tables 3 and 5, most figures | Articles, mean/median citations, mean FWCI and % open access per year, 1990–2025 |
| `screening_log.csv`, `relevance_audit.csv` | Table 2 | Records excluded at each screening stage; random relevance audit (n = 25) |
| `year_subfield.csv` | Fig. 3 | Articles per year and OpenAlex subfield |
| `year_topic.csv`, `topics_top25.csv` | Fig. 4 | Articles per year and OpenAlex topic; top-25 topics |
| `year_keyword.csv`, `keywords_top60.csv` | Fig. 5 | Articles per year and OpenAlex keyword; top-60 keywords |
| `services_year.csv`, `services_year.txt` | Fig. 6, Table 4 | Articles per ES category and year; whole-set citations and FWCI |
| `services_country.csv` | Fig. 7 | Articles per ES category and country of authorship |
| `methods_year_fixed.csv`, `methods_summary.csv` | Fig. 8, Table 5 | Articles per model/method query and year (InVEST = exact phrase); whole-set impact |
| `country_totals.csv` | Figs. 9 and 12 | Articles, citations and FWCI per country of authorship |
| `regions_year.csv`, `regions_year.txt` | Fig. 10 | Articles per study-area region and year |
| `institutions_top.csv` | Fig. 11 | Most productive institutions (umbrella bodies removed) |
| `collab_matrix.csv` | Fig. 12 | Country co-authorship matrix (30 most productive countries) |
| `region_collab_gs.csv`, `funders_top20.csv` | Fig. 13, Table 7 | Externally led shares by region; most acknowledged funders |
| `sources_top20.csv` | Table 6 | 20 most productive journals |
| `authors_top20.csv` | Table 7 | 20 most prolific authors (OpenAlex disambiguation) |
| `notes.txt` | — | Corpus-level notes (InVEST exact vs stemmed match, precision audit, collaboration bins) |

Means in the processed files are stored to two decimals. The tables print one decimal; where a stored
value ends in 5 and the article value was rounded from the unrounded OpenAlex mean, the table script keeps the
article value and says so in a comment (three cells in total, Tables 4 and 6).

Every group in the processed files was produced by an OQL calculation of the form
`get works where <C3 query>; then, group those works by <year | subfield | topic | keyword | country | institution | source | funder | author | search>; finally, summarize using count, mean citation count, mean FWCI, percent open access`.

## `geo/`
`countries-50m.json` is the Natural Earth 1:50m country layer distributed as TopoJSON by the
[world-atlas](https://github.com/topojson/world-atlas) package (ISC licence, see `LICENSE_world-atlas`).
Map lines delineate study areas and do not necessarily depict accepted national boundaries.
