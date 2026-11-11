# Cleaning & transformation change log

## Prepare (2026-11-11)
| Step | Rows | Note |
| --- | ---: | --- |
| Downloaded OpenDengue V1.3.1 national and spatial extracts | 29,540 national rows (128 countries); 503 MB spatial CSV | `scripts/download_data.py`, originals kept in `data/raw/` |
| Vietnam, province level (`S_res = Admin1`), monthly | 12,273 | 64 provinces, 1994-02 → 2010-12; one source (Project Tycho); 0 negative, 0 missing, 0 duplicate province-months |
| Vietnam, national level, all resolutions | 317 | yearly 1960–2022 (gaps), monthly 1995–2012 and 2024–2025, weekly 2016 and 2023 |
| Downloaded NASA POWER monthly weather, 11 provincial capitals, 1994–2024 | 11 files × 3 variables × 31 years | no `-999` values |

## Process (from 2026-11-22)
| Date | Step | Rows before | Rows after | Note |
| --- | --- | ---: | ---: | --- |
| | Keep Vietnam province-month rows; parse `calendar_start_date` to `month` | | | |
| | Add region (North, Central coast, Central Highlands, South) to each province | | | |
| | Reshape weather from wide to long; precipitation mm/day → mm/month | | | |
| | Join cases and weather on province + year + month; add lags 1–3 | | | |
| | National annual series: combine yearly, monthly and weekly sources without double counting | | | |
| | … | | | |
