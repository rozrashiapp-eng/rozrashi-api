from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# ✅ SAMPLE RASHIFAL DATA (same structure your JS expects)
rashifal_data = [
    {"id": 1, "name": "मेष", "english": "Aries", "symbol": "♈",
     "message": "आज का दिन आपके लिए बहुत शुभ है। नए कार्य की शुरुआत करें।",
     "lucky_number": 3, "lucky_color": "लाल"},

    {"id": 2, "name": "वृषभ", "english": "Taurus", "symbol": "♉",
     "message": "धैर्य रखें। आर्थिक मामलों में सावधानी रखें।",
     "lucky_number": 6, "lucky_color": "नीला"},

    {"id": 3, "name": "मिथुन", "english": "Gemini", "symbol": "♊",
     "message": "व्यापार में लाभ मिलेगा। परिवार में खुशी का माहौल रहेगा।",
     "lucky_number": 5, "lucky_color": "हरा"},

    {"id": 4, "name": "कर्क", "english": "Cancer", "symbol": "♋",
     "message": "आज भावनाओं पर नियंत्रण रखें। परिवार का साथ मिलेगा।",
     "lucky_number": 2, "lucky_color": "पीला"},

    {"id": 5, "name": "सिंह", "english": "Leo", "symbol": "♌",
     "message": "काम में सफलता मिलेगी। आत्मविश्वास बढ़ेगा।",
     "lucky_number": 1, "lucky_color": "नारंगी"},

    {"id": 6, "name": "कन्या", "english": "Virgo", "symbol": "♍",
     "message": "स्वास्थ्य का ध्यान रखें। कोई नया अवसर मिल सकता है।",
     "lucky_number": 5, "lucky_color": "हरा"},

    {"id": 7, "name": "तुला", "english": "Libra", "symbol": "♎",
     "message": "संबंधों में मधुरता आएगी। नया कार्य शुरू कर सकते हैं।",
     "lucky_number": 6, "lucky_color": "गुलाबी"},

    {"id": 8, "name": "वृश्चिक", "english": "Scorpio", "symbol": "♏",
     "message": "गुस्से पर नियंत्रण रखें। धन लाभ के योग हैं।",
     "lucky_number": 9, "lucky_color": "लाल"},

    {"id": 9, "name": "धनु", "english": "Sagittarius", "symbol": "♐",
     "message": "यात्रा के योग बन रहे हैं। अध्ययन में सफलता मिलेगी।",
     "lucky_number": 3, "lucky_color": "पीला"},

    {"id": 10, "name": "मकर", "english": "Capricorn", "symbol": "♑",
     "message": "मेहनत रंग लाएगी। करियर में प्रगति होगी।",
     "lucky_number": 8, "lucky_color": "काला"},

    {"id": 11, "name": "कुंभ", "english": "Aquarius", "symbol": "♒",
     "message": "नए अवसर मिलेंगे। मित्रों का सहयोग मिलेगा।",
     "lucky_number": 4, "lucky_color": "आसमानी"},

    {"id": 12, "name": "मीन", "english": "Pisces", "symbol": "♓",
     "message": "धैर्य रखें। प्रेम जीवन में सुख मिलेगा।",
     "lucky_number": 7, "lucky_color": "बैंगनी"}
]

# ✅ STATUS DATA
status_data = {
    "good_morning": [
        "सुप्रभात! आपका दिन मंगलमय हो 🌞",
        "हर सुबह एक नई शुरुआत है 💫",
        "खुश रहो और मुस्कुराते रहो 😊"
    ],
    "motivation": [
        "सफलता मेहनत से मिलती है 💪",
        "हार मत मानो, कोशिश जारी रखो 🔥",
        "खुद पर विश्वास रखो ✨"
    ],
    "motivational": [
        "हर दिन एक नया मौका है 🌟",
        "मेहनत कभी बेकार नहीं जाती 💯",
        "सपने वो नहीं जो नींद में आएं 🚀"
    ],
    "love": [
        "प्यार में सब कुछ खूबसूरत लगता है ❤️",
        "तुम्हारी मुस्कान मेरी दुनिया है 😍",
        "दिल से दिल की बात होती है 💕"
    ],
    "attitude": [
        "अपना काम बोलता है 😎",
        "हम वो हैं जो दिखते हैं 🔥",
        "जो मेरी परवाह करे, उसकी करता हूँ 👑"
    ],
    "sad": [
        "वक्त सब ठीक कर देता है 🌧️",
        "दर्द भी एक एहसास है 😔",
        "कभी कभी चुप रहना ही बेहतर होता है 💭"
    ]
}

# ✅ UI ROUTE
@app.route('/app')
def app_ui():
    return render_template('index.html')


# ✅ GET ALL RASHIFAL (THIS FIXES YOUR JS)
@app.route('/rashifal')
def get_all_rashifal():
    return jsonify({
        "data": rashifal_data
    })


# ✅ GET SINGLE RASHI
@app.route('/rashifal/<int:rashi_id>')
def get_rashifal_by_id(rashi_id):
    for rashi in rashifal_data:
        if rashi["id"] == rashi_id:
            return jsonify({"data": rashi})

    return jsonify({"error": "Not found"}), 404


# ✅ STATUS API
@app.route('/status/<category>')
def get_status_by_category(category):
    data = status_data.get(category, [])
    return jsonify({
        "data": data
    })


# ✅ RUN
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)