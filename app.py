from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from rashifal_data import get_rashifal_today, get_single_rashi_today
from chalisa_data import CHALISA_DATA
from mantra_data import MANTRA_DATA
from aarti_data import AARTI_DATA
from tithi_data import get_today_tithi
from stotra_data import STOTRA_DATA, get_all_stotras, get_stotra
from festivals_data import get_today_festival
from datetime import datetime, timedelta
import json as _json
import pytz
IST = pytz.timezone('Asia/Kolkata')
import os
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

# ===== DAY WISE CHALISA ROTATION =====
DAILY_CHALISA_ROTATION = {
    0: ["shiv", "parvati", "ganga", "narmada"],
    # Monday — Shiv family

    1: ["hanuman", "bajrang", "narsingh", "kartikeya", "ram"],
    # Tuesday — Hanuman/Mangal/Shakti

    2: ["ganesh", "saraswati", "krishna"],
    # Wednesday — Ganesh/Budh/Wisdom

    3: ["vishnu", "krishna", "guru", "vaishno"],
    # Thursday — Vishnu/Guru family

    4: ["durga", "laxmi", "kali", "santoshi",
        "vaishno", "saraswati", "radha", "sita"],
    # Friday — Devi/Shakti/Lakshmi

    5: ["shani", "bhairav", "kali", "yamraj"],
    # Saturday — Shani/Bhairav

    6: ["surya", "ram", "vishnu"]
    # Sunday — Surya/Ram
}


@app.route('/chalisa/today')
def get_today_chalisa():
    try:
        now      = datetime.now(IST)
        day      = now.weekday()          # 0=Mon ... 6=Sun
        week_no  = now.isocalendar()[1]   # week number of year

        rotation = DAILY_CHALISA_ROTATION[day]
        key      = rotation[week_no % len(rotation)]
        chalisa  = CHALISA_DATA.get(key)

        if not chalisa:
            return jsonify({
                "success": False,
                "message": "Chalisa not found"
            }), 404

        return jsonify({
            "success":   True,
            "day_index": day,
            "week":      week_no,
            "key":       key,
            "data":      chalisa
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route('/chalisa/all')
def get_all_chalisa():
    try:
        result = []
        for key, value in CHALISA_DATA.items():
            result.append({
                "key":     key,
                "name":    value.get("name", ""),
                "god":     value.get("god", ""),
                "day":     value.get("day", ""),
                "symbol":  value.get("symbol", ""),
                "benefit": value.get("benefit", "")
            })
        return jsonify({
            "success": True,
            "data":    result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route('/chalisa/<key>')
def get_single_chalisa(key):
    try:
        if key in CHALISA_DATA:
            return jsonify({
                "success": True,
                "key":     key,
                "data":    CHALISA_DATA[key]
            })
        return jsonify({
            "success": False,
            "message": "Chalisa not found"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# ═══════════════════════════════════════
# AARTI ROUTES
# ═══════════════════════════════════════

DAILY_AARTI = {
    0: "shiv",      # Monday
    1: "hanuman",   # Tuesday
    2: "ganesh",    # Wednesday
    3: "vishnu",    # Thursday
    4: "durga",     # Friday
    5: "shani",     # Saturday
    6: "surya",     # Sunday
}

@app.route('/aarti/today')
def get_today_aarti():
    day = datetime.now(IST).weekday()
    key = DAILY_AARTI[day]
    aarti = AARTI_DATA.get(key)
    return jsonify({
        "success": True,
        "day_index": day,
        "key": key,
        "data": aarti
    })

@app.route('/aarti/all')
def get_all_aartis():
    result = []
    for key, value in AARTI_DATA.items():
        result.append({
            "key": key,
            "name": value["name"],
            "god": value["god"],
            "day": value["day"],
            "symbol": value["symbol"],
            "benefit": value["benefit"],
            "verse_count": len(value["verses"])
        })
    return jsonify({"success": True, "data": result})

@app.route('/aarti/<name>')
def get_aarti(name):
    aarti = AARTI_DATA.get(name)
    if aarti:
        return jsonify({"success": True, "data": aarti})
    return jsonify({
        "success": False,
        "message": "Aarti not found"
    }), 404

# ═══════════════════════════════════════
# MANTRA ROUTES
# ═══════════════════════════════════════

DAYS_MAP = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday"
}

@app.route('/mantra/today')
def get_today_mantra():
    day = datetime.now(IST).weekday()
    key = DAYS_MAP[day]
    mantra = MANTRA_DATA.get(key)
    return jsonify({
        "success": True,
        "day_index": day,
        "key": key,
        "data": mantra
    })

@app.route('/mantra/all')
def get_all_mantras():
    result = []
    for key, value in MANTRA_DATA.items():
        result.append({
            "key": key,
            "day": value["day"],
            "god": value["god"],
            "symbol": value["symbol"],
            "benefit": value["benefit"],
            "mantra_count": len(value["mantras"])
        })
    return jsonify({"success": True, "data": result})

@app.route('/mantra/<day>')
def get_mantra(day):
    mantra = MANTRA_DATA.get(day)
    if mantra:
        return jsonify({"success": True, "data": mantra})
    return jsonify({
        "success": False,
        "message": "Mantra not found"
    }), 404

# ════════════════════════════════════════
#  STOTRA ROUTES
# ════════════════════════════════════════

@app.route('/stotra/all')
def get_all_stotras_route():
    return jsonify({
        "success": True,
        "data": get_all_stotras()
    })

@app.route('/stotra/<key>')
def get_stotra_route(key):
    stotra = get_stotra(key)
    if stotra:
        return jsonify({"success": True, "data": stotra})
    return jsonify({
        "success": False,
        "message": "Stotra not found"
    }), 404

@app.route('/status/daily')
def get_daily_status():
    from datetime import datetime

    # Combine all categories into one pool
    all_statuses = []
    for category, items in STATUS_DATA.items():
        all_statuses.extend(items)

    # Pick based on day of year (rotates automatically)
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(all_statuses)

    return jsonify({
        "success": True,
        "data": all_statuses[index],
        "total": len(all_statuses)
    })

# ═══════════════════════════════════════
# PANCHANG ROUTES
# ═══════════════════════════════════════

# Default location — Ujjain (traditional Panchang city)
DEFAULT_LAT = 23.1765
DEFAULT_LNG = 75.7885
DEFAULT_TZ  = 5.5

BASE_URL = "https://json.freeastrologyapi.com"

# ── Hindi translation tables ──────────────────────────────────────────────────

TITHI_NAMES = {
    "Pratipada": "प्रतिपदा", "Dwitiya": "द्वितीया", "Tritiya": "तृतीया",
    "Chaturthi": "चतुर्थी", "Panchami": "पंचमी", "Shashthi": "षष्ठी",
    "Saptami": "सप्तमी", "Ashtami": "अष्टमी", "Navami": "नवमी",
    "Dashami": "दशमी", "Ekadashi": "एकादशी", "Dwadashi": "द्वादशी",
    "Trayodashi": "त्रयोदशी", "Chaturdashi": "चतुर्दशी",
    "Purnima": "पूर्णिमा", "Amavasya": "अमावस्या", "Shashti": "षष्ठी",
    "Shukla": "शुक्ल", "Krishna": "कृष्ण",
    "Shahshthi": "षष्ठी", "Shashhthi": "षष्ठी",
}

NAKSHATRA_NAMES = {
    "Ashwini": "अश्विनी", "Bharani": "भरणी", "Krittika": "कृत्तिका",
    "Rohini": "रोहिणी", "Mrigashira": "मृगशिरा", "Ardra": "आर्द्रा",
    "Punarvasu": "पुनर्वसु", "Pushya": "पुष्य", "Ashlesha": "आश्लेषा",
    "Magha": "मघा", "Purva Phalguni": "पूर्व फाल्गुनी",
    "Uttara Phalguni": "उत्तर फाल्गुनी", "Hasta": "हस्त", "Chitra": "चित्रा",
    "Swati": "स्वाती", "Vishakha": "विशाखा", "Anuradha": "अनुराधा",
    "Jyeshtha": "ज्येष्ठा", "Mula": "मूल", "Purva Ashadha": "पूर्वाषाढ़ा",
    "Uttara Ashadha": "उत्तराषाढ़ा", "Shravana": "श्रवण",
    "Dhanishtha": "धनिष्ठा", "Shatabhisha": "शतभिषा",
    "Purva Bhadrapada": "पूर्व भाद्रपद", "Uttara Bhadrapada": "उत्तर भाद्रपद",
    "Revati": "रेवती",
}

NAKSHATRA_ALIASES = {
    "Poorvaabhadra":  "Purva Bhadrapada",
    "Uttarabhadra":   "Uttara Bhadrapada",
    "Poorvaphalguni": "Purva Phalguni",
    "Uttaraphalguni": "Uttara Phalguni",
    "Poorvashadha":   "Purva Ashadha",
    "Uttarashadha":   "Uttara Ashadha",
    "Mrigasira":      "Mrigashira",
    "Chitta":         "Chitra",
    "Swathi":         "Swati",
    "Visakha":        "Vishakha",
    "Poorvabhadra":   "Purva Bhadrapada",
    "Dhanistha":      "Dhanishtha",
    "Sravana":        "Shravana",
}

YOGA_NAMES = {
    "Vishkambha": "विष्कम्भ", "Priti": "प्रीति", "Ayushman": "आयुष्मान",
    "Saubhagya": "सौभाग्य", "Shobhana": "शोभन", "Atiganda": "अतिगण्ड",
    "Sukarma": "सुकर्मा", "Dhriti": "धृति", "Shula": "शूल",
    "Ganda": "गण्ड", "Vriddhi": "वृद्धि", "Dhruva": "ध्रुव",
    "Vyaghata": "व्याघात", "Harshana": "हर्षण", "Vajra": "वज्र",
    "Siddhi": "सिद्धि", "Vyatipata": "व्यतीपात", "Variyan": "वरीयान",
    "Parigha": "परिघ", "Shiva": "शिव", "Siddha": "सिद्ध",
    "Sadhya": "साध्य", "Shubha": "शुभ", "Brahma": "ब्रह्म",
    "Indra": "इन्द्र", "Vaidhriti": "वैधृति",
}

YOGA_ALIASES = {
    "Soubhaagya": "Saubhagya",
    "Sobhana":    "Shobhana",
    "Sukharma":   "Sukarma",
}

KARAN_NAMES = {
    "Bava": "बव", "Balava": "बालव", "Kaulava": "कौलव", "Taitila": "तैतिल",
    "Garaja": "गरज", "Vanija": "वणिज", "Vanij": "वणिज", "Vishti": "विष्टि",
    "Bhadra": "भद्रा", "Shakuni": "शकुनि", "Chatushpada": "चतुष्पाद",
    "Naga": "नाग", "Kimstughna": "किंस्तुघ्न",
    "Garija": "गरज", "Taitula": "तैतिल",
}

PAKSHA_NAMES = {
    "Shukla": "शुक्ल पक्ष",
    "Krishna": "कृष्ण पक्ष",
}

# ── In-memory daily cache (default Ujjain only) ───────────────────────────────
_panchang_cache = {"date_key": None, "payload": None}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_headers():
    api_key = os.environ.get('FREE_ASTRO_API_KEY')
    return {"Content-Type": "application/json", "x-api-key": api_key}, api_key


def _base_payload(now, lat, lng, tz):
    return {
        "year": now.year, "month": now.month, "date": now.day,
        "hours": now.hour, "minutes": now.minute, "seconds": 0,
        "latitude": lat, "longitude": lng, "timezone": tz,
        "config": {"observation_point": "topocentric", "ayanamsha": "lahiri"}
    }


def _call_endpoint(path, payload, headers, timeout=10):
    try:
        resp = requests.post(
            f"{BASE_URL}/{path}", json=payload,
            headers=headers, timeout=timeout
        )
        if resp.status_code != 200:
            return False, None, f"HTTP {resp.status_code}: {resp.text}"

        data = resp.json()

        unwrapped = data
        if isinstance(data, dict) and "output" in data:
            unwrapped = data["output"]

        if isinstance(unwrapped, dict) and "message" in unwrapped:
            return False, None, str(unwrapped["message"])

        if isinstance(unwrapped, str):
            lower = unwrapped.lower()
            if "deprecat" in lower or "limit" in lower or "error" in lower:
                return False, None, unwrapped

        return True, data, resp.text

    except Exception as e:
        return False, None, str(e)


def _unwrap(data):
    def _try_parse(x):
        if isinstance(x, dict):
            return {k: _try_parse(v) for k, v in x.items()}
        if not isinstance(x, str):
            return x

        s = x.strip()
        if not s:
            return x

        # Attempt 1: parse directly. This handles BOTH plain JSON
        # ({"a":1}) AND an already-quoted JSON-string-of-a-string
        # ("{\"a\":1}") — json.loads unescapes either correctly.
        try:
            parsed = _json.loads(s)
            if parsed != s:
                return _try_parse(parsed)
            return parsed
        except Exception:
            pass

        # Attempt 2 (fallback): string has escaped quotes but is
        # missing its own outer quotes (e.g. `{\"a\":1}` with no "" around it).
        try:
            unescaped = _json.loads('"' + s + '"')
            if isinstance(unescaped, str) and unescaped != s:
                return _try_parse(unescaped)
        except Exception:
            pass

        return x

    if isinstance(data, dict) and "output" in data:
        return _try_parse(data["output"])
    return _try_parse(data)


def _first_item(d):
    if not isinstance(d, dict):
        return {}
    if "name" in d:
        return d
    if "1" in d:
        item = d["1"]
        if isinstance(item, str):
            try:
                item = _json.loads(item)
            except Exception:
                return {}
        if isinstance(item, dict):
            return item
    if isinstance(d, list) and d:
        return d[0]
    return {}


def _dig(d, *keys, default=None):
    for k in keys:
        if isinstance(k, tuple):
            cur, ok = d, True
            for part in k:
                if isinstance(cur, dict) and part in cur:
                    cur = cur[part]
                else:
                    ok = False
                    break
            if ok and cur not in (None, ""):
                return cur
        else:
            if isinstance(d, dict) and k in d and d[k] not in (None, ""):
                return d[k]
    return default


def fetch_full_panchang(lat, lng, tz, now, debug_raw=False):
    headers, api_key = _get_headers()
    if not api_key:
        return None, {"success": False, "message": "FREE_ASTRO_API_KEY not set in environment"}

    payload  = _base_payload(now, lat, lng, tz)
    result   = {}
    raw_dump = {}

    endpoints = {
        "sun":       "getsunriseandset",
        "tithi":     "tithi-durations",
        "nakshatra": "nakshatra-durations",
        "yoga":      "yoga-durations",
        "karana":    "karana-durations",
        "weekday":   "vedicweekday",
        "lunar":     "lunarmonthinfo",
        "samvat":    "samvatinfo",
        "rahu":      "rahu-kalam",
    }

    endpoint_items = list(endpoints.items())
    errors = {}

    for i, (key, path) in enumerate(endpoint_items):
        ok, data, raw_text = _call_endpoint(path, payload, headers)
        raw_dump[key] = raw_text

        if ok:
            result[key] = _unwrap(data)
        else:
            result[key] = None
            errors[key] = raw_text

        if i < len(endpoint_items) - 1:
            time.sleep(1.1)

    all_failed = all(v is None for v in result.values())
    if all_failed:
        first_err = next(iter(errors.values()), "Unknown API error")
        hint = ""
        if "limit" in first_err.lower():
            hint = ("Free tier allows limited calls per day. "
                    "Wait until tomorrow or upgrade your plan.")
        return None, {
            "success": False,
            "message": f"API error: {first_err}",
            "hint": hint,
            "errors": errors if debug_raw else None,
        }

    translated = {}

    # Sunrise / Sunset
    sun = result.get("sun") or {}
    translated["sunrise"] = _dig(sun, "sun_rise_time", "sun_rise", "sunrise", default="--")
    translated["sunset"]  = _dig(sun, "sun_set_time",  "sun_set",  "sunset",  default="--")

    # Tithi
    tithi_item = _first_item(result.get("tithi") or {})
    tithi_name = _dig(tithi_item, "name", "tithi_name", default="")
    paksha     = _dig(tithi_item, "paksha", default="")
    tithi_hi   = TITHI_NAMES.get(tithi_name, tithi_name) or "--"
    paksha_hi  = PAKSHA_NAMES.get(paksha.capitalize() if paksha else "", paksha)
    translated["tithi"]      = f"{paksha_hi} {tithi_hi}".strip() or "--"
    translated["tithi_ends"] = _dig(tithi_item, "completion", "ends_at", "completes_at", default="")

    # Nakshatra
    nak      = result.get("nakshatra") or {}
    nak_name = _dig(nak, "name", "nakshatra_name", default="")
    nak_norm = NAKSHATRA_ALIASES.get(nak_name, nak_name)
    translated["nakshatra"]      = NAKSHATRA_NAMES.get(nak_norm, nak_name) or "--"
    translated["nakshatra_lord"] = _dig(nak, "lord", "nakshatra_lord", default="")
    translated["nakshatra_ends"] = _dig(nak, "ends_at", "completion", "completes_at", default="")

    # Yoga
    yoga_item = _first_item(result.get("yoga") or {})
    yoga_name = _dig(yoga_item, "name", "yoga_name", default="")
    yoga_norm = YOGA_ALIASES.get(yoga_name, yoga_name)
    translated["yoga"]      = YOGA_NAMES.get(yoga_norm, yoga_name) or "--"
    translated["yoga_ends"] = _dig(yoga_item, "completion", "ends_at", "completes_at", default="")

    # Karan
    karan_item = _first_item(result.get("karana") or {})
    karan_name = _dig(karan_item, "name", "karan_name", default="")
    translated["karan"] = KARAN_NAMES.get(karan_name, karan_name) or "--"

    # Rahu Kaal
    rahu    = result.get("rahu") or {}
    r_start = _dig(rahu, "starts_at", "start_time", "start", default="--")
    r_end   = _dig(rahu, "ends_at",   "end_time",   "end",   default="--")
    translated["rahu_kaal"] = f"{r_start} - {r_end}"

    # Lunar Month
    lunar = result.get("lunar") or {}
    translated["lunar_month"] = _dig(
        lunar,
        "lunar_month_full_name", "lunar_month_name", "name",
        default="--"
    )
    translated["adhika_maas"] = bool(_dig(lunar, "adhika", default=0))

    # Vikram Samvat
    samvat = result.get("samvat") or {}
    translated["vikram_samvat"] = str(_dig(
        samvat,
        "vikram_chaitradi_number",
        "vikram_chaitradi_name_number",
        "vikram_samvat",
        "vikram_samvat_year",
        default="--"
    ))
    translated["samvat_name"] = _dig(
        samvat,
        "vikram_chaitradi_year_name",
        "vikram_chairadi_year_name",
        default=""
    )

    # Weekday
    weekday = result.get("weekday") or {}
    translated["weekday"] = _dig(
        weekday,
        "vedic_weekday_name", "weekday_name", "name",
        default="--"
    )

    if debug_raw:
        translated["_raw_debug"] = raw_dump
        translated["_parsed_types"] = {
            k: {
                "type": type(v).__name__,
                "preview": (str(v)[:200] if v is not None else None)
            }
            for k, v in result.items()
        }

    return translated, None


@app.route('/panchang')
def get_panchang():
    """
    Query params:
      lat, lng, tz  — location (defaults to Ujjain)
      debug=1       — include raw API responses in output
      force=1       — bypass cache and call API fresh (use sparingly!)
    """
    try:
        lat   = float(request.args.get('lat', DEFAULT_LAT))
        lng   = float(request.args.get('lng', DEFAULT_LNG))
        tz    = float(request.args.get('tz',  DEFAULT_TZ))
        debug = request.args.get('debug', '') == '1'
        force = request.args.get('force', '') == '1'

        now        = datetime.now(IST)
        is_default = (lat == DEFAULT_LAT and lng == DEFAULT_LNG and tz == DEFAULT_TZ)
        today_key  = now.strftime("%Y-%m-%d")

        # Serve from cache if valid
        if is_default and not force and not debug and _panchang_cache["date_key"] == today_key:
            cached = dict(_panchang_cache["payload"])
            if debug:
                cached["cache_hit"] = True
            return jsonify(cached)

        translated, err = fetch_full_panchang(lat, lng, tz, now, debug_raw=debug)

        if err:
            # Serve stale cache rather than blank error
            if _panchang_cache["payload"]:
                stale = dict(_panchang_cache["payload"])
                stale["stale"]        = True
                stale["stale_reason"] = err.get("message", "API error")
                stale["hint"]         = err.get("hint", "")
                return jsonify(stale)
            return jsonify(err), 502

        if (translated.get("sunrise", "--") == "--"
                and translated.get("tithi", "--") in ("--", " --", "")):
            return jsonify({
                "success": False,
                "message": "Panchang data unavailable from provider",
                "debug":   translated.get("_raw_debug") if debug else None
            }), 502

        response_payload = {
            "success":  True,
            "date":     now.strftime("%d %B %Y"),
            "location": {"lat": lat, "lng": lng, "is_default": is_default},
            "data":     translated,
        }

        core_ok = all(
            translated.get(f, "--") not in ("--", "", " --")
            for f in ("tithi", "nakshatra", "yoga", "karan", "lunar_month", "vikram_samvat")
        ) and translated.get("rahu_kaal", "-- - --") != "-- - --"

        if is_default and not debug and core_ok:
            _panchang_cache["date_key"] = today_key
            _panchang_cache["payload"]  = response_payload
            print("Panchang cached ✅")
        elif is_default and not debug and not core_ok:
            print("⚠️ Incomplete panchang data — skipping cache update")

        return jsonify(response_payload)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ═══════════════════════════════════════
# KUNDALI ROUTES
# ═══════════════════════════════════════

_prokerala_token        = None
_prokerala_token_expiry = None

def get_prokerala_token():
    global _prokerala_token, _prokerala_token_expiry
    now = datetime.now(IST)
    if _prokerala_token and _prokerala_token_expiry and now < _prokerala_token_expiry:
        return _prokerala_token

    client_id     = os.environ.get('PROKERALA_CLIENT_ID')
    client_secret = os.environ.get('PROKERALA_CLIENT_SECRET')
    if not client_id or not client_secret:
        return None

    try:
        response = requests.post(
            "https://api.prokerala.com/token",
            data={
                "grant_type":    "client_credentials",
                "client_id":     client_id,
                "client_secret": client_secret
            },
            timeout=10
        )
        if response.status_code == 200:
            token_data = response.json()
            _prokerala_token        = token_data.get("access_token")
            _prokerala_token_expiry = now + timedelta(minutes=55)
            return _prokerala_token
        return None
    except Exception as e:
        print(f"Prokerala token error: {e}")
        return None


def get_coordinates_from_city(city_name):
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city_name + ", India", "format": "json", "limit": 1},
            headers={"User-Agent": "RozRashi/1.0"},
            timeout=5
        )
        if response.status_code == 200:
            results = response.json()
            if results:
                return {
                    "lat":          float(results[0]["lat"]),
                    "lng":          float(results[0]["lon"]),
                    "display_name": results[0]["display_name"]
                }
        return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None


@app.route('/kundali', methods=['POST'])
def get_kundali():
    try:
        data = request.get_json()
        name = data.get('name', 'जातक')
        dob  = data.get('dob')
        tob  = data.get('tob')
        city = data.get('city')
        lat  = data.get('lat')
        lng  = data.get('lng')

        if not dob or not tob or (not city and not lat):
            return jsonify({
                "success": False,
                "message": "कृपया जन्म तिथि, समय और स्थान भरें।"
            }), 400

        if city and not lat:
            coords = get_coordinates_from_city(city)
            if not coords:
                return jsonify({
                    "success": False,
                    "message": f"'{city}' शहर नहीं मिला। कृपया दूसरा नाम डालें।"
                }), 400
            lat = coords["lat"]
            lng = coords["lng"]

        date_parts   = dob.split('-')
        time_parts   = tob.split(':')
        year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
        datetime_str = f"{dob}T{tob}:00+05:30"

        token = get_prokerala_token()
        if not token:
            return jsonify({
                "success": False,
                "message": "कुंडली सेवा अभी उपलब्ध नहीं है।"
            }), 500

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json"
        }

        kundali_response = requests.get(
            "https://api.prokerala.com/v2/astrology/kundli",
            params={
                "ayanamsa":    1,
                "coordinates": f"{lat},{lng}",
                "datetime":    datetime_str,
                "chart_type":  "rasi",
                "chart_style": "north-indian",
                "format":      "svg"
            },
            headers=headers, timeout=15
        )

        planet_response = requests.get(
            "https://api.prokerala.com/v2/astrology/planet-position",
            params={
                "ayanamsa":    1,
                "coordinates": f"{lat},{lng}",
                "datetime":    datetime_str
            },
            headers=headers, timeout=15
        )

        kundali_data = kundali_response.json() if kundali_response.status_code == 200 else {}
        planet_data  = planet_response.json()  if planet_response.status_code == 200  else {}

        planet_hindi = {
            "Sun": "सूर्य ☀️", "Moon": "चंद्र 🌙", "Mars": "मंगल 🔴",
            "Mercury": "बुध 💚", "Jupiter": "गुरु 🟡", "Venus": "शुक्र ⚪",
            "Saturn": "शनि ⚫", "Rahu": "राहु 🌑", "Ketu": "केतु 🌒",
            "Ascendant": "लग्न ⬆️"
        }
        rashi_hindi = {
            "Aries": "मेष ♈", "Taurus": "वृषभ ♉", "Gemini": "मिथुन ♊",
            "Cancer": "कर्क ♋", "Leo": "सिंह ♌", "Virgo": "कन्या ♍",
            "Libra": "तुला ♎", "Scorpio": "वृश्चिक ♏", "Sagittarius": "धनु ♐",
            "Capricorn": "मकर ♑", "Aquarius": "कुंभ ♒", "Pisces": "मीन ♓"
        }

        planets_formatted = []
        for planet in planet_data.get("data", {}).get("planet_position", []):
            p_name  = planet.get("name", "")
            p_rashi = planet.get("rasi", {}).get("name", "")
            planets_formatted.append({
                "name":     planet_hindi.get(p_name, p_name),
                "rashi":    rashi_hindi.get(p_rashi, p_rashi),
                "degree":   round(planet.get("degree", 0), 2),
                "is_retro": planet.get("is_retrograde", False)
            })

        return jsonify({
            "success":     True,
            "name":        name,
            "dob":         f"{day:02d}/{month:02d}/{year}",
            "tob":         tob,
            "city":        city or f"{lat}, {lng}",
            "kundali_svg": kundali_data.get("data", {}).get("svg", ""),
            "planets":     planets_formatted,
            "lagna":       kundali_data.get("data", {}).get("ascendant", {})
        })

    except Exception as e:
        print(f"Kundali error: {e}")
        return jsonify({
            "success": False,
            "message": "कुंडली बनाने में समस्या आई। पुनः प्रयास करें।"
        }), 500


@app.route('/city-search')
def city_search():
    try:
        query = request.args.get('q', '')
        if len(query) < 2:
            return jsonify({"success": True, "data": []})

        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q":              query + ", India",
                "format":         "json",
                "limit":          5,
                "addressdetails": 1
            },
            headers={"User-Agent": "RozRashi/1.0"},
            timeout=5
        )
        if response.status_code == 200:
            cities = []
            for r in response.json():
                cities.append({
                    "name": r.get("display_name", "").split(",")[0].strip(),
                    "full": r.get("display_name", ""),
                    "lat":  float(r["lat"]),
                    "lng":  float(r["lon"])
                })
            return jsonify({"success": True, "data": cities})
        return jsonify({"success": True, "data": []})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# ════════════════════════════════════════
#  STATUS DATA
# ════════════════════════════════════════

STATUS_DATA = {
    "good_morning": [
        """🌅 हर सुबह ईश्वर का दिया हुआ
एक नया अवसर है।
उठो, प्रभु का नाम लो,
और दिन की शुरुआत शुभ करो। 🙏
सुप्रभात!""",

        """☀️ सूर्योदय के साथ उठकर
प्रभु का धन्यवाद करो।
जो मिला है वो उनकी कृपा है,
जो मिलेगा वो भी उनकी दया है। 🌸
सुप्रभात!""",

        """🌺 हर सुबह एक नई प्रार्थना लेकर आती है।
मन को शांत करो,
ईश्वर को याद करो,
दिन मंगलमय होगा। 🕉️
सुप्रभात!""",

        """🪔 जब सुबह आँखें खुलें तो
सबसे पहले ईश्वर का नाम लो।
राम कहो, कृष्ण कहो, शिव कहो —
नाम में ही जीवन की शक्ति है। 🙏
सुप्रभात!""",

        """🌻 प्रभु की कृपा से
आज का दिन मंगलमय हो।
घर में सुख-शांति रहे,
मन में भक्ति बनी रहे। 🌟
सुप्रभात!""",

        """🌸 ब्रह्म मुहूर्त में उठकर
ईश्वर का ध्यान करने वाले पर
माँ लक्ष्मी और माँ सरस्वती
दोनों की कृपा बनी रहती है। 🙏
सुप्रभात!""",

        """☀️ राम नाम की शक्ति ऐसी है
कि हर मुश्किल आसान हो जाती है।
आज राम का नाम लेकर उठो
और देखो कैसे दिन बदल जाता है। 🏹
सुप्रभात!""",

        """🌺 हनुमान जी की कृपा से
हर संकट दूर होता है।
मंगलवार हो या कोई भी दिन —
बजरंगबली का नाम लो। 🙏
सुप्रभात!""",

        """🕉️ ओम नमः शिवाय का जाप करते हुए
दिन की शुरुआत करो।
महादेव की कृपा से
हर काम सफल होगा। 🔱
सुप्रभात!""",

        """🌟 माँ दुर्गा की कृपा से
आज का दिन शुभ हो।
जय माता दी के साथ
नई सुबह का स्वागत करो। 🌺
सुप्रभात!""",

        """🪷 भगवान विष्णु की कृपा हो,
माँ लक्ष्मी का आशीर्वाद हो।
घर में धन-धान्य आए,
परिवार में सुख-शांति रहे। 🙏
सुप्रभात!""",

        """🌅 गणेश जी का आशीर्वाद लेकर
दिन की शुरुआत करो।
विघ्नों का नाश होगा,
हर काम सफल होगा। 🐘
सुप्रभात!""",
    ],

    "bhakti_quotes": [
        """🕉️ जो राम का नाम जपता है,
उसे किसी का डर नहीं।
राम नाम की डोर थामो,
जीवन सफल हो जाएगा। 🙏""",

        """🔱 शिव का ध्यान करने वाले को
न रोग सताता है, न शत्रु।
हर हर महादेव बोलो,
और देखो चमत्कार होता है। ✨""",

        """🌺 माँ दुर्गा की शक्ति असीम है।
जो उन्हें पुकारता है,
वो कभी हारता नहीं।
जय माता दी! 🙏""",

        """🐘 गणेश जी कहते हैं —
पहले धर्म का काम करो,
बाकी सब मैं संभालूँगा।
जय श्री गणेश! 🌟""",

        """🪷 कृष्ण कहते हैं गीता में —
फल की चिंता मत करो,
कर्म करते रहो।
जो होगा अच्छा ही होगा। 🕉️""",

        """🏹 राम ने सिखाया कि
सत्य के रास्ते पर चलो,
चाहे मुश्किलें आएं।
सत्य की हमेशा जीत होती है। 🙏""",

        """🙏 हनुमान जी का आशीर्वाद है —
जो राम का नाम लेता है,
उसकी रक्षा मैं करता हूँ।
राम राम, जय बजरंगबली! 🔥""",

        """🌸 ईश्वर हर जगह है,
हर इंसान में,
हर प्राणी में।
इसीलिए सबसे प्रेम करो। 💕""",

        """🪔 दीपक जलाने से
सिर्फ घर नहीं,
मन का अंधेरा भी दूर होता है।
ईश्वर का नाम ही असली दीपक है। ✨""",

        """🕉️ जीवन में तीन चीजें जरूरी हैं —
ईश्वर पर विश्वास,
माता-पिता का आशीर्वाद,
और मन की शुद्धता। 🙏""",

        """🌺 भक्ति वो शक्ति है
जो असंभव को भी संभव बना देती है।
प्रेम से प्रभु को पुकारो,
वो जरूर सुनते हैं। 💫""",

        """🔱 महादेव कहते हैं —
मुझे मंदिर में मत ढूंढो,
मुझे अपने मन में ढूंढो।
मैं वहीं हूँ जहाँ तुम हो। 🙏""",

        """🐘 गणेश जी की कृपा से
हर बाधा दूर होती है।
नई शुरुआत से पहले
गणेश जी को याद करो। 🌟""",

        """🪷 कृष्ण की बाँसुरी की धुन में
जीवन का सत्य छुपा है।
प्रेम करो, भजन करो,
यही मोक्ष का मार्ग है। 💕""",

        """🙏 माँ लक्ष्मी वहाँ रहती हैं
जहाँ परिश्रम है,
जहाँ पवित्रता है,
जहाँ ईश्वर का आशीर्वाद है। 🌟""",
    ],
}
# ════════════════════════════════════════
#  NOTIFICATION DATA
# ════════════════════════════════════════

HINDI_DAYS = {
    0: "सोमवार", 1: "मंगलवार", 2: "बुधवार", 3: "गुरुवार",
    4: "शुक्रवार", 5: "शनिवार", 6: "रविवार"
}

CHALISA_INFO = {
    0: {"name": "शिव चालीसा",     "god": "भगवान शिव",   "emoji": "🔱"},
    1: {"name": "हनुमान चालीसा",  "god": "हनुमान जी",   "emoji": "🙏"},
    2: {"name": "गणेश चालीसा",    "god": "गणेश जी",     "emoji": "🐘"},
    3: {"name": "लक्ष्मी चालीसा", "god": "माँ लक्ष्मी", "emoji": "🪷"},
    4: {"name": "दुर्गा चालीसा",  "god": "माँ दुर्गा",  "emoji": "🌺"},
    5: {"name": "शनि चालीसा",     "god": "शनि देव",     "emoji": "⚫"},
    6: {"name": "सूर्य चालीसा",   "god": "सूर्य देव",   "emoji": "☀️"},
}

AARTI_INFO = {
    0: {"name": "शिव जी की आरती",    "emoji": "🔱"},
    1: {"name": "हनुमान जी की आरती", "emoji": "🙏"},
    2: {"name": "गणेश जी की आरती",   "emoji": "🐘"},
    3: {"name": "विष्णु जी की आरती", "emoji": "🪷"},
    4: {"name": "दुर्गा जी की आरती", "emoji": "🌺"},
    5: {"name": "शनि जी की आरती",    "emoji": "⚫"},
    6: {"name": "सूर्य जी की आरती",  "emoji": "☀️"},
}

# ════════════════════════════════════════
#  NOTIFICATION FUNCTIONS
# ════════════════════════════════════════

def send_onesignal_notification(title, message):
    api_key = os.environ.get('ONESIGNAL_API_KEY')
    app_id  = os.environ.get('ONESIGNAL_APP_ID')
    if not api_key or not app_id:
        print("❌ OneSignal credentials missing")
        return None

    headers = {
        "Authorization": f"Basic {api_key}",
        "Content-Type":  "application/json"
    }
    payload = {
        "app_id":            app_id,
        "included_segments": ["All"],
        "headings":          {"en": title, "hi": title},
        "contents":          {"en": message, "hi": message},
        "small_icon":        "ic_stat_onesignal_default"
    }
    try:
        response = requests.post(
            "https://onesignal.com/api/v1/notifications",
            json=payload, headers=headers
        )
        print(f"Notification sent: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"Notification error: {e}")
        return None


def send_morning_notification():
    """6:00 AM — tithi > festival > default rashifal"""
    tithi = get_today_tithi()
    if tithi:
        send_onesignal_notification(
            tithi["notification_title"],
            tithi["notification_msg"]
        )
        return
    festival = get_today_festival()
    if festival:
        send_onesignal_notification(
            festival["notification_title"],
            festival["notification_msg"]
        )
        return
    send_onesignal_notification(
        "🌅 शुभ प्रभात! आज का राशिफल तैयार है",
        "आज का दिन कैसा रहेगा? अपनी राशि चेक करें "
        "और दिन की शुभ शुरुआत करें 🙏"
    )


def send_aarti_notification():
    """8:00 AM — Aarti reminder"""
    day   = datetime.now(IST).weekday()
    aarti = AARTI_INFO[day]
    send_onesignal_notification(
        f"🪔 संध्या आरती — {aarti['name']}",
        f"आज की {aarti['name']} करें और ईश्वर का आभार व्यक्त करें {aarti['emoji']} 🙏"
    )


def send_chalisa_notification():
    """7:00 PM — Chalisa reminder"""
    day       = datetime.now(IST).weekday()
    hindi_day = HINDI_DAYS[day]
    chalisa   = CHALISA_INFO[day]
    send_onesignal_notification(
        f"{chalisa['emoji']} आज की चालीसा — {chalisa['name']}",
        f"आज {hindi_day} है। {chalisa['god']} की {chalisa['name']} पढ़ें और मंत्र जपें। "
        f"मन को शांति और आशीर्वाद मिलेगा 🕉️"
    )


# ════════════════════════════════════════
#  PANCHANG CACHE WARMER
# ════════════════════════════════════════

def warm_panchang_cache():
    """Pre-fills the panchang cache. Validates data before caching."""
    try:
        now       = datetime.now(IST)
        today_key = now.strftime("%Y-%m-%d")
        if _panchang_cache["date_key"] == today_key:
            print("Panchang cache already warm ✅")
            return

        print("Warming panchang cache...")
        translated, err = fetch_full_panchang(
            DEFAULT_LAT, DEFAULT_LNG, DEFAULT_TZ, now, debug_raw=False
        )
        if err:
            print(f"Panchang cache warm failed: {err}")
            return

        # ✅ Validate before caching — must have both tithi AND nakshatra, not just sunrise
        core_ok = all(
            translated.get(f, "--") not in ("--", "", " --")
            for f in ("tithi", "nakshatra", "yoga", "karan", "lunar_month", "vikram_samvat")
        ) and translated.get("rahu_kaal", "-- - --") != "-- - --"

        if not core_ok:
            print("⚠️ Panchang data incomplete — not caching bad data")
            return

        _panchang_cache["date_key"] = today_key
        _panchang_cache["payload"]  = {
            "success":  True,
            "date":     now.strftime("%d %B %Y"),
            "location": {"lat": DEFAULT_LAT, "lng": DEFAULT_LNG, "is_default": True},
            "data":     translated,
        }
        print("Panchang cache warmed ✅")
    except Exception as e:
        print(f"Panchang warm error: {e}")


# ════════════════════════════════════════
#  SCHEDULER  (single definition)
# ════════════════════════════════════════

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=IST)
    scheduler.add_job(send_morning_notification,  'cron', hour=6,  minute=0)
    scheduler.add_job(send_aarti_notification,    'cron', hour=8,  minute=0)
    scheduler.add_job(send_chalisa_notification,  'cron', hour=19, minute=0)
    scheduler.add_job(warm_panchang_cache,        'cron', hour=5,  minute=30)
    scheduler.start()
    print("Scheduler started ✅")


# ════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════

@app.route('/')
def home():
    return jsonify({"message": "RozRashi API is running!", "version": "2.0"})

@app.route('/app')
def app_ui():
    return render_template('index.html')

@app.route('/privacy')
def privacy_policy():
    return render_template('privacy.html')

@app.route('/rashifal')
def get_all_rashifal():
    return jsonify({"success": True, "data": get_rashifal_today()})

@app.route('/rashifal/<int:rashi_id>')
def get_rashifal_by_id(rashi_id):
    rashi = get_single_rashi_today(rashi_id)
    if rashi:
        return jsonify({"success": True, "data": rashi})
    return jsonify({"success": False, "message": "Rashi not found"}), 404

# NOTE: static route defined BEFORE dynamic route to avoid Flask ambiguity
@app.route('/status/categories/all')
def get_categories():
    return jsonify({"success": True, "categories": list(STATUS_DATA.keys())})

@app.route('/status/<category>')
def get_status_by_category(category):
    data = STATUS_DATA.get(category)
    if data:
        return jsonify({"success": True, "category": category, "data": data})
    return jsonify({"success": False, "message": "Category not found"}), 404

@app.route('/today/special')
def get_today_special():
    tithi = get_today_tithi()
    if tithi:
        return jsonify({"success": True, "type": "tithi", "data": tithi})
    festival = get_today_festival()
    if festival:
        return jsonify({"success": True, "type": "festival", "data": festival})
    return jsonify({"success": False, "message": "No special event today"})

# ════════════════════════════════════════
#  NOTIFICATION TEST ROUTES
# ════════════════════════════════════════

@app.route('/notify/morning')
def trigger_morning():
    send_morning_notification()
    return jsonify({"status": "Morning sent ✅"})

@app.route('/notify/aarti')
def trigger_aarti():
    send_aarti_notification()
    return jsonify({"status": "Aarti sent ✅"})

@app.route('/notify/chalisa')
def trigger_chalisa():
    send_chalisa_notification()
    return jsonify({"status": "Chalisa sent ✅"})

# ════════════════════════════════════════
#  RUN  (single block)
# ════════════════════════════════════════

# ✅ Start scheduler outside __main__ so it runs on Render/Gunicorn too
if not os.environ.get('WERKZEUG_RUN_MAIN'):
    start_scheduler()
    warm_panchang_cache()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)