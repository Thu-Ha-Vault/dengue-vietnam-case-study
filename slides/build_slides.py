"""Build the dengue case study deck (16:9, 15 slides, ~30 minutes) from the figures in ../figures.

Usage: .venv/bin/python slides/build_slides.py  ->  slides/dengue_case_study.pptx
Speaker notes hold the talking points, timing and caveats for each slide.
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
OUT = ROOT / "slides" / "dengue_case_study.pptx"

INK = RGBColor(0x1F, 0x1F, 0x1E)
SOFT = RGBColor(0x6B, 0x6B, 0x68)
ACCENT = RGBColor(0x2A, 0x78, 0xD6)
FOOT = "Data: OpenDengue V1.3.1 (Clarke et al. 2024, CC BY 4.0), 64 provinces 1994–2010 + national series to 2024; NASA POWER weather."

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def text(slide, x, y, w, h, lines, size=20, color=INK, bold=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines if isinstance(lines, list) else [lines]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        p.space_after = Pt(8)
    return box


def slide(title, notes="", kicker=None):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()
    if kicker:
        text(s, 0.6, 0.35, 12, 0.4, kicker, size=14, color=SOFT)
    text(s, 0.6, 0.7 if kicker else 0.45, 12.1, 1.0, title, size=28, bold=True)
    text(s, 0.6, 7.0, 12.2, 0.4, FOOT, size=10, color=SOFT)
    s.notes_slide.notes_text_frame.text = notes
    return s


def figure(s, name, y=1.75, max_h=5.1):
    pic = s.shapes.add_picture(str(FIG / name), Inches(0.6), Inches(y), width=Inches(12.1))
    if pic.height > Inches(max_h):  # keep the chart inside the slide, centred
        ratio = Inches(max_h) / pic.height
        pic.height = Inches(max_h)
        pic.width = Emu(int(pic.width * ratio))
        pic.left = int((prs.slide_width - pic.width) / 2)
    return pic


# 1. Title (1 min)
s = prs.slides.add_slide(BLANK)
text(s, 0.8, 2.0, 11.7, 1.6, "Dengue in Vietnam: when and where does the season hit, and does rain warn us early?", size=38, bold=True)
text(s, 0.8, 4.1, 11.7, 1.0, "A preparation plan for a pest-control client, from 17 years of provincial data", size=22, color=SOFT)
text(s, 0.8, 6.3, 11.7, 0.5, "Google Data Analytics Capstone · Track B", size=14, color=SOFT)
s.notes_slide.notes_text_frame.text = "1 min. Introduce yourself, the client and the one-line question."

# 2. Why it matters (2 min)
s = slide("Why it matters: dengue costs the client most when it arrives unprepared", kicker="Context",
          notes="2 min. Vietnam reports tens to hundreds of thousands of cases a year; 2022 set the record (367,729). "
                "Vector control works best before the peak: larval control and community clean-ups need weeks. "
                "Staff and insecticide bought in a hurry cost more.")
text(s, 0.6, 1.9, 12, 4.6, [
    "Reported cases in Vietnam: 109,000 in a typical recent year, 367,729 in the record year 2022.",
    "Aedes mosquitoes breed in standing water; control works best before cases rise (larval control, clean-ups, spraying).",
    "The client needs to know which months and which provinces to staff, and how early it can see a season coming.",
], size=22)

# 3. Business task (2 min)
s = slide("Business task, stakeholders and metrics", kicker="Ask",
          notes="2 min. Read the business task. Metrics: cases per month, peak month and season length, outbreak years "
                "(mean + 2 SD), Spearman correlation of weather k months earlier with cases.")
text(s, 0.6, 1.9, 12, 4.8, [
    "Business task: identify when in the year and where reported dengue cases rise, and how strongly they follow "
    "rainfall and temperature in the preceding months, so the client can prepare one to two months before each regional peak.",
    "Stakeholders: operations director, regional managers (North, Central coast, Central Highlands, South), finance, public-health partners.",
    "Metrics: cases per month · peak month and season length · outbreak years (mean + 2 SD) · weather lead time (Spearman ρ, lag 0–3 months).",
], size=21)

# 4. Data (2 min)
s = slide("Data: 64 provinces × 17 years of monthly cases, plus weather for 11 provinces", kicker="Prepare",
          notes="2 min. OpenDengue compiles official reports; province data comes from Project Tycho. "
                "The sum of provinces matches the national monthly series exactly. ROCCC: weak on Current, "
                "so 2024 national data is used as a check.")
text(s, 0.6, 1.9, 6.3, 4.8, [
    "OpenDengue V1.3.1 (CC BY 4.0): 12,273 province-months, 1994-02 → 2010-12, 1.38 million reported cases; national series 1960–2024.",
    "NASA POWER: monthly rainfall, temperature and humidity, 1994–2024, at 11 provincial capitals in four regions.",
    "Checks: no negative, missing or duplicate province-months; provinces sum exactly to the national monthly figures.",
], size=19)
text(s, 7.2, 1.9, 5.6, 4.8, [
    "Limitations",
    "• Province data ends in 2010",
    "• Reported cases < real infections",
    "• One weather point per province",
    "• Counts, not incidence (no population)",
    "• Correlation is not causation",
], size=19, color=SOFT)

# 5. Process (2 min)
s = slide("Process: clean, join and lag", kicker="Process",
          notes="2 min. Walk through the change log. Emphasise: no gaps filled with zero; one source per year in the "
                "national series; lags computed on the full weather series so the first months keep their lags.")
text(s, 0.6, 1.9, 12, 4.8, [
    "Filtered the 503 MB global file to Vietnam with DuckDB (0.1 MB), parsed dates, added four regions.",
    "Weather from wide to long; rainfall mm/day → mm/month; lags of 1–3 months for rain, temperature, humidity.",
    "Joined cases and weather on province + year + month: 2,191 rows for 11 provinces.",
    "National annual series: one complete total per year (57 years), no double counting, gaps left empty.",
], size=21)

# 6–12. Findings (12 min)
findings = [
    ("01_national_trend.png", "Finding 1", "Outbreak years reach 4–5× a typical year, and the typical year has doubled",
     "Median year 51k (1980–1999), 63k (2000–2009), 109k (2010–2024). Outbreak years above mean + 2 SD: 1987, 2019, 2022. "
     "1998 (235k) came close. Implication: plan for a rising baseline and keep surge capacity."),
    ("02_heatmap_year_month.png", "Finding 2", "The season is regular: June–November holds 73% of cases",
     "Every row shows the same band from June. Peak in July–October in 15 of 16 years; 1999 peaked in May. "
     "February–April holds only 9.5%: the quiet window for preparation."),
    ("04_top_provinces.png", "Finding 3", "The South carries 68% of cases; ten provinces carry 54%",
     "Ho Chi Minh City averages 7,105 cases a year, then the Mekong Delta. Binh Thuan and Khanh Hoa lead the Central coast. "
     "Counts, not incidence: small provinces with high risk can hide here."),
    ("03_region_profiles.png", "Finding 4", "Regions are staggered: August peaks in the South, October in the North",
     "Highlands and South climb fastest (by July) and peak in August; the Central coast has a July hump and peaks in October; "
     "the North climbs from August and has half of its cases in September–November. Ha Noi 2009: 16,175 cases."),
    ("05_weather_lead.png", "Finding 5", "Weather runs ahead of the season",
     "Rain leads cases by about a month in the Mekong Delta (An Giang 0.58). Temperature leads by 2–3 months in the North "
     "and Centre (Ha Noi 0.52, Da Nang 0.62). This mostly reflects the shared seasonal cycle."),
    ("06_weather_anomaly.png", "Finding 6", "But a wetter-than-usual month does not predict a worse season",
     "After removing the normal seasonal pattern, rain anomalies are unrelated to case anomalies (median ρ ~0). "
     "Warmer-than-usual months give a weak signal, clearest on the Central coast. So: plan by calendar, not by rain forecast."),
    ("07_recent_season_2024.png", "Finding 7", "Recent seasons run later: 2024 stayed high into December",
     "2024 (WHO national monthly figures): June 4.8% of cases vs 9.2% before; December 11.7% vs 7.5%; peak in October. "
     "One year only, but it matches 2016. Keep crews until December."),
]
for fig_name, kicker, title, note in findings:
    s = slide(title, notes="~1.7 min. " + note, kicker=kicker)
    figure(s, fig_name)

# 13. Top insights (2 min)
s = slide("Top insights", kicker="Conclusion",
          notes="2 min. One sentence each, with the number.")
text(s, 0.6, 1.9, 12, 5, [
    "1. A predictable June–November season (73% of cases): the calendar tells you when to prepare.",
    "2. Where matters more than when: the South has 68% of cases, ten provinces 54%.",
    "3. Regions are staggered: August peaks in the South and Highlands, October on the Central coast and in the North.",
    "4. Weather confirms timing but does not forecast severity; bad years (4–5×) need surge capacity.",
    "5. The baseline doubled since the 1990s, and the 2024 season ran later, into December.",
], size=21)

# 14. Recommendations (2 min)
s = slide("Recommendations: a regional preparation calendar", kicker="Act",
          notes="2 min. Tie each recommendation to findings. Mention costs: earlier stocking vs emergency purchases.")
text(s, 0.6, 1.9, 12, 5, [
    "1. Ready by May in the South, Central Highlands and Central coast; ready by July in the North; crews on until December (findings 2, 4, 7).",
    "2. Allocate by burden: about two thirds of capacity to the South (HCMC, Mekong Delta), a quarter to the Central coast "
    "(Binh Thuan, Khanh Hoa), a flexible reserve for the North (findings 3, 4).",
    "3. Use the onset of rains (May–June) as the trigger for larval-control campaigns in the South; sign a surge contract "
    "for outbreak years instead of scaling with rainfall (findings 1, 5, 6).",
], size=21)

# 15. Further work (1 min) + Q&A
s = slide("Next deliverables, then questions", kicker="Further work",
          notes="1 min, then Q&A for the rest of the 30 minutes. Likely questions: why data ends in 2010; why counts not incidence; "
                "how strong is ρ 0.5; what about the 2025 province merger.")
text(s, 0.6, 1.9, 12, 5, [
    "Incidence per 100,000 with provincial population.",
    "Province data after 2010, mapped to the 34 provinces created in 2025.",
    "Early-warning model: lagged cases + temperature anomalies + El Niño, tested on held-out years.",
    "Mosquito indices (Breteau, House index) and district-level cases from the client.",
    "A monthly Tableau dashboard refreshed with new national figures.",
], size=21)

OUT.parent.mkdir(exist_ok=True)
prs.save(OUT)
print(f"saved {OUT} ({len(prs.slides)} slides)")
