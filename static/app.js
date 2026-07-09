// ===== API URL =====
const API_URL = 'https://rozrashi-api.onrender.com';

// ===== APP DOWNLOAD LINK (VIRAL SHARE WATERMARK) =====
const APP_LINK = '\n\n📲 RozRashi App Download करें\n👉 https://play.google.com/store/apps/details?id=com.rozrashi.app';

// ===== TRACK PREVIOUS SCREEN =====
let previousScreen = 'home';

// ===== SET TODAY'S DATE IN HINDI =====
function setTodayDate() {
    const days = ['रविवार', 'सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार'];
    const months = ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून',
                    'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'];
    const today = new Date();
    const dateStr = `${days[today.getDay()]}, ${today.getDate()} ${months[today.getMonth()]}`;
    document.getElementById('today-date').textContent = dateStr;
}

// ===== SHOW TOAST MESSAGE =====
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 2500);
}

// ===== SHOW/HIDE SCREENS =====
function showScreen(screenName, addToHistory = true) {
    // Save current screen to history before switching
    const currentScreen = document.querySelector('.screen.active');
    if (addToHistory && currentScreen) {
        const currentId = currentScreen.id.replace('screen-', '');
        if (currentId !== screenName) {
            navHistory.push(currentId);
            history.pushState(null, '', window.location.href);
        }
    }

    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('screen-' + screenName).classList.add('active');
    const navBtn = document.getElementById('nav-' + screenName);
    if (navBtn) navBtn.classList.add('active');
    if (screenName === 'home') loadHome();
    if (screenName === 'rashifal') loadRashifalScreen();
    if (screenName === 'status') loadStatus('good_morning', document.querySelector('#screen-status .tab-btn'));
    if (screenName === 'chalisa') loadChalisaList(document.querySelector('#screen-chalisa .tab-btn'));
    if (screenName === 'aarti') loadAartiList(document.querySelector('#screen-aarti .tab-btn'));
    if (screenName === 'mantra') loadMantraList(document.querySelector('#screen-mantra .tab-btn'));
    if (screenName === 'stotra') loadStotraList(document.querySelector('#screen-stotra .tab-btn'));
    if (screenName === 'panchang') loadPanchang();
    if (screenName === 'kundali') { /* form is static, no load needed */ }
    previousScreen = screenName;
}

// ===== GO BACK =====
function goBack() {
    showScreen('rashifal');
}

// ===== LOAD HOME SCREEN =====
async function loadHome() {
    loadRashiGrid('rashi-grid');
    loadHomeStatusPreview();
    loadHomeTodayLabels();
}

// ===== LOAD TODAY LABELS FOR HOME CARDS =====
async function loadHomeTodayLabels() {
    try {
        // Aarti today label + direct link
        const aartiRes = await fetch(`${API_URL}/aarti/today`);
        const aartiJson = await aartiRes.json();
        const aartiLabel = document.getElementById('home-aarti-label');
        if (aartiLabel) {
            aartiLabel.textContent = aartiJson.data.god;
        }
        const aartiCard = document.getElementById('home-aarti-card');
        if (aartiCard) {
            aartiCard.onclick = () => showAartiDetail(aartiJson.key);
        }
    } catch (err) {
        const aartiLabel = document.getElementById('home-aarti-label');
        if (aartiLabel) aartiLabel.textContent = 'आज की आरती';
        const aartiCard = document.getElementById('home-aarti-card');
        if (aartiCard) aartiCard.onclick = () => showScreen('aarti');
    }

    try {
        // Chalisa today label + direct link
        const chalisaRes = await fetch(`${API_URL}/chalisa/today`);
        const chalisaJson = await chalisaRes.json();
        const chalisaLabel = document.getElementById('home-chalisa-label');
        if (chalisaLabel) {
            chalisaLabel.textContent = chalisaJson.data.god;
        }
        const chalisaCard = document.getElementById('home-chalisa-card');
        if (chalisaCard) {
            chalisaCard.onclick = () => showChalisaDetail(chalisaJson.key);
        }
    } catch (err) {
        const chalisaLabel = document.getElementById('home-chalisa-label');
        if (chalisaLabel) chalisaLabel.textContent = 'आज की चालीसा';
        const chalisaCard = document.getElementById('home-chalisa-card');
        if (chalisaCard) chalisaCard.onclick = () => showScreen('chalisa');
    }

    try {
        // Mantra today label + direct link
        const mantraRes = await fetch(`${API_URL}/mantra/today`);
        const mantraJson = await mantraRes.json();
        const mantraLabel = document.getElementById('home-mantra-label');
        if (mantraLabel) {
            mantraLabel.textContent = mantraJson.data.god;
        }
        const mantraCard = document.getElementById('home-mantra-card');
        if (mantraCard) {
            mantraCard.onclick = () => showMantraDetail(mantraJson.key);
        }
    } catch (err) {
        const mantraLabel = document.getElementById('home-mantra-label');
        if (mantraLabel) mantraLabel.textContent = 'आज के मंत्र';
        const mantraCard = document.getElementById('home-mantra-card');
        if (mantraCard) mantraCard.onclick = () => showScreen('mantra');
    }
}

// ===== LOAD RASHI GRID =====
async function loadRashiGrid(containerId) {
    try {
        const res = await fetch(`${API_URL}/rashifal`);
        const json = await res.json();
        const container = document.getElementById(containerId);
        container.innerHTML = '';

        json.data.forEach(rashi => {
            const card = document.createElement('div');
            card.className = 'rashi-mini-card';
            card.innerHTML = `
                <span class="symbol">${rashi.symbol}</span>
                <div class="name">${rashi.name}</div>
                <div class="english">${rashi.english}</div>
            `;
            card.onclick = () => showRashiDetail(rashi.id);
            container.appendChild(card);
        });
    } catch (err) {
        document.getElementById(containerId).innerHTML =
            '<div class="loading">लोड नहीं हो सकी। इंटरनेट चेक करें।</div>';
    }
}

// ===== LOAD RASHIFAL SCREEN =====
function loadRashifalScreen() {
    loadRashiGrid('rashifal-grid');
}

// ===== SHOW RASHI DETAIL =====
async function showRashiDetail(rashiId) {
    // Hide all screens, show detail screen
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('screen-rashi-detail').classList.add('active');
    previousScreen = 'rashifal';

    const content = document.getElementById('rashi-detail-content');
    content.innerHTML = '<div class="loading">राशिफल लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/rashifal/${rashiId}`);
        const json = await res.json();
        const r = json.data;

        content.innerHTML = `
            <div class="rashi-detail-card">
                <span class="big-symbol">${r.symbol}</span>
                <h2>${r.name} राशि</h2>
                <div class="english-name">${r.english}</div>
                <div class="message">🌟 ${r.message}</div>
                <div class="lucky-row">
                    <span class="lucky-badge">🔢 लकी नंबर: ${r.lucky_number}</span>
                    <span class="lucky-badge">🎨 लकी रंग: ${r.lucky_color}</span>
                </div>
            </div>
            <button class="btn-share" style="width:100%; padding:12px; font-size:15px; border-radius:12px;"
                onclick="shareRashifal('${r.name}', '${r.symbol}', \`${r.message}\`, ${r.lucky_number}, '${r.lucky_color}')">
                📤 WhatsApp पर शेयर करें
            </button>
        `;
    } catch (err) {
        content.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

// ===== SHARE RASHIFAL (WITH APP LINK WATERMARK) =====
function shareRashifal(name, symbol, message, luckyNum, luckyColor) {
    const text = `${symbol} ${name} राशिफल 🌟\n\n${message}\n\n🔢 लकी नंबर: ${luckyNum}\n🎨 लकी रंग: ${luckyColor}${APP_LINK}`;
    if (window.Android) {
        Android.shareText(text);
    } else if (navigator.share) {
        navigator.share({ text: text });
    } else {
        navigator.clipboard.writeText(text);
        showToast('📋 राशिफल कॉपी हो गया!');
    }
}

// ===== LOAD STATUS BY CATEGORY =====
async function loadStatus(category, btnElement) {
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    const statusList = document.getElementById('status-list');
    statusList.innerHTML = '<div class="loading">स्टेटस लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/status/${category}`);
        const json = await res.json();
        statusList.innerHTML = '';

        json.data.forEach((text, index) => {
            const card = document.createElement('div');
            card.className = 'status-card';
            card.innerHTML = `
                <div class="status-text">${text}</div>
                <div class="status-actions">
                    <button class="btn-image" style="flex:1" onclick="openGenerator(\`${text.replace(/`/g, "'")}\`)">
                        📤 WhatsApp / Share
                    </button>
                </div>
            `;
            statusList.appendChild(card);
        });
    } catch (err) {
        statusList.innerHTML = '<div class="loading">लोड नहीं हो सकी। इंटरनेट चेक करें।</div>';
    }
}

// ===== COPY STATUS =====
function copyStatus(text) {
    const fullText = text + APP_LINK;
    navigator.clipboard.writeText(fullText)
        .then(() => showToast('✅ कॉपी हो गया!'))
        .catch(() => showToast('❌ कॉपी नहीं हो सका'));
}

// ===== SHARE STATUS (WITH APP LINK WATERMARK) =====
function shareStatus(text) {
    const fullText = text + APP_LINK;
    if (window.Android) {
        Android.shareText(fullText);
    } else if (navigator.share) {
        navigator.share({ text: fullText });
    } else {
        navigator.clipboard.writeText(fullText);
        showToast('✅ कॉपी हो गया! अब WhatsApp पर पेस्ट करें');
    }
}

// ===== LOAD HOME STATUS PREVIEW =====
async function loadHomeStatusPreview() {
    try {
        const res = await fetch(
            `${API_URL}/status/bhakti_quotes`);
        const json = await res.json();
        const container = document.getElementById(
            'home-status-preview');
        container.innerHTML = '';

        const preview = json.data.slice(0, 2);
        preview.forEach(text => {
            const card = document.createElement('div');
            card.className = 'status-card';
            card.innerHTML = `
                <div class="status-text">${text}</div>
                <div class="status-actions">
                    <button class="btn-image" style="flex:1" onclick="openGenerator(\`${text.replace(/`/g, "'")}\`)">
                        📤 WhatsApp / Share
                    </button>
                </div>
            `;
            container.appendChild(card);
        });

        const seeAll = document.createElement('button');
        seeAll.className = 'btn-share';
        seeAll.style = 'width:100%;padding:12px;border-radius:12px;margin-top:8px;font-size:14px;';
        seeAll.textContent = '✨ सभी भक्ति Status देखें';
        seeAll.onclick = () => showScreen('status');
        container.appendChild(seeAll);

    } catch (err) {
        document.getElementById('home-status-preview')
            .innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

// ===== CHALISA FUNCTIONS =====

async function loadChalisaList(btnElement) {
    document.querySelectorAll('#screen-chalisa .tab-btn')
        .forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    const container = document.getElementById('chalisa-list');
    container.innerHTML = '<div class="loading">लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/chalisa/all`);
        const json = await res.json();
        container.innerHTML = '';

        json.data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'rashi-mini-card';
            card.style = 'text-align:center; cursor:pointer;';
            card.innerHTML = `
                <span class="symbol">${item.symbol}</span>
                <div class="name">${item.name}</div>
                <div class="english" style="font-size:11px;">${item.god}</div>
                <div class="english" style="font-size:10px; opacity:0.7;">${item.day}</div>
            `;
            card.onclick = () => showChalisaDetail(item.key);
            container.appendChild(card);
        });
    } catch (err) {
        container.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

async function loadTodayChalisa(btnElement) {
    document.querySelectorAll('#screen-chalisa .tab-btn')
        .forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    const container = document.getElementById('chalisa-list');
    container.innerHTML = '<div class="loading">लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/chalisa/today`);
        const json = await res.json();
        container.innerHTML = '';

        const item = json.data;
        const card = document.createElement('div');
        card.className = 'rashi-mini-card';
        card.style = 'text-align:center; cursor:pointer;';
        card.innerHTML = `
            <span class="symbol">${item.symbol}</span>
            <div class="name">${item.name}</div>
            <div class="english">${item.god}</div>
            <div class="english" style="font-size:10px;">${item.day}</div>
        `;
        card.onclick = () => showChalisaDetail(json.key);
        container.appendChild(card);
    } catch (err) {
        container.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

async function showChalisaDetail(key) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('screen-chalisa-detail').classList.add('active');

    const content = document.getElementById('chalisa-detail-content');
    content.innerHTML = '<div class="loading">चालीसा लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/chalisa/${key}`);
        const json = await res.json();
        const c = json.data;

        let versesHTML = '';
        c.verses.forEach(v => {
            versesHTML += `
                <div class="status-card" style="margin-bottom:12px;">
                    <div style="font-size:11px; color:#FF6B00; margin-bottom:6px; font-weight:bold;">
                        ${v.type === 'doha' ? '📖 दोहा' : `🔢 चौपाई ${v.id}`}
                    </div>
                    <div class="status-text" style="font-size:16px; line-height:1.9;">${v.text}</div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:8px; font-style:italic;">
                        📝 ${v.meaning}
                    </div>
                </div>
            `;
        });

        content.innerHTML = `
            <div class="rashi-detail-card" style="text-align:center; margin-bottom:16px;">
                <span class="big-symbol">${c.symbol}</span>
                <h2>${c.name}</h2>
                <div class="english-name">${c.god} • ${c.day}</div>
                <div class="message" style="font-size:13px;">✨ ${c.benefit}</div>
            </div>
            ${versesHTML}
        `;
    } catch (err) {
        content.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

function goBackToChalisa() {
    showScreen('chalisa');
}

// ===== AARTI FUNCTIONS =====

async function loadAartiList(btnElement) {
    document.querySelectorAll('#screen-aarti .tab-btn')
        .forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    const container = document.getElementById('aarti-list');
    container.innerHTML = '<div class="loading">लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/aarti/all`);
        const json = await res.json();
        container.innerHTML = '';

        json.data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'rashi-mini-card';
            card.style = 'text-align:center; cursor:pointer;';
            card.innerHTML = `
                <span class="symbol">${item.symbol}</span>
                <div class="name">${item.name}</div>
                <div class="english" style="font-size:11px;">${item.god}</div>
                <div class="english" style="font-size:10px; opacity:0.7;">${item.day}</div>
            `;
            card.onclick = () => showAartiDetail(item.key);
            container.appendChild(card);
        });
    } catch (err) {
        container.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

async function loadTodayAarti(btnElement) {
    document.querySelectorAll('#screen-aarti .tab-btn')
        .forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    const container = document.getElementById('aarti-list');
    container.innerHTML = '<div class="loading">लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/aarti/today`);
        const json = await res.json();
        container.innerHTML = '';

        const item = json.data;
        const card = document.createElement('div');
        card.className = 'rashi-mini-card';
        card.style = 'text-align:center; cursor:pointer;';
        card.innerHTML = `
            <span class="symbol">${item.symbol}</span>
            <div class="name">${item.name}</div>
            <div class="english">${item.god}</div>
            <div class="english" style="font-size:10px;">${item.day}</div>
        `;
        card.onclick = () => showAartiDetail(json.key);
        container.appendChild(card);
    } catch (err) {
        container.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

async function showAartiDetail(key) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('screen-aarti-detail').classList.add('active');

    const content = document.getElementById('aarti-detail-content');
    content.innerHTML = '<div class="loading">आरती लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/aarti/${key}`);
        const json = await res.json();
        const a = json.data;

        let versesHTML = '';
        a.verses.forEach(v => {
            versesHTML += `
                <div class="status-card" style="margin-bottom:12px;">
                    <div class="status-text" style="font-size:16px; line-height:2.0;">${v.text}</div>
                    <div style="font-size:12px; color:#94a3b8; margin-top:8px; font-style:italic;">
                        📝 ${v.meaning}
                    </div>
                </div>
            `;
        });

        content.innerHTML = `
            <div class="rashi-detail-card" style="text-align:center; margin-bottom:16px;">
                <span class="big-symbol">${a.symbol}</span>
                <h2>${a.name}</h2>
                <div class="english-name">${a.god} • ${a.day}</div>
                <div class="message" style="font-size:13px;">✨ ${a.benefit}</div>
            </div>
            ${versesHTML}
        `;
    } catch (err) {
        content.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

function goBackToAarti() {
    showScreen('aarti');
}

// ===== MANTRA FUNCTIONS =====

async function loadMantraList(btnElement) {
    document.querySelectorAll('#screen-mantra .tab-btn')
        .forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    const container = document.getElementById('mantra-list');
    container.innerHTML = '<div class="loading">लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/mantra/all`);
        const json = await res.json();
        container.innerHTML = '';

        json.data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'rashi-mini-card';
            card.style = 'text-align:center; cursor:pointer;';
            card.innerHTML = `
                <span class="symbol">${item.symbol}</span>
                <div class="name">${item.day}</div>
                <div class="english" style="font-size:11px;">${item.god}</div>
            `;
            card.onclick = () => showMantraDetail(item.key);
            container.appendChild(card);
        });
    } catch (err) {
        container.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

async function loadTodayMantra(btnElement) {
    document.querySelectorAll('#screen-mantra .tab-btn')
        .forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    const container = document.getElementById('mantra-list');
    container.innerHTML = '<div class="loading">लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/mantra/today`);
        const json = await res.json();
        showMantraDetail(json.key);
    } catch (err) {
        container.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

async function showMantraDetail(key) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    // reuse mantra screen itself for detail
    document.getElementById('screen-mantra').classList.add('active');

    const container = document.getElementById('mantra-list');
    container.innerHTML = '<div class="loading">मंत्र लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/mantra/${key}`);
        const json = await res.json();
        const m = json.data;

        let mantrasHTML = `
            <div class="rashi-detail-card" style="text-align:center; margin-bottom:16px;">
                <span class="big-symbol">${m.symbol}</span>
                <h2>${m.day} के मंत्र</h2>
                <div class="english-name">${m.god}</div>
                <div class="message" style="font-size:13px;">✨ ${m.benefit}</div>
            </div>
            <button class="btn-copy"
                style="width:100%;padding:10px;border-radius:12px;
                       margin-bottom:12px;font-size:13px;"
                onclick="loadMantraList(null)">
                ← सभी दिन के मंत्र देखें
            </button>
        `;

        m.mantras.forEach(mantra => {
            mantrasHTML += `
                <div class="status-card" style="margin-bottom:14px;">
                    <div style="font-size:13px; color:#FF6B00;
                                font-weight:bold; margin-bottom:8px;">
                        🕉️ ${mantra.title}
                    </div>
                    <div class="status-text"
                         style="font-size:17px; line-height:2.0; color:#CC5500;">
                        ${mantra.mantra}
                    </div>
                    <div style="font-size:12px; color:#8B6914;
                                margin-top:6px; font-style:italic;">
                        🔤 ${mantra.transliteration}
                    </div>
                    <div style="font-size:12px; color:#5C3D00; margin-top:6px;">
                        📝 ${mantra.meaning}
                    </div>
                    <div style="font-size:11px; color:#2D6A2D; margin-top:6px;">
                        🔢 जाप: ${mantra.jaap_count} बार | ✨ ${mantra.benefit}
                    </div>
                    <div class="status-actions" style="margin-top:10px;">
                        <button class="btn-image" style="flex:1"
                            onclick="openGenerator(\`${mantra.mantra.replace(/`/g, "'")}\`)">
                            📤 WhatsApp / Share
                        </button>
                    </div>
                </div>
            `;
        });

        container.innerHTML = mantrasHTML;
    } catch (err) {
        container.innerHTML = '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

// ===== STOTRA FUNCTIONS =====

async function loadStotraList(btnElement) {
    document.querySelectorAll('#screen-stotra .tab-btn')
        .forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    const container = document.getElementById('stotra-list');
    container.innerHTML =
        '<div class="loading">स्तोत्र लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/stotra/all`);
        const json = await res.json();
        container.innerHTML = '';

        json.data.forEach(stotra => {
            const card = document.createElement('div');
            card.className = 'rashi-mini-card';
            card.style.cssText =
                'text-align:left;padding:14px;margin-bottom:10px;' +
                'display:flex;align-items:center;gap:12px;';
            card.innerHTML = `
                <span style="font-size:32px">
                    ${stotra.symbol}
                </span>
                <div>
                    <div class="name" style="font-size:15px">
                        ${stotra.name}
                    </div>
                    <div class="english">
                        ${stotra.god}
                    </div>
                    <div style="font-size:11px;color:#FF6B00;
                                margin-top:3px;">
                        ${stotra.verse_count} श्लोक
                    </div>
                </div>
            `;
            card.onclick = () => showStotraDetail(stotra.key);
            container.appendChild(card);
        });
    } catch (err) {
        container.innerHTML =
            '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

async function showStotraDetail(key) {
    document.querySelectorAll('.screen')
        .forEach(s => s.classList.remove('active'));
    document.getElementById('screen-stotra-detail')
        .classList.add('active');

    const content = document.getElementById(
        'stotra-detail-content');
    content.innerHTML =
        '<div class="loading">लोड हो रही है...</div>';

    try {
        const res = await fetch(`${API_URL}/stotra/${key}`);
        const json = await res.json();
        const s = json.data;

        let versesHtml = '';
        s.verses.forEach(verse => {
            versesHtml += `
                <div class="status-card"
                     style="margin-bottom:14px;">
                    <div style="font-size:15px;
                                line-height:1.9;
                                color:#ffffff;
                                font-family:'Hind',sans-serif;
                                white-space:pre-line;
                                margin-bottom:10px;">
                        ${verse.text}
                    </div>
                    <div style="font-size:13px;
                                color:#FF6B00;
                                line-height:1.6;
                                border-top:1px solid #2a2a4a;
                                padding-top:8px;">
                        📖 ${verse.meaning}
                    </div>
                    <div class="status-actions"
                         style="margin-top:10px;">
                        <button class="btn-copy"
                            onclick="copyStatus(
                                \`${verse.text.replace(
                                    /`/g,"'")}\`)">
                            📋 कॉपी
                        </button>
                        <button class="btn-image"
                            onclick="openGenerator(
                                \`${verse.text.replace(
                                    /`/g,"'")}\`)">
                            🎨 Image
                        </button>
                    </div>
                </div>
            `;
        });

        content.innerHTML = `
            <div class="rashi-detail-card"
                 style="margin-bottom:16px;">
                <span class="big-symbol">
                    ${s.symbol}
                </span>
                <h2>${s.name}</h2>
                <div class="english-name">${s.god}</div>
                <div class="message">
                    ✨ ${s.benefit}
                </div>
            </div>
            ${versesHtml}
        `;
    } catch (err) {
        content.innerHTML =
            '<div class="loading">लोड नहीं हो सकी।</div>';
    }
}

function goBackToStotra() {
    document.querySelectorAll('.screen')
        .forEach(s => s.classList.remove('active'));
    document.getElementById('screen-stotra')
        .classList.add('active');
}

// Load stotra when screen opens
const originalShowScreen = showScreen;

// ================================================================
// ADD THESE FUNCTIONS IN app.js
// Place them BEFORE the "// ===== INIT APP =====" line
// ================================================================


// ===== PANCHANG FUNCTIONS =====

let panchangLat = 23.1765;  // Default Ujjain
let panchangLng = 75.7885;
let panchangLocationName = 'उज्जैन (डिफ़ॉल्ट)';

async function loadPanchang() {
    const content = document.getElementById('panchang-content');
    const locationText = document.getElementById('panchang-location-text');

    content.innerHTML = '<div class="loading">पंचांग लोड हो रही है...</div>';
    if (locationText) {
        locationText.textContent = `📍 ${panchangLocationName}`;
    }

    try {
        const url = `${API_URL}/panchang?lat=${panchangLat}&lng=${panchangLng}&tz=5.5`;
        const res = await fetch(url);
        const json = await res.json();

        if (!json.success) {
            content.innerHTML = `<div class="loading">❌ ${json.message || 'लोड नहीं हो सकी'}</div>`;
            return;
        }

        const d = json.data;

        content.innerHTML = `
            <!-- Date Header -->
            <div class="rashi-detail-card" style="text-align:center;margin-bottom:16px;padding:16px;">
                <div style="font-size:28px;margin-bottom:4px;">🗓️</div>
                <h2 style="margin:4px 0;font-size:18px;">${json.date}</h2>
                <div style="font-size:13px;color:#a78bfa;">${d.vikram_samvat ? `विक्रम संवत ${d.vikram_samvat}` : ''}</div>
                <div style="font-size:13px;color:#94a3b8;">${d.lunar_month ? `${d.lunar_month} मास` : ''}</div>
            </div>

            <!-- Main Panchang Grid -->
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;">

                <div class="status-card" style="padding:12px;text-align:center;">
                    <div style="font-size:11px;color:#FF6B00;font-weight:bold;margin-bottom:4px;">🌅 सूर्योदय</div>
                    <div style="font-size:18px;font-weight:bold;color:#ffd200;">${d.sunrise || '--'}</div>
                </div>

                <div class="status-card" style="padding:12px;text-align:center;">
                    <div style="font-size:11px;color:#FF6B00;font-weight:bold;margin-bottom:4px;">🌇 सूर्यास्त</div>
                    <div style="font-size:18px;font-weight:bold;color:#ffd200;">${d.sunset || '--'}</div>
                </div>

            </div>

            <!-- Tithi, Nakshatra, Yoga, Karan -->
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;">

                <div class="status-card" style="padding:12px;">
                    <div style="font-size:11px;color:#FF6B00;font-weight:bold;margin-bottom:4px;">🌙 तिथि</div>
                    <div style="font-size:15px;font-weight:bold;">${d.tithi || '--'}</div>
                    ${d.tithi_ends ? `<div style="font-size:10px;color:#94a3b8;margin-top:4px;">समाप्त: ${d.tithi_ends}</div>` : ''}
                </div>

                <div class="status-card" style="padding:12px;">
                    <div style="font-size:11px;color:#FF6B00;font-weight:bold;margin-bottom:4px;">⭐ नक्षत्र</div>
                    <div style="font-size:15px;font-weight:bold;">${d.nakshatra || '--'}</div>
                    ${d.nakshatra_lord ? `<div style="font-size:10px;color:#94a3b8;margin-top:4px;">स्वामी: ${d.nakshatra_lord}</div>` : ''}
                </div>

                <div class="status-card" style="padding:12px;">
                    <div style="font-size:11px;color:#FF6B00;font-weight:bold;margin-bottom:4px;">🔯 योग</div>
                    <div style="font-size:15px;font-weight:bold;">${d.yoga || '--'}</div>
                    ${d.yoga_ends ? `<div style="font-size:10px;color:#94a3b8;margin-top:4px;">समाप्त: ${d.yoga_ends}</div>` : ''}
                </div>

                <div class="status-card" style="padding:12px;">
                    <div style="font-size:11px;color:#FF6B00;font-weight:bold;margin-bottom:4px;">📿 करण</div>
                    <div style="font-size:15px;font-weight:bold;">${d.karan || '--'}</div>
                </div>

            </div>

            <!-- Rahu Kaal - highlighted in red -->
            <div class="status-card"
                 style="padding:14px;margin-bottom:12px;
                        border:1px solid rgba(220,38,38,0.4);
                        background:rgba(220,38,38,0.08);">
                <div style="font-size:12px;color:#ef4444;font-weight:bold;margin-bottom:4px;">
                    ⚠️ राहुकाल (अशुभ समय)
                </div>
                <div style="font-size:17px;font-weight:bold;color:#fca5a5;">
                    ${d.rahu_kaal || '--'}
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:4px;">
                    इस समय में शुभ कार्य न करें
                </div>
            </div>

            <!-- Share Panchang -->
            <button onclick="sharePanchang('${json.date}', '${d.tithi}', '${d.nakshatra}', '${d.yoga}', '${d.rahu_kaal}', '${d.sunrise}', '${d.sunset}')"
                    class="btn-share"
                    style="width:100%;padding:12px;border-radius:12px;
                           font-size:14px;margin-bottom:16px;">
                📤 पंचांग WhatsApp पर शेयर करें
            </button>
        `;

    } catch (err) {
        content.innerHTML = '<div class="loading">❌ पंचांग लोड नहीं हो सका। इंटरनेट चेक करें।</div>';
    }
}

function getPanchangLocation() {
    if (!navigator.geolocation) {
        showToast('❌ GPS इस डिवाइस पर उपलब्ध नहीं है');
        return;
    }

    const locationText = document.getElementById('panchang-location-text');
    if (locationText) locationText.textContent = '📍 स्थान प्राप्त हो रहा है...';

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            panchangLat = position.coords.latitude;
            panchangLng = position.coords.longitude;

            // Reverse geocode to get city name
            try {
                const res = await fetch(
                    `https://nominatim.openstreetmap.org/reverse?lat=${panchangLat}&lon=${panchangLng}&format=json`,
                    { headers: { 'User-Agent': 'RozRashi/1.0' } }
                );
                const json = await res.json();
                const addr = json.address || {};
                panchangLocationName = addr.city || addr.town || addr.village || 'आपका स्थान';
            } catch {
                panchangLocationName = 'आपका स्थान';
            }

            showToast(`✅ स्थान मिला: ${panchangLocationName}`);
            loadPanchang();
        },
        (error) => {
            showToast('❌ स्थान नहीं मिला। उज्जैन का पंचांग दिखाया जा रहा है।');
            panchangLocationName = 'उज्जैन (डिफ़ॉल्ट)';
            loadPanchang();
        },
        { timeout: 8000, maximumAge: 300000 }
    );
}

function sharePanchang(date, tithi, nakshatra, yoga, rahu, sunrise, sunset) {
    const text = `🗓️ आज का पंचांग — ${date}

🌙 तिथि: ${tithi}
⭐ नक्षत्र: ${nakshatra}
🔯 योग: ${yoga}
⚠️ राहुकाल: ${rahu}
🌅 सूर्योदय: ${sunrise}
🌇 सूर्यास्त: ${sunset}
${APP_LINK}`;

    if (window.Android) {
        Android.shareText(text);
    } else if (navigator.share) {
        navigator.share({ text });
    } else {
        navigator.clipboard.writeText(text);
        showToast('✅ पंचांग कॉपी हो गया!');
    }
}


// ===== KUNDALI FUNCTIONS =====

let citySearchTimeout = null;
let selectedCityLat = null;
let selectedCityLng = null;

async function searchCity(query) {
    clearTimeout(citySearchTimeout);
    const suggestions = document.getElementById('city-suggestions');

    if (query.length < 2) {
        suggestions.style.display = 'none';
        return;
    }

    citySearchTimeout = setTimeout(async () => {
        try {
            const res = await fetch(`${API_URL}/city-search?q=${encodeURIComponent(query)}`);
            const json = await res.json();

            if (json.data && json.data.length > 0) {
                suggestions.innerHTML = '';
                json.data.forEach(city => {
                    const item = document.createElement('div');
                    item.style = `padding:10px 12px;cursor:pointer;border-bottom:
                                  1px solid #FFD49A;font-size:13px;color:#2D1B00;
                                  background:#FFF0E0;`;
                    item.textContent = city.name + (city.full.includes(',') ?
                        ' — ' + city.full.split(',').slice(1, 3).join(',').trim() : '');
                    item.onmousedown = () => {
                        document.getElementById('k-city').value = city.name;
                        document.getElementById('k-lat').value  = city.lat;
                        document.getElementById('k-lng').value  = city.lng;
                        selectedCityLat = city.lat;
                        selectedCityLng = city.lng;
                        suggestions.style.display = 'none';
                    };
                    suggestions.appendChild(item);
                });
                suggestions.style.display = 'block';
            } else {
                suggestions.style.display = 'none';
            }
        } catch {
            suggestions.style.display = 'none';
        }
    }, 400);
}

// Hide suggestions when clicking outside
document.addEventListener('click', (e) => {
    const suggestions = document.getElementById('city-suggestions');
    if (suggestions && !suggestions.contains(e.target)) {
        suggestions.style.display = 'none';
    }
});

async function generateKundali() {
    const name  = document.getElementById('k-name').value.trim() || 'जातक';
    const dob   = document.getElementById('k-dob').value;
    const tob   = document.getElementById('k-tob').value;
    const city  = document.getElementById('k-city').value.trim();
    const lat   = document.getElementById('k-lat').value;
    const lng   = document.getElementById('k-lng').value;

    // Validate
    if (!dob) { showToast('❌ जन्म तिथि भरें'); return; }
    if (!tob) { showToast('❌ जन्म समय भरें');  return; }
    if (!city) { showToast('❌ जन्म स्थान भरें'); return; }
    if (!lat)  { showToast('❌ सुझाव में से शहर चुनें'); return; }

    const result = document.getElementById('kundali-result');
    result.style.display = 'block';
    result.innerHTML = '<div class="loading">🔮 कुंडली बन रही है...</div>';

    // Scroll to result
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
        const res = await fetch(`${API_URL}/kundali`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, dob, tob, city, lat: parseFloat(lat), lng: parseFloat(lng) })
        });
        const json = await res.json();

        if (!json.success) {
            result.innerHTML = `<div class="loading">❌ ${json.message}</div>`;
            return;
        }

        // Build planets table HTML
        let planetsHTML = '';
        if (json.planets && json.planets.length > 0) {
            planetsHTML = `
                <div class="status-card" style="margin-bottom:12px;padding:14px;">
                    <div style="font-size:13px;color:#FF6B00;font-weight:bold;margin-bottom:10px;">
                        🪐 ग्रह स्थिति
                    </div>
                    <table style="width:100%;border-collapse:collapse;font-size:13px;">
                        <tr style="color:#a78bfa;border-bottom:1px solid rgba(255,107,0,0.2);">
                            <th style="text-align:left;padding:6px 4px;">ग्रह</th>
                            <th style="text-align:left;padding:6px 4px;">राशि</th>
                            <th style="text-align:right;padding:6px 4px;">अंश</th>
                        </tr>
                        ${json.planets.map(p => `
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:7px 4px;color:#fff;">
                                ${p.name}
                                ${p.is_retro ? '<span style="color:#ef4444;font-size:10px;">(वक्री)</span>' : ''}
                            </td>
                            <td style="padding:7px 4px;color:#ffd200;">${p.rashi}</td>
                            <td style="padding:7px 4px;text-align:right;color:#94a3b8;">${p.degree}°</td>
                        </tr>`).join('')}
                    </table>
                </div>
            `;
        }

        // Build kundali chart HTML
        let chartHTML = '';
        if (json.kundali_svg) {
            chartHTML = `
                <div class="status-card" style="margin-bottom:12px;padding:14px;text-align:center;">
                    <div style="font-size:13px;color:#FF6B00;font-weight:bold;margin-bottom:10px;">
                        🔯 जन्म कुंडली चार्ट
                    </div>
                    <div style="max-width:300px;margin:0 auto;">
                        ${json.kundali_svg}
                    </div>
                </div>
            `;
        }

        result.innerHTML = `
            <!-- Header -->
            <div class="rashi-detail-card" style="text-align:center;margin-bottom:16px;padding:16px;">
                <div style="font-size:32px;margin-bottom:6px;">🔮</div>
                <h2 style="margin:4px 0;">${json.name} की कुंडली</h2>
                <div style="font-size:13px;color:#a78bfa;margin-top:4px;">
                    📅 ${json.dob} &nbsp;|&nbsp; ⏰ ${json.tob}
                </div>
                <div style="font-size:13px;color:#94a3b8;">
                    📍 ${json.city}
                </div>
            </div>

            ${chartHTML}
            ${planetsHTML}

            <!-- Share button -->
            <button onclick="shareKundali('${json.name}', '${json.dob}', '${json.tob}', '${json.city}')"
                    class="btn-share"
                    style="width:100%;padding:12px;border-radius:12px;
                           font-size:14px;margin-bottom:8px;">
                📤 कुंडली WhatsApp पर शेयर करें
            </button>

            <!-- New Kundali button -->
            <button onclick="resetKundali()"
                    class="btn-copy"
                    style="width:100%;padding:12px;border-radius:12px;
                           font-size:13px;margin-bottom:16px;">
                🔄 नई कुंडली बनाएं
            </button>
        `;

    } catch (err) {
        result.innerHTML = '<div class="loading">❌ कुंडली नहीं बन सकी। पुनः प्रयास करें।</div>';
    }
}

function shareKundali(name, dob, tob, city) {
    const text = `🔮 ${name} की जन्म कुंडली

📅 जन्म तिथि: ${dob}
⏰ जन्म समय: ${tob}
📍 जन्म स्थान: ${city}

अपनी कुंडली देखें RozRashi App पर!
${APP_LINK}`;

    if (window.Android) {
        Android.shareText(text);
    } else if (navigator.share) {
        navigator.share({ text });
    } else {
        navigator.clipboard.writeText(text);
        showToast('✅ कुंडली जानकारी कॉपी हो गई!');
    }
}

function resetKundali() {
    document.getElementById('k-name').value = '';
    document.getElementById('k-dob').value  = '';
    document.getElementById('k-tob').value  = '';
    document.getElementById('k-city').value = '';
    document.getElementById('k-lat').value  = '';
    document.getElementById('k-lng').value  = '';
    document.getElementById('kundali-result').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== INIT APP =====
document.addEventListener('DOMContentLoaded', () => {
    setTodayDate();
    loadHome();
});

// ===== IMAGE CARD GENERATOR =====

const THEMES = [
    {
        name: "Purple",
        bg1: "#4c1d95", bg2: "#7c3aed",
        text: "#ffffff", sub: "rgba(255,255,255,0.75)"
    },
    {
        name: "Sunset",
        bg1: "#92400e", bg2: "#dc2626",
        text: "#ffffff", sub: "rgba(255,255,255,0.75)"
    },
    {
        name: "Ocean",
        bg1: "#1e3a5f", bg2: "#0369a1",
        text: "#ffffff", sub: "rgba(255,255,255,0.75)"
    },
    {
        name: "Forest",
        bg1: "#14532d", bg2: "#15803d",
        text: "#ffffff", sub: "rgba(255,255,255,0.75)"
    },
    {
        name: "Rose",
        bg1: "#881337", bg2: "#be185d",
        text: "#ffffff", sub: "rgba(255,255,255,0.75)"
    },
    {
        name: "Dark",
        bg1: "#111827", bg2: "#374151",
        text: "#ffd200", sub: "rgba(255,210,0,0.75)"
    },
];

let currentTheme = 0;
let currentStatusText = '';

// Open generator overlay
function openGenerator(text) {
    currentStatusText = text;
    currentTheme = 0;

    // Reset theme buttons
    document.querySelectorAll('.theme-btn').forEach(b =>
        b.classList.remove('selected'));
    document.querySelectorAll('.theme-btn')[0]
        .classList.add('selected');

    // Set text preview
    document.getElementById('generatorText').textContent = text;

    // Draw canvas
    drawStatusCard();

    // Show overlay
    document.getElementById('generatorOverlay')
        .classList.add('active');
}

// Close generator overlay
function closeGenerator() {
    document.getElementById('generatorOverlay')
        .classList.remove('active');
}

// Select theme
function selectTheme(index, btn) {
    currentTheme = index;
    document.querySelectorAll('.theme-btn')
        .forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    drawStatusCard();
}

// Draw canvas
function drawStatusCard() {
    const canvas = document.getElementById('statusCanvas');
    const ctx = canvas.getContext('2d');
    const W = 1080, H = 1080;
    const th = THEMES[currentTheme];

    // Background gradient
    const grad = ctx.createLinearGradient(0, 0, W, H);
    grad.addColorStop(0, th.bg1);
    grad.addColorStop(1, th.bg2);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // Decorative circles
    ctx.fillStyle = 'rgba(255,255,255,0.07)';
    ctx.beginPath();
    ctx.arc(W * 0.85, H * 0.15, 180, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(W * 0.1, H * 0.82, 140, 0, Math.PI * 2);
    ctx.fill();

    // Inner card
    ctx.fillStyle = 'rgba(255,255,255,0.05)';
    roundRect(ctx, 60, 60, W - 120, H - 120, 40);
    ctx.fill();

    // App name at top
    ctx.textAlign = 'center';
    ctx.font = 'bold 42px Hind, sans-serif';
    ctx.fillStyle = th.sub;
    ctx.fillText('🌟 RozRashi', W / 2, 160);

    // Divider line top
    ctx.strokeStyle = 'rgba(255,255,255,0.2)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(W / 2 - 160, 190);
    ctx.lineTo(W / 2 + 160, 190);
    ctx.stroke();

    // Main status text
    ctx.font = 'bold 58px Hind, sans-serif';
    ctx.fillStyle = th.text;
    drawWrappedText(ctx, currentStatusText, W / 2, 280, W - 200, 80);

    // Divider line bottom
    ctx.strokeStyle = 'rgba(255,255,255,0.2)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(W / 2 - 160, H - 200);
    ctx.lineTo(W / 2 + 160, H - 200);
    ctx.stroke();

    // Watermark at bottom
    ctx.font = '38px Hind, sans-serif';
    ctx.fillStyle = th.sub;
    ctx.fillText('📲 RozRashi App से', W / 2, H - 150);
    ctx.fillText('👉 bit.ly/rozrashi', W / 2, H - 95);
}

// Helper — draw wrapped Hindi text
function drawWrappedText(ctx, text, x, y, maxWidth, lineHeight) {
    const lines = text.split('\n');
    let currentY = y;
    lines.forEach(line => {
        const words = line.split(' ');
        let currentLine = '';
        words.forEach(word => {
            const testLine = currentLine ? currentLine + ' ' + word : word;
            if (ctx.measureText(testLine).width > maxWidth && currentLine) {
                ctx.fillText(currentLine, x, currentY);
                currentLine = word;
                currentY += lineHeight;
            } else {
                currentLine = testLine;
            }
        });
        if (currentLine) {
            ctx.fillText(currentLine, x, currentY);
            currentY += lineHeight;
        }
    });
}

// Helper — rounded rectangle
function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.arcTo(x + w, y, x + w, y + r, r);
    ctx.lineTo(x + w, y + h - r);
    ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
    ctx.lineTo(x + r, y + h);
    ctx.arcTo(x, y + h, x, y + h - r, r);
    ctx.lineTo(x, y + r);
    ctx.arcTo(x, y, x + r, y, r);
    ctx.closePath();
}

// Download image
function downloadImage() {
    const canvas = document.getElementById('statusCanvas');
    const small = document.createElement('canvas');
    small.width = 540;
    small.height = 540;
    small.getContext('2d').drawImage(canvas, 0, 0, 540, 540);
    const base64 = small.toDataURL('image/jpeg', 0.85).split(',')[1];

    closeGenerator();

    if (window.Android) {
        setTimeout(() => {
            Android.saveImage(base64);
        }, 400);
    } else {
        const link = document.createElement('a');
        link.download = 'rozrashi-status.jpg';
        link.href = 'data:image/jpeg;base64,' + base64;
        link.click();
        setTimeout(() => showToast('✅ Image Download हो रही है!'), 400);
    }
}

function shareImage() {
    const canvas = document.getElementById('statusCanvas');
    const small = document.createElement('canvas');
    small.width = 540;
    small.height = 540;
    small.getContext('2d').drawImage(canvas, 0, 0, 540, 540);

    const shareText = currentStatusText + APP_LINK;

    // ✅ Android WebView — use text share (WhatsApp ignores text when image attached)
    if (window.Android) {
        closeGenerator();
        setTimeout(() => {
            Android.shareText(shareText);
        }, 300);
        return;
    }

    // ✅ Web browser
    if (navigator.share) {
        navigator.share({ text: shareText })
            .then(() => closeGenerator())
            .catch(err => {
                if (err.name !== 'AbortError') {
                    navigator.clipboard.writeText(shareText)
                        .then(() => {
                            closeGenerator();
                            showToast('✅ कॉपी हो गया! WhatsApp पर पेस्ट करें');
                        });
                } else {
                    closeGenerator();
                }
            });
    } else {
        navigator.clipboard.writeText(shareText)
            .then(() => {
                closeGenerator();
                showToast('✅ कॉपी हो गया! WhatsApp पर पेस्ट करें');
            })
            .catch(() => {
                closeGenerator();
                const link = document.createElement('a');
                link.download = 'rozrashi-status.jpg';
                link.href = small.toDataURL('image/jpeg', 0.85);
                link.click();
                showToast('✅ Image Download हो रही है!');
            });
    }
}

// ===== BACK NAVIGATION HISTORY =====
const navHistory = [];

function pushHistory(screenName) {
    navHistory.push(screenName);
}

function handleBackPress() {
    if (navHistory.length > 0) {
        const previous = navHistory.pop();
        showScreen(previous);
        return true; // back handled
    }
    return false; // let app close
}

// Listen for Android back button via WebView
document.addEventListener('backbutton', function(e) {
    e.preventDefault();
    handleBackPress();
});

// For swipe back gesture (popstate)
window.addEventListener('popstate', function(e) {
    if (handleBackPress()) {
        history.pushState(null, '', window.location.href);
    }
});

// Push a dummy state so popstate fires on swipe
history.pushState(null, '', window.location.href);