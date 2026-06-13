from flask import Flask, jsonify, render_template
from flask_cors import CORS
from rashifal_data import get_rashifal_today, get_single_rashi_today
import os

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

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

@app.route('/')
def home():
    return jsonify({
        "message": "RozRashi API is running!",
        "version": "2.0"
    })

@app.route('/app')
def app_ui():
    return render_template('index.html')

@app.route('/rashifal')
def get_all_rashifal():
    return jsonify({
        "success": True,
        "data": get_rashifal_today()
    })

@app.route('/rashifal/<int:rashi_id>')
def get_rashifal_by_id(rashi_id):
    rashi = get_single_rashi_today(rashi_id)
    if rashi:
        return jsonify({"success": True, "data": rashi})
    return jsonify({"success": False, "message": "Rashi not found"}), 404

@app.route('/status/<category>')
def get_status_by_category(category):
    data = STATUS_DATA.get(category)
    if data:
        return jsonify({"success": True, "category": category, "data": data})
    return jsonify({"success": False, "message": "Category not found"}), 404

@app.route('/status/categories/all')
def get_categories():
    return jsonify({
        "success": True,
        "categories": list(STATUS_DATA.keys())
    })

# ════════════════════════════════════════
#  RUN
# ════════════════════════════════════════

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)