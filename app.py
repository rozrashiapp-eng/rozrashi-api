from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

# ===== RASHIFAL DATA =====
rashifal_data = [
    {
        "id": 1,
        "name": "मेष",
        "english": "Aries",
        "symbol": "♈",
        "lucky_number": 3,
        "lucky_color": "लाल",
        "message": "आज का दिन आपके लिए बहुत शुभ है। नए कार्यों की शुरुआत के लिए यह दिन उत्तम है। परिवार के साथ समय बिताएं।"
    },
    {
        "id": 2,
        "name": "वृषभ",
        "english": "Taurus",
        "symbol": "♉",
        "lucky_number": 6,
        "lucky_color": "सफेद",
        "message": "आर्थिक मामलों में सावधानी रखें। कोई पुराना मित्र आज मिल सकता है। स्वास्थ्य का ध्यान रखें।"
    },
    {
        "id": 3,
        "name": "मिथुन",
        "english": "Gemini",
        "symbol": "♊",
        "lucky_number": 5,
        "lucky_color": "हरा",
        "message": "व्यापार में लाभ के योग हैं। परिवार में खुशी का माहौल रहेगा। किसी बड़े का आशीर्वाद मिलेगा।"
    },
    {
        "id": 4,
        "name": "कर्क",
        "english": "Cancer",
        "symbol": "♋",
        "lucky_number": 2,
        "lucky_color": "पीला",
        "message": "आज भावनात्मक रूप से मजबूत रहें। प्रेम संबंधों में मधुरता आएगी। धैर्य से काम लें।"
    },
    {
        "id": 5,
        "name": "सिंह",
        "english": "Leo",
        "symbol": "♌",
        "lucky_number": 1,
        "lucky_color": "नारंगी",
        "message": "आज आपका आत्मविश्वास चरम पर रहेगा। नौकरी में तरक्की के संकेत हैं। शाम को परिवार के साथ बाहर जाएं।"
    },
    {
        "id": 6,
        "name": "कन्या",
        "english": "Virgo",
        "symbol": "♍",
        "lucky_number": 5,
        "lucky_color": "नीला",
        "message": "बौद्धिक कार्यों में सफलता मिलेगी। स्वास्थ्य पर ध्यान दें। नए निवेश से बचें।"
    },
    {
        "id": 7,
        "name": "तुला",
        "english": "Libra",
        "symbol": "♎",
        "lucky_number": 6,
        "lucky_color": "गुलाबी",
        "message": "संबंधों में मधुरता बनाए रखें। आज कोई महत्वपूर्ण निर्णय लेने से बचें। मन शांत रहेगा।"
    },
    {
        "id": 8,
        "name": "वृश्चिक",
        "english": "Scorpio",
        "symbol": "♏",
        "lucky_number": 9,
        "lucky_color": "लाल",
        "message": "गुप्त शत्रुओं से सावधान रहें। धन लाभ के योग बन रहे हैं। परिश्रम का फल मिलेगा।"
    },
    {
        "id": 9,
        "name": "धनु",
        "english": "Sagittarius",
        "symbol": "♐",
        "lucky_number": 3,
        "lucky_color": "पीला",
        "message": "यात्रा के योग हैं। उच्च शिक्षा में सफलता मिलेगी। आज का दिन उत्साह से भरा रहेगा।"
    },
    {
        "id": 10,
        "name": "मकर",
        "english": "Capricorn",
        "symbol": "♑",
        "lucky_number": 8,
        "lucky_color": "काला",
        "message": "कार्यक्षेत्र में मेहनत रंग लाएगी। वरिष्ठों का सहयोग मिलेगा। आर्थिक स्थिति मजबूत होगी।"
    },
    {
        "id": 11,
        "name": "कुंभ",
        "english": "Aquarius",
        "symbol": "♒",
        "lucky_number": 4,
        "lucky_color": "आसमानी",
        "message": "मित्रों का साथ मिलेगा। सामाजिक कार्यों में भागीदारी फायदेमंद रहेगी। नई योजना बनाएं।"
    },
    {
        "id": 12,
        "name": "मीन",
        "english": "Pisces",
        "symbol": "♓",
        "lucky_number": 7,
        "lucky_color": "बैंगनी",
        "message": "आध्यात्मिक कार्यों में मन लगेगा। कल्पनाशीलता से काम लें। प्रेम जीवन में मधुरता आएगी।"
    }
]

# ===== STATUS DATA =====
status_data = {
    "good_morning": [
        "🌅 हर सुबह एक नया मौका है, खुद को बेहतर बनाने का। सुप्रभात! 🌸",
        "☀️ उठो, जागो और अपने सपनों की तरफ बढ़ो। सुप्रभात! 💪",
        "🌺 सुबह की पहली किरण के साथ, नई उम्मीदें लेकर आती है। सुप्रभात! ✨",
        "🌻 जो बीत गया उसे भूलो, जो आने वाला है उसका स्वागत करो। सुप्रभात! 🙏",
        "💐 मुस्कुराओ, क्योंकि आज का दिन सिर्फ तुम्हारा है। सुप्रभात! 😊"
    ],
    "motivational": [
        "💪 मंजिल उन्हीं को मिलती है, जिनके सपनों में जान होती है।",
        "🔥 हार मत मानो, हर मुश्किल के बाद कामयाबी जरूर आती है।",
        "⭐ खुद पर भरोसा रखो, दुनिया खुद-ब-खुद रास्ता दे देती है।",
        "🚀 सफलता एक दिन में नहीं मिलती, लेकिन हर दिन की मेहनत जरूर मिलाती है।",
        "🌟 जो गिरकर उठना जानते हैं, वही असली योद्धा होते हैं।"
    ],
    "love": [
        "❤️ तुम्हारे बिना यह जिंदगी अधूरी सी लगती है।",
        "💕 प्यार वो नहीं जो दिखता है, प्यार वो है जो महसूस होता है।",
        "🌹 तुम मेरी जिंदगी की वो खुशबू हो, जो हमेशा मेरे साथ रहती है।",
        "💑 हर पल तुम्हारे साथ बिताना चाहता हूं, यही मेरी दुआ है।",
        "🥰 तुम्हारी एक मुस्कान मेरा पूरा दिन बना देती है।"
    ],
    "attitude": [
        "😎 मैं वो नहीं जो दिखता है, मैं वो हूं जो महसूस होता है।",
        "👑 अपनी औकात में रहो, मेरी औकात तुम्हारी सोच से बड़ी है।",
        "🦁 शेर की एक दहाड़ काफी है, बार-बार बोलना कुत्तों का काम है।",
        "💯 नकल करने वाले हमेशा पीछे रहते हैं, असली हमेशा आगे।",
        "🔥 मुझे कम मत समझो, मैं वो आग हूं जो चुप रहकर जलती है।"
    ],
    "sad": [
        "😔 कभी-कभी खामोशी ही सबसे बड़ा जवाब होती है।",
        "💔 दिल टूटता है तो दर्द होता है, लेकिन टूटा हुआ दिल भी धड़कता है।",
        "🌧️ कुछ दर्द ऐसे होते हैं जो आंखों से नहीं, दिल से रोते हैं।",
        "😞 जिनसे उम्मीद होती है, वही सबसे ज्यादा तकलीफ देते हैं।",
        "🥀 वक्त सब ठीक कर देता है, बस थोड़ा सब्र चाहिए।"
    ]
}

# ===== API ROUTES =====

# Home route - just to check API is working
@app.route('/')
def home():
    return jsonify({
        "message": "RozRashi API is running!",
        "version": "1.0"
    })

# Get all rashifal
@app.route('/rashifal')
def get_all_rashifal():
    return jsonify({
        "success": True,
        "data": rashifal_data
    })

# Get single rashi by id
@app.route('/rashifal/<int:rashi_id>')
def get_rashi(rashi_id):
    rashi = next((r for r in rashifal_data if r["id"] == rashi_id), None)
    if rashi:
        return jsonify({"success": True, "data": rashi})
    return jsonify({"success": False, "message": "Rashi not found"}), 404

# Get statuses by category
@app.route('/status/<category>')
def get_status(category):
    if category in status_data:
        return jsonify({
            "success": True,
            "category": category,
            "data": status_data[category]
        })
    return jsonify({"success": False, "message": "Category not found"}), 404

# Get all status categories
@app.route('/status/categories/all')
def get_categories():
    return jsonify({
        "success": True,
        "categories": list(status_data.keys())
    })

if __name__ == '__main__':
    app.run(debug=True)