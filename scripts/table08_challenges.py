"""Table 8. Challenges of spatially explicit ES research in the Global South: key factors, corpus evidence and regional expression.

Qualitative synthesis; the quantitative evidence column is computed in Figs. 6, 8, 12, 13 and Tables 4, 5 and 7.
This table is qualitative, so its content is recorded here exactly as printed in
the article and exported in machine-readable form.

Run from the repository root:  python scripts/table08_challenges.py
"""
from _tables import write_table

CAPTION = 'Challenges of spatially explicit ES research in the Global South: key factors, corpus evidence and regional expression.'
HEAD = ['Challenge domain', 'Key factor / variable', 'Evidence from the corpus', 'Regional expression (Africa | Asia)']
ROWS = [['Research ownership',
  'Location of authorship; leadership; data sovereignty',
  '32.0% (SSA), 37.6% (LAC), 24.9% (S&SE Asia) of region-focused articles lack a Global South-affiliated '
  'author',
  'Africa: externally led, higher-visibility studies (FWCI 4.76 vs 2.32) | Asia: domestic ownership high in '
  'China (7.9% external), lower elsewhere'],
 ['Data and validation',
  'Ground-truth density; uncertainty reporting',
  'Uncertainty/validation mentioned in 9.2% of articles; flat share 2015–2025',
  'Africa: sparse gauges and inventories | Asia: default parameters in multi-scenario chains'],
 ['Methodological transfer',
  'Value coefficients; transferred biophysical tables',
  'ESV coefficients in 960 articles (12.2% of 2025 output); FWCI 2.73',
  'Africa: ESV in Ethiopian and Kenyan highlands | Asia: equivalent-factor ESV in Chinese basins'],
 ['Thematic mismatch',
  'Alignment with livelihood and hazard risks',
  'Food production 9.6%; pollination, flood and cooling < 7% combined; adaptation and food-security concepts '
  'declining',
  'Africa: food, water and drought under-modelled | Asia: urban heat and flood risk rising faster than '
  'research'],
 ['Collaboration structure',
  'South–South linkage; network brokerage',
  'South–South links carry 8.0% of collaborative weight; 61.7% single-country articles',
  'Africa: links routed via Europe (Euro-African community) | Asia: links routed via the USA and Australia'],
 ['Funding and publishing',
  'Funder origin; peer-review traceability; APCs',
  'Chinese funders account for 3,232 of the top-20 funder acknowledgements; 706 records in untracked-review '
  'journals; 75 in predatory-listed outlets',
  'Africa: one national funder (South Africa) among top 20 | Asia: strong domestic funding in China, weaker '
  'in South and Southeast Asia']]
NOTE = 'SSA = sub-Saharan Africa; LAC = Latin America and the Caribbean; S&SE Asia = South and Southeast Asia; APC = article-processing charge.'


def main():
    return write_table(8, 'challenges', CAPTION, HEAD, ROWS, NOTE)


if __name__ == "__main__":
    main()
