"""Download the raw data for the Track B dengue case study into data/raw/ (not committed).

1. OpenDengue V1.3.1 national and spatial extracts (CC BY 4.0), https://opendengue.org
2. NASA POWER monthly weather (T2M, PRECTOTCORR, RH2M), 1994-2024, one CSV per location in data/raw/weather/
3. Average population by province, 1995-2010 (General Statistics Office of Vietnam, table V02.03-07, PxWeb API)
4. Province boundaries, 2008 (geoBoundaries VNM ADM1, simplified GeoJSON, public domain)

Usage: python scripts/download_data.py            (skips files that already exist)
"""
from __future__ import annotations

import csv
import json
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
WEATHER = RAW / "weather"
POPULATION = RAW / "population" / "nso_V02.03-07_population_1995_2010.csv"
BOUNDARIES = RAW / "boundaries" / "geoBoundaries-VNM-ADM1_simplified.geojson"
NSO_TABLE = ("https://pxweb.nso.gov.vn/api/v1/vi/D%C3%A2n%20s%E1%BB%91%20v%C3%A0%20lao%20%C4%91%E1%BB%99ng/"
             "V02.03-07.px")
GEOBOUNDARIES = ("https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/VNM/ADM1/"
                 "geoBoundaries-VNM-ADM1_simplified.geojson")

OPENDENGUE = "https://github.com/OpenDengue/master-repo/raw/main/data/releases/V1.3.1/{name}"
EXTRACTS = ["National_extract_V1_3_1.zip", "Spatial_extract_V1_3_1.zip"]

POWER = (
    "https://power.larc.nasa.gov/api/temporal/monthly/point"
    "?parameters=T2M,PRECTOTCORR,RH2M&community=AG&latitude={lat}&longitude={lon}"
    "&start=1994&end=2024&format=CSV"
)
# Provincial capitals (lat, lon). NASA POWER cells are 0.5 x 0.625 degrees, so the capital stands in for the
# province. adm_1_name matches OpenDengue spelling. Chosen to cover the four regions and the highest burdens.
LOCATIONS = {
    "HA NOI CITY": ("North", 21.03, 105.85),
    "HAI PHONG CITY": ("North", 20.86, 106.68),
    "QUANG TRI": ("Central coast", 16.82, 107.10),
    "DA NANG CITY": ("Central coast", 16.05, 108.20),
    "KHANH HOA": ("Central coast", 12.24, 109.19),
    "BINH THUAN": ("Central coast", 10.93, 108.10),
    "DAK LAK": ("Central Highlands", 12.67, 108.04),
    "HO CHI MINH CITY": ("South", 10.82, 106.63),
    "TIEN GIANG": ("South", 10.36, 106.36),
    "AN GIANG": ("South", 10.38, 105.44),
    "CA MAU": ("South", 9.18, 105.15),
}


def fetch(url: str, dest: Path, tries: int = 4) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"skip  {dest.relative_to(ROOT)}")
        return
    part = dest.with_suffix(dest.suffix + ".part")
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r, open(part, "wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
            part.rename(dest)
            print(f"saved {dest.relative_to(ROOT)} ({dest.stat().st_size / 1e6:.1f} MB)")
            return
        except OSError as e:
            print(f"retry {i + 1}/{tries} {dest.name}: {e}")
            time.sleep(2 ** (i + 1))
    raise SystemExit(f"failed: {url}")


def slug(name: str) -> str:
    return name.lower().replace(" - ", "-").replace(" ", "-")


def fetch_population() -> None:
    """Total average population (thousand people) by province and year, 1995-2010, saved as UTF-8 CSV.
    The JSON response is used because the CSV export loses Vietnamese characters."""
    if POPULATION.exists():
        print(f"skip  {POPULATION.relative_to(ROOT)}")
        return
    POPULATION.parent.mkdir(parents=True, exist_ok=True)
    meta = json.load(urllib.request.urlopen(NSO_TABLE, timeout=120))
    var = {v["code"]: v for v in meta["variables"]}
    areas = dict(zip(var["Tỉnh, thành phố"]["values"], var["Tỉnh, thành phố"]["valueTexts"]))
    years = dict(zip(var["Năm"]["values"], var["Năm"]["valueTexts"]))
    wanted = [c for c, t in years.items() if t.isdigit() and 1995 <= int(t) <= 2010]
    query = {"query": [
        {"code": "Tỉnh, thành phố", "selection": {"filter": "all", "values": ["*"]}},
        {"code": "Dân số trung bình", "selection": {"filter": "item", "values": [var["Dân số trung bình"]["values"][0]]}},
        {"code": "Năm", "selection": {"filter": "item", "values": wanted}},
    ], "response": {"format": "json"}}
    req = urllib.request.Request(NSO_TABLE, data=json.dumps(query).encode(), headers={"Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req, timeout=120))
    with open(POPULATION, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["area", "year", "population_thousand"])
        for row in data["data"]:
            a, _, y = row["key"]
            v = row["values"][0]
            w.writerow([areas[a], int(years[y]), "" if v in ("..", "-", "") else v])
    print(f"saved {POPULATION.relative_to(ROOT)}")


def main() -> None:
    WEATHER.mkdir(parents=True, exist_ok=True)
    BOUNDARIES.parent.mkdir(parents=True, exist_ok=True)
    fetch_population()
    fetch(GEOBOUNDARIES, BOUNDARIES)
    for name in EXTRACTS:
        z = RAW / name
        fetch(OPENDENGUE.format(name=name), z)
        csv = RAW / name.replace(".zip", ".csv")
        if not csv.exists():
            with zipfile.ZipFile(z) as zf:
                zf.extractall(RAW)
            print(f"unzip {csv.relative_to(ROOT)}")
    for name, (_, lat, lon) in LOCATIONS.items():
        fetch(POWER.format(lat=lat, lon=lon), WEATHER / f"{slug(name)}.csv")
        time.sleep(1)  # be gentle with the public API


if __name__ == "__main__":
    main()
