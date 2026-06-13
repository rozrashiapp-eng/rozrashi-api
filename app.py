from flask import Flask, jsonify, render_template
from flask_cors import CORS
from datetime import date
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)
CORS(app)

# ════════════════════════════════════════
#  FIREBASE INIT via Environment Variables
# ════════════════════════════════════════

private_key = os.environ.get("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n")

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "private_key": private_key,
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "token_uri": "https://oauth2.googleapis.com/token",
})

firebase_admin.initialize_app(cred)
db = firestore.client()

# ════════════════════════════════════════
#  RASHI METADATA
# ════════════════════════════════════════

RASHI_META = [
    {"id": 1,  "name": "मेष",      "english": "Aries",       "symbol": "♈"},
    {"id": 2,  "name": "वृषभ",    "english": "Taurus",      "symbol": "♉"},
    {"id": 3,  "name": "मिथुन",   "english": "Gemini",      "symbol": "♊"},
    {"id": 4,  "name": "कर्क",    "english": "Cancer",      "symbol": "♋"},
    {"id": 5,  "name": "सिंह",    "english": "Leo",         "symbol": "♌"},
    {"id": 6,  "name": "कन्या",   "english": "Virgo",       "symbol": "♍"},
    {"id": 7,  "name": "तुला",    "english": "Libra",       "symbol": "♎"},
    {"id": 8,  "name": "वृश्चिक", "english": "Scorpio",     "symbol": "♏"},
    {"id": 9,  "name": "धनु",     "english": "Sagittarius", "symbol": "♐"},
    {"id": 10, "name": "मकर",     "english": "Capricorn",   "symbol": "♑"},
    {"id": 11, "name": "कुंभ",    "english": "Aquarius",    "symbol": "♒"},
    {"id": 12, "name": "मीन",     "english": "Pisces",      "symbol": "♓"},
]

# ════════════════════════════════════════
#  STATUS DATA
# ════════════════════════════════════════

STATUS_DATA = {
    "good_morning": [
        "सुप्रभात! आपका दिन मंगलमय हो 🌞",
        "हर सुबह एक नई शुरुआत है — इसे बर्बाद मत करो 💫",
        "खुश रहो, मुस्कुराते रहो, जीवन बहुत खूबसूरत है 😊",
        "उठो, जागो और अपने सपनों की ओर बढ़ो 🌅",
        "आज का दिन सिर्फ तुम्हारा है — इसे खास बनाओ ✨",
    ],
    "motivational": [
        "सफलता मेहनत से मिलती है, किस्मत से नहीं 💪",
        "हार मत मानो, कोशिश जारी रखो — मंजिल दूर नहीं 🔥",
        "खुद पर विश्वास रखो — तुम जो सोचते हो वो बन सकते हो ✨",
        "हर दिन एक नया मौका है — इसे गंवाओ मत 🌟",
        "मेहनत कभी बेकार नहीं जाती — फल जरूर मिलता है 💯",
    ],
    "motivation": [
        "सफलता मेहनत से मिलती है 💪",
        "हार मत मानो, कोशिश जारी रखो 🔥",
        "खुद पर विश्वास रखो ✨",
    ],
    "love": [
        "प्यार में सब कुछ खूबसूरत लगता है ❤️",
        "तुम्हारी मुस्कान मेरी दुनिया है 😍",
        "दिल से दिल की बात होती है 💕",
        "प्यार वो नहीं जो दिखाया जाए, प्यार वो है जो महसूस किया जाए 🌹",
        "तेरे बिना हर लम्हा अधूरा लगता है 💞",
    ],
    "attitude": [
        "अपना काम बोलता है, हम नहीं 😎",
        "जो मेरी परवाह करे, उसकी करता हूँ 👑",
        "हम वो हैं जो दिखते हैं — नकली नहीं 🔥",
        "तेवर ऐसे कि दुश्मन भी सलाम करे 😤",
        "अकेले चलना सीखो — भीड़ तो बाद में आती है 🦁",
    ],
    "sad": [
        "वक्त सब ठीक कर देता है — बस थोड़ा सब्र रखो 🌧️",
        "दर्द भी एक एहसास है — जो जीना सिखाता है 😔",
        "कभी कभी चुप रहना ही बेहतर होता है 💭",
        "टूटे हुए दिल भी एक दिन जुड़ जाते हैं 🖤",
        "रात कितनी भी काली हो, सुबह जरूर आती है 🌙",
    ],
}

# ════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════

@app.route('/app')
def app_ui():
    return render_template('index.html')


@app.route('/rashifal')
def get_all_rashifal():
    """Return all 12 rashis with today's horoscope from Firestore."""
    today_day = date.today().day  # 1-30/31
    day_index = min(today_day, 30)  # cap at 30

    result = []
    for meta in RASHI_META:
        rashi_name = meta["name"]
        try:
            doc = db.collection("rashifal") \
                    .document(rashi_name) \
                    .collection("days") \
                    .document(str(day_index)) \
                    .get()

            if doc.exists:
                day_data = doc.to_dict()
            else:
                day_data = {
                    "message": "आज का राशिफल जल्द उपलब्ध होगा।",
                    "lucky_number": 1,
                    "lucky_color": "सफेद",
                    "lucky_time": "सुबह 8-10 बजे",
                    "tip": "आज सकारात्मक रहें।"
                }
        except Exception:
            day_data = {
                "message": "डेटा लोड नहीं हो सका।",
                "lucky_number": 1,
                "lucky_color": "सफेद",
                "lucky_time": "सुबह 8-10 बजे",
                "tip": "बाद में पुनः प्रयास करें।"
            }

        result.append({
            "id": meta["id"],
            "name": rashi_name,
            "english": meta["english"],
            "symbol": meta["symbol"],
            **day_data
        })

    return jsonify({"data": result})


@app.route('/rashifal/<int:rashi_id>')
def get_rashifal_by_id(rashi_id):
    """Return single rashi detail with today's horoscope."""
    today_day = date.today().day
    day_index = min(today_day, 30)

    meta = next((r for r in RASHI_META if r["id"] == rashi_id), None)
    if not meta:
        return jsonify({"error": "Rashi not found"}), 404

    rashi_name = meta["name"]
    try:
        doc = db.collection("rashifal") \
                .document(rashi_name) \
                .collection("days") \
                .document(str(day_index)) \
                .get()

        if doc.exists:
            day_data = doc.to_dict()
        else:
            day_data = {
                "message": "आज का राशिफल जल्द उपलब्ध होगा।",
                "lucky_number": 1,
                "lucky_color": "सफेद",
                "lucky_time": "सुबह 8-10 बजे",
                "tip": "आज सकारात्मक रहें।"
            }
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"data": {
        "id": meta["id"],
        "name": rashi_name,
        "english": meta["english"],
        "symbol": meta["symbol"],
        **day_data
    }})


@app.route('/status/<category>')
def get_status_by_category(category):
    data = STATUS_DATA.get(category, [])
    return jsonify({"data": data})


# ════════════════════════════════════════
#  RUN
# ════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)