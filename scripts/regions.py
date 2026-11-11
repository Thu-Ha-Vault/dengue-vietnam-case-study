"""Province → region on the 1994–2010 boundaries (64 provinces, OpenDengue spelling).

Four regions used in the case study: North (Red River Delta + northern midlands and mountains), Central coast
(North Central + South Central Coast), Central Highlands, South (Southeast + Mekong Delta).
"""
NORTH = ["HA NOI CITY", "HA TAY", "HAI PHONG CITY", "HAI DUONG", "HUNG YEN", "THAI BINH", "NAM DINH", "HA NAM",
         "NINH BINH", "BAC NINH", "VINH PHUC", "QUANG NINH", "HA GIANG", "CAO BANG", "BAC KAN", "TUYEN QUANG",
         "LAO CAI", "YEN BAI", "THAI NGUYEN", "LANG SON", "BAC GIANG", "PHU THO", "DIEN BIEN", "LAI CHAU", "SON LA",
         "HOA BINH"]
CENTRAL_COAST = ["THANH HOA", "NGHE AN", "HA TINH", "QUANG BINH", "QUANG TRI", "THUA THIEN - HUE", "DA NANG CITY",
                 "QUANG NAM", "QUANG NGAI", "BINH DINH", "PHU YEN", "KHANH HOA", "NINH THUAN", "BINH THUAN"]
HIGHLANDS = ["KON TUM", "GIA LAI", "DAK LAK", "DAK NONG", "LAM DONG"]
SOUTH = ["BINH PHUOC", "TAY NINH", "BINH DUONG", "DONG NAI", "BA RIA-VUNG TAU", "HO CHI MINH CITY", "LONG AN",
         "TIEN GIANG", "BEN TRE", "TRA VINH", "VINH LONG", "DONG THAP", "AN GIANG", "KIEN GIANG", "CAN THO CITY",
         "HAU GIANG", "SOC TRANG", "BAC LIEU", "CA MAU"]
REGION = {p: r for r, ps in [("North", NORTH), ("Central coast", CENTRAL_COAST), ("Central Highlands", HIGHLANDS),
                             ("South", SOUTH)] for p in ps}
ORDER = ["North", "Central coast", "Central Highlands", "South"]
assert len(REGION) == 64
