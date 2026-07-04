from flask import Flask, jsonify, render_template
from flask_cors import CORS
from rashifal_data import get_rashifal_today, get_single_rashi_today
from chalisa_data import CHALISA_DATA
from mantra_data import MANTRA_DATA
from aarti_data import AARTI_DATA
from tithi_data import get_today_tithi
from festivals_data import get_today_festival
from datetime import datetime
import pytz
IST = pytz.timezone('Asia/Kolkata')
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

# ═══════════════════════════════════════
# CHALISA ROUTES
# ═══════════════════════════════════════

DAILY_CHALISA = {
    0: "shiv",      # Monday
    1: "hanuman",   # Tuesday
    2: "ganesh",    # Wednesday
    3: "laxmi",     # Thursday
    4: "durga",     # Friday
    5: "shani",     # Saturday
    6: "surya",     # Sunday
}

@app.route('/chalisa/today')
def get_today_chalisa():
    day = datetime.now(IST).weekday()
    key = DAILY_CHALISA[day]
    chalisa = CHALISA_DATA.get(key)
    return jsonify({
        "success": True,
        "day_index": day,
        "key": key,
        "data": chalisa
    })

@app.route('/chalisa/all')
def get_all_chalisas():
    result = []
    for key, value in CHALISA_DATA.items():
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

@app.route('/chalisa/<name>')
def get_chalisa(name):
    chalisa = CHALISA_DATA.get(name)
    if chalisa:
        return jsonify({"success": True, "data": chalisa})
    return jsonify({
        "success": False,
        "message": "Chalisa not found"
    }), 404

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

    "mantra_status": [
        """🐘 वक्रतुंड महाकाय
सूर्यकोटि समप्रभ।
निर्विघ्नं कुरु मे देव
सर्वकार्येषु सर्वदा।।
जय श्री गणेश 🌟""",

        """🌺 या देवी सर्वभूतेषु
शक्तिरूपेण संस्थिता।
नमस्तस्यै नमस्तस्यै
नमस्तस्यै नमो नमः।।
जय माता दी 🙏""",

        """🔱 ॐ त्र्यम्बकं यजामहे
सुगन्धिं पुष्टिवर्धनम्।
उर्वारुकमिव बन्धनान्
मृत्योर्मुक्षीय माऽमृतात्।।
हर हर महादेव 🙏""",

        """🪷 ॐ नमो भगवते वासुदेवाय।
जय श्री कृष्ण
हरे कृष्ण हरे कृष्ण
कृष्ण कृष्ण हरे हरे 🌸""",

        """☀️ ॐ घृणि सूर्याय नमः।
सूर्य देव को नमस्कार।
रोग दूर हो, यश बढ़े,
मिले आरोग्य और तेज। 🙏""",

        """🙏 ॐ हं हनुमते नमः।
जय बजरंगबली।
संकट हरो, बल दो,
राम भक्त की रक्षा करो। 💪""",

        """⚫ ॐ शं शनिश्चराय नमः।
शनि देव को प्रणाम।
न्याय करो, दोष हरो,
कृपा करो महाराज। 🙏""",

        """🌺 ॐ दुं दुर्गायै नमः।
जय माँ दुर्गा।
शत्रु नाश करो माँ,
भक्तों की रक्षा करो। 🔱""",

        """🪷 ॐ श्रीं महालक्ष्म्यै नमः।
जय माँ लक्ष्मी।
धन दो, सुख दो,
दरिद्रता दूर करो। 💰""",

        """🐘 ॐ गं गणपतये नमः।
जय श्री गणेश।
विघ्न हरो, बुद्धि दो,
हर काम सफल करो। 🌟""",
    ],

    "festival": [
        """🪔 दीपावली की हार्दिक शुभकामनाएं!
माँ लक्ष्मी की कृपा से
आपके घर में सुख-समृद्धि आए।
खुशियों का यह त्योहार
आपके जीवन में नई रोशनी लाए। 🌟""",

        """🌺 नवरात्रि की शुभकामनाएं!
माँ दुर्गा की शक्ति से
आपके जीवन में नई ऊर्जा आए।
जय माता दी! 🙏""",

        """🏹 राम नवमी की शुभकामनाएं!
मर्यादा पुरुषोत्तम राम के
आशीर्वाद से आपका जीवन
सुखमय और धर्ममय हो। जय श्री राम! 🙏""",

        """🐘 गणेश चतुर्थी की शुभकामनाएं!
गणपति बप्पा मोरया!
सभी बाधाएं दूर हों,
हर काम सफल हो। 🌟""",

        """🦚 जन्माष्टमी की शुभकामनाएं!
श्री कृष्ण के आशीर्वाद से
आपके जीवन में खुशियाँ आएं।
हरे कृष्ण! जय श्री कृष्ण! 🌸""",

        """🎨 होली की हार्दिक शुभकामनाएं!
रंगों के इस पावन त्योहार पर
ईश्वर आपके जीवन को
खुशियों के रंगों से भर दे। 🙏""",

        """🪁 मकर संक्रांति की शुभकामनाएं!
सूर्यदेव की कृपा से
आपके जीवन में नई रोशनी आए।
तिल-गुड़ खाओ, मीठा बोलो। ☀️""",

        """🔱 महाशिवरात्रि की शुभकामनाएं!
भगवान शिव की कृपा से
आपके सभी कष्ट दूर हों।
हर हर महादेव! बम बम भोले! 🙏""",

        """🌸 बसंत पंचमी की शुभकामनाएं!
माँ सरस्वती का आशीर्वाद मिले।
विद्या, बुद्धि और कला में
आप आगे बढ़ते रहें। 🎵 जय माँ सरस्वती!""",

        """🏹 दशहरा की शुभकामनाएं!
बुराई पर अच्छाई की जीत का यह पर्व
आपके जीवन में भी
विजय और सफलता लाए। जय श्री राम! 🙏""",

        """🎀 रक्षाबंधन की शुभकामनाएं!
भाई-बहन के पवित्र रिश्ते को
ईश्वर सदा मजबूत बनाए रखे।
यह पावन धागा सदा रक्षा करे। 💕""",

        """🌅 छठ पूजा की शुभकामनाएं!
भगवान सूर्य की कृपा से
आपके परिवार में सुख-समृद्धि रहे।
जय छठी मैया! जय सूर्यदेव! ☀️""",
    ],

    "stotra": [
        """🕉️ असतो मा सद्गमय।
तमसो मा ज्योतिर्गमय।
मृत्योर्मा अमृतं गमय।
ॐ शांति शांति शांति।।
अर्थ: मुझे असत्य से सत्य की ओर,
अंधेरे से प्रकाश की ओर,
मृत्यु से अमरत्व की ओर ले जाओ। 🙏""",

        """🌟 त्वमेव माता च पिता त्वमेव।
त्वमेव बंधुश्च सखा त्वमेव।
त्वमेव विद्या द्रविणं त्वमेव।
त्वमेव सर्वं मम देव देव।।
अर्थ: हे प्रभु! आप ही मेरी माँ हैं,
पिता हैं, मित्र हैं और सब कुछ हैं। 🙏""",

        """🔱 कर्पूर गौरं करुणावतारं
संसारसारम् भुजगेंद्रहारम्।
सदा वसंतं हृदयारविंदे
भवं भवानी सहितं नमामि।।
अर्थ: कपूर जैसे गौर वर्ण,
करुणा के अवतार शिव को
पार्वती सहित नमस्कार। 🙏""",

        """🪷 शांताकारं भुजगशयनं
पद्मनाभं सुरेशम्।
विश्वाधारं गगनसदृशं
मेघवर्णं शुभाङ्गम्।।
अर्थ: शांत स्वरूप, शेषनाग पर शयन करने वाले,
पद्मनाभ, देवताओं के स्वामी
विष्णु जी को नमस्कार। 🙏""",

        """🌺 सर्वमंगल मांगल्ये
शिवे सर्वार्थ साधिके।
शरण्ये त्र्यंबके गौरि
नारायणि नमोस्तुते।।
अर्थ: हे सब मंगलों की मंगल,
हे शिवे, हे गौरी, हे नारायणी!
आपको नमस्कार है। 🙏""",

        """🐘 वक्रतुंड महाकाय
सूर्यकोटि समप्रभ।
निर्विघ्नं कुरु मे देव
सर्वकार्येषु सर्वदा।।
अर्थ: हे विशाल शरीर वाले,
करोड़ों सूर्यों के समान तेजस्वी गणेश!
मेरे सभी कार्यों में विघ्न दूर करो। 🙏""",

        """🏹 श्री रामचंद्र कृपालु भजु मन
हरण भव भय दारुणम्।
नव कंज लोचन कंज मुख
कर कंज पद कंजारुणम्।।
अर्थ: हे मन! कृपालु श्री रामचंद्र का
भजन कर जो भव भय हरने वाले हैं।
उनके नेत्र, मुख, हाथ और
चरण कमल जैसे लाल हैं। 🙏""",

        """☀️ जयत्यधिकसत्त्वस्थो
रमयन्निव सागरान्।
सूर्यः श्रीमान्महातेजा
जगत्कर्ता जगत्पतिः।।
अर्थ: सत्त्वगुण से परिपूर्ण,
सागरों को प्रकाशित करने वाले,
महातेजस्वी सूर्यदेव की जय हो।
वे जगत के निर्माता और स्वामी हैं। 🙏""",

        """🌸 या कुंदेंदु तुषार हार धवला
या शुभ्र वस्त्रावृता।
या वीणावर दंड मंडित करा
या श्वेत पद्मासना।।
अर्थ: जो कुंद फूल, चंद्रमा और
बर्फ जैसी सफेद हैं,
शुभ वस्त्र धारण किए हैं,
वीणाधारी माँ सरस्वती को नमस्कार। 🙏""",

        """🔱 ॐ नमः शिवाय।
नमस्ते नमस्ते विभो विश्वमूर्ते।
नमस्ते नमस्ते चिदानंदमूर्ते।
नमस्ते नमस्ते तपोयोगागम्य।
नमस्ते नमस्ते श्रुतिज्ञानगम्य।।
हर हर महादेव! 🙏""",

        """🙏 गुरुर्ब्रह्मा गुरुर्विष्णुः
गुरुर्देवो महेश्वरः।
गुरुः साक्षात् परब्रह्म
तस्मै श्री गुरवे नमः।।
अर्थ: गुरु ही ब्रह्मा हैं, विष्णु हैं,
गुरु ही महेश्वर हैं।
गुरु ही साक्षात परब्रह्म हैं —
उन्हें नमस्कार है। 🙏""",

        """🌺 महालक्ष्मी च विद्महे
विष्णुपत्नी च धीमहि।
तन्नो लक्ष्मीः प्रचोदयात्।।
जय माँ लक्ष्मी!
धन दो, सुख दो,
घर में खुशियाँ भर दो। 🪷🙏""",
    ],
}

# ════════════════════════════════════════
#  NOTIFICATION DATA
# ════════════════════════════════════════

HINDI_DAYS = {
    0: "सोमवार",
    1: "मंगलवार",
    2: "बुधवार",
    3: "गुरुवार",
    4: "शुक्रवार",
    5: "शनिवार",
    6: "रविवार"
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
    headers = {
        "Authorization": f"Basic {os.environ.get('ONESIGNAL_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "app_id": os.environ.get("ONESIGNAL_APP_ID"),
        "included_segments": ["All"],
        "headings": {"en": title, "hi": title},
        "contents": {"en": message, "hi": message},
        "small_icon": "ic_stat_onesignal_default"
    }
    try:
        response = requests.post(
            "https://onesignal.com/api/v1/notifications",
            json=payload,
            headers=headers
        )
        print(f"Notification sent: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"Notification error: {e}")
        return None


def send_morning_notification():
    """6:00 AM - Smart notification based on today"""
    from tithi_data import get_today_tithi

    # Check tithi first (highest priority)
    tithi = get_today_tithi()
    if tithi:
        send_onesignal_notification(
            tithi["notification_title"],
            tithi["notification_msg"]
        )
        return

    # Check festival
    festival = get_today_festival()
    if festival:
        send_onesignal_notification(
            festival["notification_title"],
            festival["notification_msg"]
        )
        return

    # Normal day - Rashifal notification
    send_onesignal_notification(
        "🌅 शुभ प्रभात! आज का राशिफल तैयार है",
        "आज का दिन कैसा रहेगा? अपनी राशि चेक करें "
        "और दिन की शुभ शुरुआत करें 🙏"
    )


def send_aarti_notification():
    """8:00 AM - Stotra + Aarti"""
    day = datetime.now(IST).weekday()
    aarti = AARTI_INFO[day]
    send_onesignal_notification(
        f"🪔 संध्या आरती — {aarti['name']}",
        f"आज की {aarti['name']} करें और "
        f"ईश्वर का आभार व्यक्त करें "
        f"{aarti['emoji']} 🙏"
    )


def send_chalisa_notification():
    """7:00 PM - Chalisa + Mantra"""
    day = datetime.now(IST).weekday()
    hindi_day = HINDI_DAYS[day]
    chalisa = CHALISA_INFO[day]
    send_onesignal_notification(
        f"{chalisa['emoji']} आज की चालीसा — {chalisa['name']}",
        f"आज {hindi_day} है। {chalisa['god']} की "
        f"{chalisa['name']} पढ़ें और मंत्र जपें। "
        f"मन को शांति और आशीर्वाद मिलेगा 🕉️"
    )


# ════════════════════════════════════════
#  SCHEDULER
# ════════════════════════════════════════

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=IST)

    # 6:00 AM - Good Morning + Rashifal
    scheduler.add_job(
        send_morning_notification,
        'cron', hour=6, minute=0)

    # 8:00 AM - Stotra + Aarti
    scheduler.add_job(
        send_aarti_notification,
        'cron', hour=8, minute=0)

    # 7:00 PM - Chalisa + Mantra
    scheduler.add_job(
        send_chalisa_notification,
        'cron', hour=19, minute=0)

    scheduler.start()
    print("Scheduler started ✅")

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

@app.route('/privacy')
def privacy_policy():
    return render_template('privacy.html')

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

@app.route('/today/special')
def get_today_special():
    """Returns today's special event if any"""
    from tithi_data import get_today_tithi
    tithi = get_today_tithi()
    if tithi:
        return jsonify({"success": True,
                       "type": "tithi",
                       "data": tithi})
    festival = get_today_festival()
    if festival:
        return jsonify({"success": True,
                       "type": "festival",
                       "data": festival})
    return jsonify({"success": False,
                   "message": "No special event today"})

@app.route('/status/categories/all')
def get_categories():
    return jsonify({
        "success": True,
        "categories": list(STATUS_DATA.keys())
    })

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
#  RUN
# ════════════════════════════════════════

# Start scheduler
start_scheduler()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)