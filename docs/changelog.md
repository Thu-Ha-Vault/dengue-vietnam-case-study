# Cleaning & transformation change log

## Prepare (2026-11-11)
| Step | Rows | Note |
| --- | ---: | --- |
| Downloaded OpenDengue V1.3.1 national and spatial extracts | 29,540 national rows (128 countries); 503 MB spatial CSV | `scripts/download_data.py`, originals kept in `data/raw/` |
| Vietnam, province level (`S_res = Admin1`), monthly | 12,273 | 64 provinces, 1994-02 → 2010-12; one source (Project Tycho); 0 negative, 0 missing, 0 duplicate province-months |
| Vietnam, national level, all resolutions | 317 | yearly 1960–2022 (gaps), monthly 1995–2012 and 2024–2025, weekly 2016 and 2023 |
| Downloaded NASA POWER monthly weather, 11 provincial capitals, 1994–2024 | 11 files × 3 variables × 31 years | no `-999` values |

## Process (2026-11-11, notebook §3)
| Step | Rows | Note |
| --- | ---: | --- |
| Vietnam province-month rows (raw) | 12,273 | `data/clean/vn_province_month_raw.parquet` (0.1 MB extract of the 503 MB spatial CSV) |
| Parse `calendar_start_date` → `date`, `month`; add region | 12,273 | no rows removed; every province maps to one of 4 regions (`scripts/regions.py`) |
| Rows in complete province-years (used for yearly averages) | 11,640 | 1994 lacks January; provinces created in 1997/2004 start mid-period; Ha Tay ends in 2007 |
| Weather wide → long, 11 locations × 31 years | 4,092 | precipitation mm/day × days in month → mm/month; lags 1–3 computed on the full weather series |
| Join cases and weather on province + year + month | 2,191 | inner join, 11 provinces (Da Nang from 1997) |
| National annual series, one complete total per year | 57 years | annual figure (41), sum of 12 months (15), sum of 52 weeks (1); 2023 (41 weeks) and 2025 (3 months) left out; gaps not filled with 0 |
| Population: province-years 1995–2010 from the statistics office | 1,024 | average population, thousand people; national and regional totals dropped |
| Join cases and population, 2004–2010, Ha Tay merged into Ha Noi | 441 | 63 provinces × 7 years on the same boundaries; names matched with an accent-free key |

Outputs: `data/clean/province_month.parquet`, `province_month_weather.csv`, `national_annual.csv`, `province_year_incidence.csv`, `tableau_*.csv` (including `tableau_incidence.csv` with province centroids for the Tableau map).

## Decisions
- Seasonal and regional averages use 1995–2010 (complete national months; 1994 lacks January).
- Before 1980 the national series is too patchy for a baseline, so outbreak years are defined on 1980–2024 (mean + 2 SD).
- Spearman correlation is computed as the Pearson correlation of ranks (robust to outbreak spikes); anomalies subtract each province's mean for that calendar month, with cases on a log scale.
- Weeks are assigned to the month they start in (2016 check only).
- Incidence is averaged over 2004–2010, the only years in which case counts and population share the same province boundaries.
