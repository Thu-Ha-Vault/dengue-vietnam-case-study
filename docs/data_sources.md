# Data sources (Prepare)

Raw files live in `data/raw/` (not committed). Re-create them with `python scripts/download_data.py`.

## 1. Dengue case counts: OpenDengue V1.3.1
| Item | Detail |
| --- | --- |
| Dataset | OpenDengue master repository, release V1.3.1: `National_extract_V1_3_1.csv`, `Spatial_extract_V1_3_1.csv` |
| Publisher | OpenDengue project, https://opendengue.org |
| License | CC BY 4.0. Cite: Clarke, J., Lim, A., Gupte, P., et al. (2024). A global dataset of publicly available dengue case count data. *Scientific Data* 11, 296. https://doi.org/10.1038/s41597-024-03120-7 |
| Download | https://github.com/OpenDengue/master-repo/tree/main/data/releases/V1.3.1 (zip: 0.3 MB and 55 MB; the spatial CSV is 503 MB) |
| Columns | `adm_0_name`, `adm_1_name`, `adm_2_name`, `calendar_start_date`, `calendar_end_date`, `Year`, `dengue_total`, `case_definition_standardised`, `S_res` (spatial resolution), `T_res` (temporal resolution), `UUID` (source id) |

### Vietnam coverage (checked 2026-11-11)
| Level | Resolution | Period | Rows | Original source |
| --- | --- | --- | ---: | --- |
| **Province (Admin1)** | **month** | **1994-02 → 2010-12** | **12,273** | Project Tycho (`TYCHO-ALL-19242017-SV_DF01-00`) |
| National (Admin0) | year | 1960–2022, with gaps | 41 | Project Tycho, literature, Ministry of Health |
| National | month | 14 complete years between 1995 and 2012, 2024-01 → 2025-03 | 183 | Project Tycho, literature, WHO WPRO, WHO |
| National | week | 2016, 2023 | 93 | WHO WPRO bulletins |

- 64 provinces on the 1994–2010 boundaries. Most have all 203 months; later-created provinces start in 1997 (Bac Kan, Bac Lieu, Bac Ninh, Binh Phuoc, Da Nang, Ha Nam, Hung Yen, Phu Tho) or 2004 (Dak Nong, Dien Bien, Hau Giang); Ha Tay ends in 2007 (merged into Hanoi in 2008).
- Province data: 1,379,503 reported cases, case definition "Total", no negative values, no missing values, no duplicate province-months.
- Cross-check: the sum of provinces equals the national monthly series exactly in every year where both exist (1995, 1996, 1998–2000, 2003–2009). Against the national annual figure it is 0.1–2.0% lower in 1997, 2001, 2002 and 2010, and 4.7% lower in 1994 because January 1994 is missing at province level.

## 2. Weather: NASA POWER monthly point data
| Item | Detail |
| --- | --- |
| Dataset | NASA POWER, Monthly & Annual, community AG, MERRA-2 reanalysis on a 0.5° × 0.625° grid |
| Variables | `T2M` air temperature at 2 m (°C), `PRECTOTCORR` corrected precipitation (mm/day), `RH2M` relative humidity at 2 m (%) |
| Period | 1994–2024 |
| Locations | the capital of 11 provinces covering four regions and the highest case counts: Ha Noi, Hai Phong (North); Quang Tri, Da Nang, Khanh Hoa, Binh Thuan (Central coast); Dak Lak (Central Highlands); Ho Chi Minh City, Tien Giang, An Giang, Ca Mau (South). Coordinates in `scripts/download_data.py`. |
| Format | one CSV per location in `data/raw/weather/`: header block, then wide rows `PARAMETER, YEAR, JAN … DEC, ANN` |
| Quality | no missing values (`-999`) in the period |
| License | free and open, no key needed. Acknowledgement: "These data were obtained from the NASA Langley Research Center (LaRC) POWER Project funded through the NASA Earth Science/Applied Science Program." https://power.larc.nasa.gov |

## 3. Population: General Statistics Office of Vietnam
| Item | Detail |
| --- | --- |
| Dataset | Table V02.03-07 "Dân số trung bình phân theo địa phương" (average population by province), total, 1995–2010, thousand people |
| Access | PxWeb API: https://pxweb.nso.gov.vn/api/v1/vi/ (database "Dân số và lao động"); the JSON response is used because the CSV export loses Vietnamese characters |
| Boundaries | population follows the boundaries of each year for the 2004 splits (Dak Nong, Hau Giang, Dien Bien) and Ha Tay until 2007; the 1997 splits are back-cast to the new provinces, so incidence is computed for **2004–2010** only, with Ha Tay added to Ha Noi |
| Use | incidence = cases / population × 100,000 for 63 provinces × 7 years |

## 4. Province boundaries: geoBoundaries
| Item | Detail |
| --- | --- |
| Dataset | geoBoundaries VNM ADM1 (2008 boundaries, 63 provinces plus Con Dao), simplified GeoJSON, commit 9469f09 |
| License | public domain (geoBoundaries, sourced from Wikipedia) |
| Use | choropleth map and province centroids (lat/lon) for the Tableau map. The file has no offshore archipelagos, so the Hoang Sa (Da Nang) and Truong Sa (Khanh Hoa) islands are marked on the map by hand. |

## ROCCC
- **Reliable:** case counts are curated by OpenDengue (peer-reviewed data paper) from official surveillance reports digitised by Project Tycho; weather is a standard NASA reanalysis product.
- **Original:** secondary data. OpenDengue keeps the source id (`UUID`) for every row, so each figure traces back to its original report.
- **Comprehensive:** every province, every month for 17 years, enough for seasonality, regional comparison and lag analysis. No age, sex, serotype or severity breakdown, and no population (incidence needs a separate population source).
- **Current:** the weak point. Province-level data ends in 2010. National monthly data for 2024–2025 is used to check that the seasonal pattern still holds today.
- **Cited:** both sources are documented and citable (DOI for OpenDengue, acknowledgement text for NASA POWER).

## Limitations
- Reported cases understate true infections (many mild cases never see a doctor) and reporting practice can change over time.
- Province boundaries are those of 1994–2010. Vietnam merged Ha Tay into Hanoi in 2008 and reorganised 63 provinces into 34 in 2025, so mapping results to today's provinces needs a crosswalk.
- Weather at one point (the provincial capital) stands in for a whole province.
- Correlation between weather and cases does not prove causation: urbanisation, water storage habits, population immunity, circulating serotypes and control campaigns also matter.
- Incidence covers 2004–2010 only (consistent boundaries); earlier years are compared by counts.
