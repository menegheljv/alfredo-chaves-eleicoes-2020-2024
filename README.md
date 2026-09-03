# The Metamorphosis of Power

*"A metamorfose do poder em Alfredo Chaves: não vivemos mais como nossos pais"* (a nod to Belchior's "Como Nossos Pais"). A case study analyzing municipal election data in Alfredo Chaves, ES (Brazil), built entirely from official public data from the TSE (Brazil's Superior Electoral Court) and cross-referenced with IBGE population, sex, race/color and income data.

**[Read it in Portuguese →](https://claude.ai/code/artifact/22daf01e-c77d-446e-beb4-51d6a1c879a7)** · **[Read it in English →](https://claude.ai/code/artifact/487ac675-6174-4eee-be60-57189dc11525)**

## Context

Between 2004 and 2020, the political group behind this project lost five mayoral elections in a row in Alfredo Chaves, ES. In 2024, the same group elected Hugo Luiz, 25 at the time, the youngest mayor in the history of Espírito Santo. This repository documents the data pipeline used to analyze that turnaround, from raw TSE data to the final case study.

**Full disclosure**: Jorge Gabriel Meneghel (2004 candidate) is my father, and Hugo Luiz (2024 winner) is my brother. This started as campaign work. The data pipeline came after, to understand what actually moved the result.

## What's here

- **`scripts/`**: the Python (pandas) and SQL pipeline. Ingestion, cleaning, normalization and joins, chart generation, and the final HTML build. Covers both the 2020 vs 2024 comparison and the full 2004-2024 historical arc, cross-referenced with IBGE population estimates.
- **`data/`**: raw CSVs pulled from [dadosabertos.tse.jus.br](https://dadosabertos.tse.jus.br), filtered down to Alfredo Chaves, ES, covering every municipal election from 2004 to 2024: votes by section, results by candidate, campaign finance, turnout and abstention, electorate profile, and candidate profile and declared assets.
- **`output/`**: what the pipeline produces. Intermediate tables (CSV), the HTML template, and the final `case_study.html`.

## TSE datasets used

| Dataset | What it's for | Years covered |
|---|---|---|
| Votes by electoral section | Mapping the turnaround section by section | 2004, 2008, 2012, 2016, 2020, 2024 |
| Results by candidate (mayor and city council) | Comparing performance across the full ticket | 2004, 2008, 2012, 2016, 2020, 2024 |
| Campaign finance | Funding and spend efficiency per vote, for every candidate | 2004, 2008, 2012, 2016, 2020, 2024 |
| Turnout detail | Turnout and abstention | 2004, 2008, 2012, 2016, 2020, 2024 |
| Electorate profile | Age and gender composition | 2008, 2012, 2016, 2020, 2024 (not published for 2004) |
| Candidate profile and assets | Age, education, declared wealth | 2008, 2012, 2016, 2020, 2024 (asset data not published for 2004) |
| Registered election polls | Voting-intention trajectory during the 2024 campaign | 2024 only, out of scope for the historical arc |

## IBGE data used

Fetched from the [SIDRA API](https://sidra.ibge.gov.br), municipality code 3200300 (Alfredo Chaves, ES):

| SIDRA table | What it's for |
|---|---|
| 6579 | Annual population estimates, 2004-2024 (cross-referenced with registered voters) |
| 9514 | Population by sex, Census 2022 |
| 9605 | Population by race/color, Census 2022 |
| 10295 | Mean/median per-capita household income by sex and race/color, Census 2022 |

## Methodology

Ingestion and cleaning in `pandas`, joins and aggregations in `SQLite`, charts in `matplotlib`, final build as static HTML with charts embedded as base64. Every finding in the case study traces back to a public TSE dataset. When a number wasn't publicly available, that's stated in the text instead of estimated.

## How to run

```bash
python scripts/pipeline.py
python scripts/vereadores_analysis.py
python scripts/add_locations.py
python scripts/extra_analysis.py
python scripts/candidate_profile_analysis.py
python scripts/historical_arc.py
python scripts/ibge_cruzamento.py
python scripts/ibge_demografico.py
python scripts/viz2.py && python scripts/viz3.py && python scripts/viz4.py && python scripts/viz5.py && python scripts/viz6.py
python scripts/build_artifact.py
```

Produces `output/case_study.html`.
