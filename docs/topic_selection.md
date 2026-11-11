# Topic selection (Ask)

Candidates (criteria: public data with a clear license, passes ROCCC, big enough to need real cleaning, a clear business question and metric; no genomics/RNA-seq):

| Topic | Hypothetical client & question | Data | Verdict |
| --- | --- | --- | --- |
| **A. Dengue fever by season and province** | Pest-control company / provincial CDC: where and when should resources go? | OpenDengue (CC BY 4.0) + NASA POWER weather | **chosen**: monthly cases for 64 provinces over 17 years, strongest link to a biology background, few existing case studies |
| B. Hanoi air quality | Air purifier company: which months and districts to target? | OpenAQ | uneven station coverage in Hanoi, needs an API key |
| C. Heart disease / diabetes screening | Clinic or insurer: which risk groups to screen first? | UCI, Kaggle | small, little cleaning, many existing notebooks |

## Decision
- **Topic:** seasonal dengue fever in Vietnam, by province, and its link to rainfall and temperature.
- **Client:** a pest-control services company (the same plan works for a provincial Center for Disease Control) that schedules vector-control staff, insecticide stock and community campaigns for the dengue season.
- **Business task:** identify **when in the year and where** reported dengue cases in Vietnam rise, and **how strongly they follow rainfall and temperature in the preceding months**, so the client can prepare resources one to two months before each regional peak.
- **Stakeholders:** operations director (staffing and stock plan), regional managers for the North, Central coast, Central Highlands and South, finance (seasonal budget), public-health partners who share case reports.
- **Audience:** the client's leadership team, non-technical; a 30-minute presentation with one finding per slide and a month-by-month preparation calendar.

## Success metrics
| Metric | Definition |
| --- | --- |
| Cases per month | sum of `dengue_total` per province-month |
| Peak month and season length | month with the highest mean cases; number of months above the province's median month |
| Incidence | cases per 100,000 people (if provincial population is added) |
| Outbreak year | annual cases above the long-run mean + 2 SD (national series) |
| Climate lead time | Spearman correlation between rainfall / temperature in month t−k and cases in month t, k = 0–3 |

## The five guiding questions
1. **What type of company is the client, and what do they want?** A pest-control services company (or provincial CDC) that wants to know when and where to deploy vector-control resources for dengue, and how early it can see a season coming.
2. **What are the key factors?** Seasonality of reported cases, differences between regions and provinces, outbreak years, and the lag between rainfall / temperature and cases (mosquito breeding needs standing water and warmth; virus incubation in the mosquito shortens when it is warm).
3. **What data is appropriate?** Monthly reported dengue cases by province over many years, plus monthly rainfall, temperature and humidity for the same places; population for incidence if available.
4. **Where will the data come from?** OpenDengue V1.3.1 (case counts compiled from Project Tycho, WHO and Vietnam's Ministry of Health; CC BY 4.0) and NASA POWER (MERRA-2 monthly weather, free). See [data_sources.md](data_sources.md).
5. **Who is the audience and what helps them?** Non-technical client leadership: charts whose titles state the finding, a regional season calendar, a ranked list of priority provinces, and a short Tableau dashboard they can filter by province.
