# Dengue in Vietnam: when and where does the season hit, and does rain warn us early?

Google Data Analytics Capstone, Track B: own topic, own data, ~30-minute presentation. Analysis in **Python (pandas)**.

**Business task:** identify when in the year and where reported dengue cases in Vietnam rise, and how strongly they follow rainfall and temperature in the preceding months, so a pest-control client can prepare staff, insecticide and campaigns one to two months before each regional peak. Details in [docs/topic_selection.md](docs/topic_selection.md).

**Data:** OpenDengue V1.3.1 (monthly reported cases for 64 provinces, 1994–2010, plus national series to 2025; CC BY 4.0) and NASA POWER monthly weather for 11 provincial capitals (1994–2024). See [docs/data_sources.md](docs/data_sources.md).

## Elevator pitch
> …

## Process
| Phase | Where | Status |
| --- | --- | --- |
| Ask | [docs/topic_selection.md](docs/topic_selection.md) | done |
| Prepare | [docs/data_sources.md](docs/data_sources.md), `scripts/download_data.py` | done |
| Process | notebook §3, [docs/changelog.md](docs/changelog.md) | |
| Analyze | notebook §4 | |
| Share | notebook §5, `figures/`, slides (link) | |
| Act | notebook §6: top insights + further deliverables | |

## Run it
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_data.py      # OpenDengue (~55 MB zip) + NASA POWER, not committed
jupyter lab notebooks/analysis.ipynb
```

Data: OpenDengue, Clarke et al. (2024), *Scientific Data* 11, 296, https://doi.org/10.1038/s41597-024-03120-7 (CC BY 4.0). Weather: NASA Langley Research Center POWER Project, funded through the NASA Earth Science/Applied Science Program.
