# More models, little validation? — code and data

Reproducible code and data for the review article

> **More models, little validation? A reproducible, full-text-tested audit of ecosystem-service modelling of human–environment change in the Global South (1990–2025).** *Human Environment Interaction* (under review).

One Python script regenerates each figure (Figs. 1–14) and each table (Tables 1–9) of the article
from OpenAlex aggregates. The tests check that every regenerated figure is **pixel-identical** to the
published figure and every regenerated table is **cell-for-cell identical** to the published table.

## Quick start

```bash
# from the folder that contains this README
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/make_all.py          # all figures + tables (about 45 s)
python tests/test_figures.py        # pixel identity with the article figures
python tests/test_tables.py         # cell identity with the article tables
```

Any single item can be rebuilt on its own, for example `python scripts/fig08_models_methods.py`
or `python scripts/table05_models_methods.py`.

**Font.** The figures use *Liberation Sans* (metric-compatible with Arial). Install it before running
(`sudo apt install fonts-liberation`, `brew install --cask font-liberation`, or download from
<https://github.com/liberationfonts>). Without it Matplotlib falls back to another font and the figure
test will report differences in glyph shapes, though the data shown are unchanged.

**Cairo.** Fig. 14 is drawn as SVG and converted with `cairosvg`, which needs the Cairo library
(`sudo apt install libcairo2`, `brew install cairo`; on Windows install GTK/Cairo or use WSL).

## Contents

```
README.md               this file
requirements.txt        pinned package versions used for the article
CITATION.cff            how to cite (complete before release)
data/
  README.md             description of every input file
  queries/              OQL retrieval and screened-corpus queries; publisher screen
  processed/            OpenAlex aggregates (CSV/TXT) read by the scripts
  geo/                  Natural Earth 1:50m countries (world-atlas TopoJSON, ISC licence)
  icons/                Lucide icons used in Fig. 14 (ISC licence)
scripts/
  _common.py            paths, palette, Matplotlib style and helpers shared by the figure scripts
  _tables.py            formatting helpers and writer shared by the table scripts
  figNN_*.py            one script per figure
  tableNN_*.py          one script per table
  make_all.py           runs everything; also builds Tables_1-9.xlsx and all_stats.json
tests/
  test_figures.py       pixel-identity check against figure_checksums.json
  test_tables.py        cell-identity check against manuscript_tables.json
outputs/                regenerated results (committed for browsing)
  figures/              FigNN_*.png (600 dpi; Fig. 14 at 1200 dpi), .svg (editable), .pdf (vector, fonts embedded)
  tables/               TableN_*.csv / .md / .json and Tables_1-9.xlsx
  stats/                summary statistics computed while drawing each figure
```

## Figures

| Fig. | Script | Output | Main inputs |
|---|---|---|---|
| 1 | `fig01_screening_flow.py` | `Fig01_screening_flow` | screening counts (in script, = Table 2) |
| 2 | `fig02_growth.py` | `Fig02_growth` | `year_overall.txt` |
| 3 | `fig03_subject_areas.py` | `Fig03_subject_areas` | `year_subfield.csv` |
| 4 | `fig04_top20_themes.py` | `Fig04_top20_themes` | `year_topic.csv`, `topics_top25.csv` |
| 5 | `fig05_concepts.py` | `Fig05_concepts` | `year_keyword.csv`, `keywords_top60.csv` |
| 6 | `fig06_es_categories.py` | `Fig06_ES_categories` | `services_year.csv`, `services_year.txt` |
| 7 | `fig07_es_country_activity_index.py` | `Fig07_ES_country_activity_index` | `services_country.csv`, `country_totals.csv` |
| 8 | `fig08_models_methods.py` | `Fig08_models_methods` | `methods_year_fixed.csv`, `year_overall.txt` |
| 9 | `fig09_geography.py` | `Fig09_geography` | `country_totals.csv`, `geo/countries-50m.json` |
| 10 | `fig10_study_regions.py` | `Fig10_study_regions` | `regions_year.csv`, `regions_year.txt` |
| 11 | `fig11_institutions.py` | `Fig11_institutions` | `institutions_top.csv` |
| 12 | `fig12_collaboration_network.py` | `Fig12_collaboration_network` | `collab_matrix.csv`, `country_totals.csv` |
| 13 | `fig13_equity_challenges.py` | `Fig13_equity_challenges` | `region_collab_gs.csv`, `funders_top20.csv` |
| 14 | `fig14_trace_es_framework.py` | `Fig14_TRACE-ES_framework` | conceptual diagram drawn as SVG at print size (14/11 pt), icons in `data/icons/` |

## Tables

| Table | Script | Computed from |
|---|---|---|
| 1 Search strategy | `table01_search_strategy.py` | qualitative (search facets; see `data/queries/`) |
| 2 Screening stages | `table02_screening.py` | `screening_log.csv`, `relevance_audit.csv` |
| 3 Decadal statistics | `table03_decades.py` | `year_overall.txt` (weighted means, CAGR, exponential fit) |
| 4 ES categories | `table04_es_categories.py` | `services_year.txt` |
| 5 Models and methods | `table05_models_methods.py` | `methods_year_fixed.csv`, `methods_summary.csv`, `year_overall.txt` |
| 6 Top-20 journals | `table06_journals.py` | `sources_top20.csv` |
| 7 Authors and funders | `table07_authors_funders.py` | `authors_top20.csv`, `funders_top20.csv` |
| 8 Challenges | `table08_challenges.py` | qualitative synthesis |
| 9 TRACE-ES framework | `table09_trace_es_framework.py` | qualitative framework |

## Data source and licence

Bibliographic aggregates come from [OpenAlex](https://openalex.org) (CC0). 
Country boundaries come from
Natural Earth via world-atlas (ISC); icons in Fig. 14 from Lucide (ISC). 

Copyright (c) 2026 Saheed A. Raji, Shakirudeen Odunuga & Mayowa Fasona

This dataset used for the study More models, little validation--- by Saheed A. Raji, Shakirudeen Odunuga & Mayowa Fasona is licensed under the Creative Commons Attribution 4.0 International License.
