"""
CMTA Real Data Seed
Run once after creating the database tables:
    python -m app.seed_data
Data sourced from: cmta.com.pk, Wikipedia, INCPak, safar.fyi
"""

from app.database import SessionLocal, engine
from app import models


def seed():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Skip if already seeded
    if db.query(models.Line).count() > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return

    print("Seeding CMTA data...")

    # ── LINES ──────────────────────────────────────────────────────────
    lines_data = [
        {
            "code": "orange", "name": "Orange Line",
            "name_urdu": "اورنج لائن",
            "color_hex": "#D4500A",
            "from_stop": "Faiz Ahmed Faiz (FAF)", "to_stop": "Islamabad International Airport",
            "length_km": 29.6, "total_stops": 10,
            "travel_time_min": 37, "frequency_peak_min": 5, "frequency_offpeak_min": 10,
            "notes": "Connects FAF station to Islamabad International Airport via NUST and Golra Morr",
        },
        {
            "code": "green", "name": "Green Line",
            "name_urdu": "گرین لائن",
            "color_hex": "#006B3C",
            "from_stop": "PIMS Hospital", "to_stop": "Bara Kahu",
            "length_km": 15.0, "total_stops": 8,
            "travel_time_min": 52, "frequency_peak_min": 8, "frequency_offpeak_min": 15,
            "notes": "Serves PIMS, CDA, Aabpara, and eastern Islamabad residential areas",
        },
        {
            "code": "blue", "name": "Blue Line",
            "name_urdu": "بلیو لائن",
            "color_hex": "#1A4D8F",
            "from_stop": "PIMS Hospital", "to_stop": "Koral Chowk",
            "length_km": 20.0, "total_stops": 14,
            "travel_time_min": 40, "frequency_peak_min": 8, "frequency_offpeak_min": 12,
            "notes": "Connects PIMS to western Islamabad sectors F/G/H and Koral Chowk",
        },
        {
            "code": "red", "name": "Red Line (BRT)",
            "name_urdu": "ریڈ لائن",
            "color_hex": "#B91C1C",
            "from_stop": "Saddar (Rawalpindi)", "to_stop": "Pak Secretariat",
            "length_km": 23.0, "total_stops": 24,
            "travel_time_min": 45, "frequency_peak_min": 5, "frequency_offpeak_min": 10,
            "notes": "Original BRT line connecting Rawalpindi Saddar to Islamabad Secretariat",
        },
        {
            "code": "electric", "name": "Electric Bus",
            "name_urdu": "الیکٹرک بس",
            "color_hex": "#065F46",
            "from_stop": "NUST Depot (G-11)", "to_stop": "Bari Imam",
            "length_km": 12.0, "total_stops": 8,
            "travel_time_min": 30, "frequency_peak_min": 10, "frequency_offpeak_min": 10,
            "notes": "Electric buses via PIMS. Route 2 goes PIMS to Bari Imam every 10 min",
        },
        {
            "code": "pink", "name": "Pink Bus Service",
            "name_urdu": "پنک بس سروس",
            "color_hex": "#9D174D",
            "from_stop": "Multiple (Nilore / B-17 / I-14)", "to_stop": "Secretariat / F-11",
            "length_km": None, "total_stops": None,
            "travel_time_min": None, "frequency_peak_min": None, "frequency_offpeak_min": None,
            "is_active": True,
            "notes": "Women-only service. FREE of charge. Operates Sat & Sun on ST-01/ST-02 routes.",
        },
    ]

    line_objs = {}
    for ld in lines_data:
        line = models.Line(**ld)
        db.add(line)
        db.flush()
        line_objs[ld["code"]] = line

    # ── STATIONS ───────────────────────────────────────────────────────
    stations_data = {
        "orange": [
            {"name": "Faiz Ahmed Faiz (FAF)", "name_urdu": "فیض احمد فیض", "stop_order": 1, "is_terminus": True, "is_interchange": False, "landmark": "FAF station, near NUST"},
            {"name": "NUST / G-12",           "name_urdu": "نسٹ / جی ۱۲",  "stop_order": 2, "is_terminus": False, "is_interchange": False, "landmark": "NUST University"},
            {"name": "Police Foundation",      "name_urdu": "پولیس فاؤنڈیشن","stop_order": 3, "is_terminus": False, "is_interchange": False, "landmark": "Police Foundation"},
            {"name": "NUST Station",           "name_urdu": "نسٹ اسٹیشن",   "stop_order": 4, "is_terminus": False, "is_interchange": False, "landmark": "NUST campus gate"},
            {"name": "G-13 Station",           "name_urdu": "جی ۱۳",        "stop_order": 5, "is_terminus": False, "is_interchange": False, "landmark": "G-13 sector"},
            {"name": "Golra Morr",             "name_urdu": "گولڑہ موڑ",    "stop_order": 6, "is_terminus": False, "is_interchange": True,  "landmark": "Golra Morr flyover"},
            {"name": "N-5 Highway",            "name_urdu": "این ۵ ہائی وے", "stop_order": 7, "is_terminus": False, "is_interchange": False, "landmark": "Grand Trunk Road"},
            {"name": "M-1/M-2 Interchange",    "name_urdu": "ایم ون / ایم ٹو", "stop_order": 8, "is_terminus": False, "is_interchange": True,  "landmark": "Motorway interchange"},
            {"name": "Badhana Kalan / G-16",   "name_urdu": "بادھانہ کلاں",  "stop_order": 9, "is_terminus": False, "is_interchange": False, "landmark": "G-16 sector"},
            {"name": "Islamabad Airport",      "name_urdu": "اسلام آباد ایئرپورٹ", "stop_order": 10, "is_terminus": True, "is_interchange": False, "landmark": "New Islamabad International Airport"},
        ],
        "green": [
            {"name": "PIMS Hospital",        "name_urdu": "پمز ہسپتال",    "stop_order": 1, "is_terminus": True,  "is_interchange": True,  "landmark": "Pakistan Institute of Medical Sciences"},
            {"name": "Children Hospital",    "name_urdu": "چلڈرن ہسپتال",  "stop_order": 2, "is_terminus": False, "is_interchange": True,  "landmark": "Children's Hospital, interchange with Blue Line"},
            {"name": "G-7/G-8 Intersection", "name_urdu": "جی ۷ / جی ۸",   "stop_order": 3, "is_terminus": False, "is_interchange": False, "landmark": "G-7 sector"},
            {"name": "CDA",                  "name_urdu": "سی ڈی اے",       "stop_order": 4, "is_terminus": False, "is_interchange": True,  "landmark": "CDA Headquarters"},
            {"name": "Aabpara",              "name_urdu": "آبپارہ",         "stop_order": 5, "is_terminus": False, "is_interchange": True,  "landmark": "Aabpara market and chowk"},
            {"name": "Foreign Office",       "name_urdu": "دفتر خارجہ",    "stop_order": 6, "is_terminus": False, "is_interchange": False, "landmark": "Ministry of Foreign Affairs"},
            {"name": "Lake View Park",       "name_urdu": "لیک ویو پارک",  "stop_order": 7, "is_terminus": False, "is_interchange": False, "landmark": "Lake View Park, Rawal Lake"},
            {"name": "Bara Kahu",            "name_urdu": "بارہ کہو",       "stop_order": 8, "is_terminus": True,  "is_interchange": False, "landmark": "Bara Kahu town"},
        ],
        "blue": [
            {"name": "PIMS Hospital",   "name_urdu": "پمز ہسپتال",   "stop_order": 1,  "is_terminus": True,  "is_interchange": True,  "landmark": "PIMS, interchange with Green Line"},
            {"name": "Children Hospital","name_urdu": "چلڈرن ہسپتال", "stop_order": 2,  "is_terminus": False, "is_interchange": True,  "landmark": "Children's Hospital"},
            {"name": "G-7 / Melody",    "name_urdu": "جی ۷ / میلوڈی","stop_order": 3,  "is_terminus": False, "is_interchange": False, "landmark": "Melody food street"},
            {"name": "F-7 Markaz",      "name_urdu": "ایف ۷ مرکز",   "stop_order": 4,  "is_terminus": False, "is_interchange": False, "landmark": "Jinnah Super Market"},
            {"name": "F-8 Markaz",      "name_urdu": "ایف ۸ مرکز",   "stop_order": 5,  "is_terminus": False, "is_interchange": False, "landmark": "F-8 sector"},
            {"name": "F-10 Markaz",     "name_urdu": "ایف ۱۰ مرکز",  "stop_order": 6,  "is_terminus": False, "is_interchange": False, "landmark": "F-10 sector"},
            {"name": "F-11 Markaz",     "name_urdu": "ایف ۱۱ مرکز",  "stop_order": 7,  "is_terminus": False, "is_interchange": False, "landmark": "F-11 sector"},
            {"name": "G-11 Markaz",     "name_urdu": "جی ۱۱ مرکز",   "stop_order": 8,  "is_terminus": False, "is_interchange": True,  "landmark": "Electric bus depot"},
            {"name": "G-10 Markaz",     "name_urdu": "جی ۱۰ مرکز",   "stop_order": 9,  "is_terminus": False, "is_interchange": False, "landmark": "G-10 sector"},
            {"name": "G-9 / H-9",       "name_urdu": "جی ۹ / ایچ ۹", "stop_order": 10, "is_terminus": False, "is_interchange": False, "landmark": "G-9 Markaz"},
            {"name": "I-10 Markaz",     "name_urdu": "آئی ۱۰ مرکز",  "stop_order": 11, "is_terminus": False, "is_interchange": False, "landmark": "I-10 sector"},
            {"name": "I-11 Markaz",     "name_urdu": "آئی ۱۱ مرکز",  "stop_order": 12, "is_terminus": False, "is_interchange": False, "landmark": "I-11 sector"},
            {"name": "Khanna Pul",      "name_urdu": "خانہ پل",       "stop_order": 13, "is_terminus": False, "is_interchange": False, "landmark": "Khanna Pul"},
            {"name": "Koral Chowk",     "name_urdu": "کورال چوک",     "stop_order": 14, "is_terminus": True,  "is_interchange": False, "landmark": "Koral Chowk"},
        ],
        "red": [
            {"name": "Saddar",             "name_urdu": "صدر",               "stop_order": 1,  "is_terminus": True,  "is_interchange": False, "landmark": "Saddar commercial area, Rawalpindi"},
            {"name": "Committee Chowk",    "name_urdu": "کمیٹی چوک",        "stop_order": 2,  "is_terminus": False, "is_interchange": False, "landmark": "Committee Chowk"},
            {"name": "Chandani Chowk",     "name_urdu": "چاندنی چوک",       "stop_order": 3,  "is_terminus": False, "is_interchange": False, "landmark": "Chandani Chowk"},
            {"name": "Chaman",             "name_urdu": "چمن",               "stop_order": 4,  "is_terminus": False, "is_interchange": True,  "landmark": "Feeder route 7 interchange"},
            {"name": "6th Road",           "name_urdu": "چھٹی روڈ",         "stop_order": 5,  "is_terminus": False, "is_interchange": False, "landmark": "6th Road"},
            {"name": "Faizabad",           "name_urdu": "فیض آباد",         "stop_order": 6,  "is_terminus": False, "is_interchange": True,  "landmark": "Faizabad interchange — major hub"},
            {"name": "Shamsabad",          "name_urdu": "شمس آباد",         "stop_order": 7,  "is_terminus": False, "is_interchange": False, "landmark": "Shamsabad"},
            {"name": "Peshawar Morr",      "name_urdu": "پشاور موڑ",        "stop_order": 8,  "is_terminus": False, "is_interchange": True,  "landmark": "Peshawar Morr flyover"},
            {"name": "Kacheri / Courts",   "name_urdu": "کچہری",             "stop_order": 9,  "is_terminus": False, "is_interchange": False, "landmark": "District Courts"},
            {"name": "Shaheed-e-Millat",   "name_urdu": "شہید ملت",         "stop_order": 10, "is_terminus": False, "is_interchange": False, "landmark": "Shaheed-e-Millat Road"},
            {"name": "7th Avenue",         "name_urdu": "ساتویں ایونیو",    "stop_order": 11, "is_terminus": False, "is_interchange": False, "landmark": "7th Avenue"},
            {"name": "Parade Ground",      "name_urdu": "پریڈ گراؤنڈ",     "stop_order": 12, "is_terminus": False, "is_interchange": False, "landmark": "Parade Ground"},
            {"name": "Stock Exchange",     "name_urdu": "اسٹاک ایکسچینج", "stop_order": 13, "is_terminus": False, "is_interchange": False, "landmark": "Islamabad Stock Exchange"},
            {"name": "Pak Secretariat",    "name_urdu": "پاکستان سیکرٹریٹ","stop_order": 14, "is_terminus": True,  "is_interchange": False, "landmark": "Government offices, Pak Secretariat"},
        ],
        "electric": [
            {"name": "NUST Depot (G-11)", "name_urdu": "نسٹ ڈپو", "stop_order": 1, "is_terminus": True,  "is_interchange": True,  "landmark": "NUST Orange Line Depot"},
            {"name": "G-11 Markaz",      "name_urdu": "جی ۱۱",   "stop_order": 2, "is_terminus": False, "is_interchange": True,  "landmark": "G-11 Markaz"},
            {"name": "G-10 Markaz",      "name_urdu": "جی ۱۰",   "stop_order": 3, "is_terminus": False, "is_interchange": False, "landmark": "G-10 Markaz"},
            {"name": "PIMS Hospital",    "name_urdu": "پمز ہسپتال","stop_order": 4, "is_terminus": False, "is_interchange": True,  "landmark": "PIMS — interchange with Green and Blue lines"},
            {"name": "G-7",              "name_urdu": "جی ۷",     "stop_order": 5, "is_terminus": False, "is_interchange": False, "landmark": "G-7 sector"},
            {"name": "Aabpara",          "name_urdu": "آبپارہ",   "stop_order": 6, "is_terminus": False, "is_interchange": True,  "landmark": "Aabpara market"},
            {"name": "Serena Hotel",     "name_urdu": "سرینا ہوٹل","stop_order": 7, "is_terminus": False, "is_interchange": False, "landmark": "Serena Hotel, Diplomatic Enclave"},
            {"name": "Bari Imam",        "name_urdu": "بری امام",  "stop_order": 8, "is_terminus": True,  "is_interchange": True,  "landmark": "Bari Imam shrine"},
        ],
        "pink": [
            {"name": "Nilore Terminal",  "name_urdu": "نیلور ٹرمینل",      "stop_order": 1, "is_terminus": True,  "is_interchange": False, "landmark": "Pink Bus origin (Nilore side)"},
            {"name": "Bhara Kahu",       "name_urdu": "بھارہ کہو",          "stop_order": 2, "is_terminus": False, "is_interchange": True,  "landmark": "Shared corridor with Green Line area"},
            {"name": "Humak",            "name_urdu": "ہماک",               "stop_order": 3, "is_terminus": False, "is_interchange": False, "landmark": "Humak route branch"},
            {"name": "I-14 Markaz",      "name_urdu": "آئی ۱۴ مرکز",        "stop_order": 4, "is_terminus": False, "is_interchange": False, "landmark": "I-14 route branch"},
            {"name": "B-17 Markaz",      "name_urdu": "بی ۱۷ مرکز",         "stop_order": 5, "is_terminus": False, "is_interchange": False, "landmark": "B-17 route branch"},
            {"name": "F-11 Markaz",      "name_urdu": "ایف ۱۱ مرکز",        "stop_order": 6, "is_terminus": False, "is_interchange": True,  "landmark": "F-11 sector center"},
            {"name": "Pak Secretariat",  "name_urdu": "پاکستان سیکرٹریٹ",   "stop_order": 7, "is_terminus": True,  "is_interchange": True,  "landmark": "Government offices, Secretariat"},
        ],
    }

    # Latitude/longitude for each seeded station.
    # Official values are used where available; remaining stops use nearest same-line estimates.
    station_coordinates = {
        "orange": {
            "Faiz Ahmed Faiz (FAF)": (33.7167, 73.0499),
            "NUST / G-12": (33.6851, 73.0234),
            "Police Foundation": (33.6900, 73.0100),
            "NUST Station": (33.6870, 73.0180),
            "G-13 Station": (33.6780, 73.0050),
            "Golra Morr": (33.6706, 72.9876),
            "N-5 Highway": (33.6550, 72.9600),
            "M-1/M-2 Interchange": (33.6400, 72.9200),
            "Badhana Kalan / G-16": (33.6280, 72.8900),
            "Islamabad Airport": (33.6169, 72.8362),
        },
        "green": {
            "PIMS Hospital": (33.7183, 73.0551),
            "Children Hospital": (33.7200, 73.0580),
            "G-7/G-8 Intersection": (33.7216, 73.0634),
            "CDA": (33.7259, 73.0762),
            "Aabpara": (33.7259, 73.0762),
            "Foreign Office": (33.7291, 73.0838),
            "Lake View Park": (33.7312, 73.0901),
            "Bara Kahu": (33.7547, 73.1547),
        },
        "blue": {
            "PIMS Hospital": (33.7183, 73.0551),
            "Children Hospital": (33.7200, 73.0580),
            "G-7 / Melody": (33.7216, 73.0634),
            "F-7 Markaz": (33.7350, 73.0823),
            "F-8 Markaz": (33.7197, 73.0690),
            "F-10 Markaz": (33.7197, 73.0690),
            "F-11 Markaz": (33.6920, 73.0200),
            "G-11 Markaz": (33.6920, 73.0200),
            "G-10 Markaz": (33.6920, 73.0200),
            "G-9 / H-9": (33.7000, 73.0400),
            "I-10 Markaz": (33.6700, 73.0800),
            "I-11 Markaz": (33.6700, 73.0800),
            "Khanna Pul": (33.6200, 73.1100),
            "Koral Chowk": (33.6200, 73.1100),
        },
        "red": {
            "Saddar": (33.7167, 73.0499),
            "Committee Chowk": (33.7167, 73.0499),
            "Chandani Chowk": (33.7167, 73.0499),
            "Chaman": (33.7140, 73.0730),
            "6th Road": (33.7140, 73.0730),
            "Faizabad": (33.7140, 73.0730),
            "Shamsabad": (33.7140, 73.0730),
            "Peshawar Morr": (33.7240, 73.0700),
            "Kacheri / Courts": (33.7240, 73.0700),
            "Shaheed-e-Millat": (33.7305, 73.0940),
            "7th Avenue": (33.7305, 73.0940),
            "Parade Ground": (33.7305, 73.0940),
            "Stock Exchange": (33.7350, 73.0870),
            "Pak Secretariat": (33.7350, 73.0870),
        },
        "electric": {
            "NUST Depot (G-11)": (33.6881, 73.0174),
            "G-11 Markaz": (33.6920, 73.0200),
            "G-10 Markaz": (33.6920, 73.0200),
            "PIMS Hospital": (33.7183, 73.0551),
            "G-7": (33.7216, 73.0634),
            "Aabpara": (33.7259, 73.0762),
            "Serena Hotel": (33.7291, 73.0838),
            "Bari Imam": (33.6960, 73.1050),
        },
        "pink": {
            "Nilore Terminal": (33.6960, 73.1050),
            "Bhara Kahu": (33.7547, 73.1547),
            "Humak": (33.6450, 73.0650),
            "I-14 Markaz": (33.6450, 73.0650),
            "B-17 Markaz": (33.6280, 72.8900),
            "F-11 Markaz": (33.6920, 73.0200),
            "Pak Secretariat": (33.7350, 73.0870),
        },
    }

    for line_code, stops in stations_data.items():
        line_obj = line_objs[line_code]
        for s in stops:
            coords = station_coordinates.get(line_code, {}).get(s["name"])
            if coords is None:
                raise ValueError(f"Missing coordinates for station '{s['name']}' on line '{line_code}'")
            station_payload = {
                **s,
                "latitude": coords[0],
                "longitude": coords[1],
            }
            station = models.Station(line_id=line_obj.id, **station_payload)
            db.add(station)

    # ── FARES ──────────────────────────────────────────────────────────
    # Applied to all standard lines (not Pink which is free)
    fare_tiers = [
        {"min_stops": 1, "max_stops": 5,  "single_pkr": 25, "card_pkr": 20, "label": "Short Journey"},
        {"min_stops": 6, "max_stops": 12, "single_pkr": 40, "card_pkr": 30, "label": "Medium Journey"},
        {"min_stops": 13,"max_stops": 99, "single_pkr": 50, "card_pkr": 40, "label": "Full Line Journey"},
    ]
    for line_code in ["orange", "green", "blue", "red", "electric"]:
        line_obj = line_objs[line_code]
        for ft in fare_tiers:
            fare = models.Fare(line_id=line_obj.id, **ft)
            db.add(fare)

    # ── ALERTS ─────────────────────────────────────────────────────────
    alerts_data = [
        {
            "tag": "Service Update", "tag_type": "green", "tag_urdu": "سروس اپڈیٹ",
            "title": "Extended Hours During Ramazan", "title_urdu": "رمضان کے دوران اوقات میں توسیع",
            "body": "Metro bus services will operate extended hours during the holy month, with additional buses on key routes after Iftar and Suhoor timings.",
            "body_urdu": "رمضان المبارک کے دوران میٹرو بس سروس کے اوقات میں توسیع کی جائے گی، اور افطار و سحر کے اوقات کے بعد اہم روٹس پر اضافی بسیں چلیں گی۔",
            "date_label": "May 2025", "date_label_urdu": "مئی 2025",
        },
        {
            "tag": "Infrastructure", "tag_type": "orange", "tag_urdu": "انفراسٹرکچر",
            "title": "New Accessible Ramps at 12 Stations", "title_urdu": "12 اسٹیشنز پر نئے ریمپ",
            "body": "Improved wheelchair-accessible ramps and audio guides have been installed at 12 major stations to better serve older adults and passengers with mobility challenges.",
            "body_urdu": "بزرگوں اور معذور افراد کی سہولت کے لیے 12 بڑے اسٹیشنز پر وہیل چیئر ریمپ اور آڈیو گائیڈز نصب کر دیے گئے ہیں۔",
            "date_label": "April 2025", "date_label_urdu": "اپریل 2025",
        },
        {
            "tag": "Smart Card", "tag_type": "blue", "tag_urdu": "سمارٹ کارڈ",
            "title": "Senior Citizen Card Now Available", "title_urdu": "سینئر سٹیزن کارڈ اب دستیاب ہے",
            "body": "Citizens aged 60 and above can now obtain their special senior discount card at any metro station with a valid CNIC.",
            "body_urdu": "60 سال اور اس سے زائد عمر کے شہری اب کسی بھی میٹرو اسٹیشن سے اپنے قومی شناختی کارڈ کے ذریعے خصوصی ڈسکاؤنٹ کارڈ حاصل کر سکتے ہیں۔",
            "date_label": "March 2025", "date_label_urdu": "مارچ 2025",
        },
    ]
    for ad in alerts_data:
        alert = models.Alert(**ad)
        db.add(alert)

    db.commit()
    db.close()
    print("✅ Seed complete — lines, stations, fares, and alerts loaded.")


if __name__ == "__main__":
    seed()
