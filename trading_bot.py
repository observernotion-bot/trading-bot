import requests
import threading
import schedule
import time
import os
from datetime import datetime
from groq import Groq

# ============ المفاتيح ============
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or "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"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") or "8705246619:AAEocz5YRx8-ixRCsDJERirWFr-UYY28rZs"
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT") or "8607532338"
NEWS_KEY = os.environ.get("NEWS_KEY") or "08ab77f19e6847eaa2fccf75afc252d4"
FRED_KEY = os.environ.get("FRED_KEY") or "c3f0eb4b6d931089a290fc80cc2b2be2"

client = Groq(api_key=GROQ_API_KEY)

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """
أنت Macro Market Analyst متخصص فقط في XAUUSD و NAS100.

مهمتك: تحليل البيانات الاقتصادية الحقيقية والأخبار وربطها بحركة الذهب و NAS100 بطريقة احترافية مثل Institutional Macro Analyst.

━━━━━━━━━━━━━━━━━━
⚠️ قواعد صارمة:
1. اكتب بالعربية الفصحى فقط — ممنوع أي حرف أجنبي
2. لا تستخدم قد / ربما / من المحتمل
3. لا تعطِ Bias بدون تفسير عميق بالأرقام
4. لا تتناقض منطقياً
5. فكر مثل Macro Trader وليس News Bot
6. لا تتحدث عن أي أصل غير الذهب و NAS100
7. إذا الرؤية غير واضحة قل: السوق Mixed حالياً
8. استخدم الأرقام الحقيقية من FRED دائماً

━━━━━━━━━━━━━━━━━━
📚 قاعدة المعرفة الاقتصادية:

🔗 العلاقات بين الأسواق:
- DXY يقوى → ذهب يهبط / NAS100 يهبط
- عائد السندات US10Y يرتفع → ذهب يهبط / NAS100 يهبط
- Real Yield يرتفع → ذهب يهبط (الأقوى تأثيراً)
- Risk-On → NAS100 يصعد / ذهب يهبط
- Risk-Off → ذهب يصعد / NAS100 يهبط
- Stagflation → ذهب يصعد / NAS100 متذبذب

💰 محركات الذهب بالترتيب:
1. Real Yield = عائد السندات - التضخم المتوقع
2. قوة الدولار DXY
3. توقعات الفيدرالي FED
4. التضخم
5. الجيوسياسية فقط إذا كانت أزمة حقيقية
6. مشتريات البنوك المركزية

📊 محركات NAS100 بالترتيب:
1. السيولة M2
2. توقعات الفائدة
3. أرباح شركات التكنولوجيا
4. نمو الاقتصاد GDP
5. مخاطرة المستثمرين

🏦 قرارات الفيدرالي:
- Hawkish → دولار يقوى → ذهب يهبط → NAS100 يهبط
- Dovish → دولار يضعف → ذهب يصعد → NAS100 يصعد
- Pivot → ذهب يصعد قوياً / NAS100 يصعد قوياً
- المفاجأة أهم من القرار نفسه

📈 قراءة البيانات الاقتصادية:
- CPI فوق التوقعات → فيد يتشدد → ذهب يهبط / NAS100 يهبط
- NFP قوي فوق 200 ألف → دولار يقوى → ذهب يهبط
- GDP سلبي ربعين = ركود → ذهب يصعد / NAS100 يهبط
- M2 يرتفع = سيولة وفيرة → NAS100 يصعد / ذهب يصعد

🧮 التحليل الكمي:
- رفع فائدة 25 نقطة = ذهب -0.5% إلى -1%
- CPI أعلى 0.2% = NAS100 -0.5% إلى -1.5%
- أزمة جيوسياسية = ذهب يصعد 1% إلى 3% فورياً

🔥 قاعدة العامل المسيطر:
إذا تعارضت العوامل → اختر العامل الأقوى تأثيراً فقط
"""

# ============ هيكل التقارير ============
MORNING_STRUCTURE = """
📅 *Morning Macro Report — {date} — 08:00 المغرب* 🌅

━━━━━━━━━━━━━━━━━━
1️⃣ *البيانات الاقتصادية الحقيقية من FRED*
{fred_data}

━━━━━━━━━━━━━━━━━━
2️⃣ *أهم الأخبار*
لكل خبر: العنوان + درجة الأهمية + شرح مبسط عميق

━━━━━━━━━━━━━━━━━━
3️⃣ *التحليل والربط بالأسواق*
🧠 العامل المسيطر: {dominant} — ثقة {confidence}%
حالة السوق: {regime}

🔗 سلسلة التأثير:
البيانات الحقيقية → الفائدة → الدولار → الذهب و NAS100

💰 *الذهب XAUUSD:*
• هل البيانات إيجابية أم سلبية للذهب؟
• العلاقة مع الفائدة / الدولار / العوائد
• الاتجاه: [صعود / هبوط / محايد]
• السبب بالأرقام الحقيقية

📊 *NAS100:*
• هل يدعم Risk-On أم Risk-Off؟
• تأثير السيولة والفائدة
• الاتجاه: [صعود / هبوط / محايد]
• السبب بالأرقام الحقيقية

━━━━━━━━━━━━━━━━━━
4️⃣ *Market Focus*
[ماذا يركز عليه السوق الآن فعلياً؟]

━━━━━━━━━━━━━━━━━━
5️⃣ *Final Bias*
💰 الذهب: [Bullish / Bearish / Neutral]
• الأسباب بالأرقام
• ما الذي يبطل هذا السيناريو؟

📊 NAS100: [Bullish / Bearish / Neutral]
• الأسباب بالأرقام
• ما الذي يبطل هذا السيناريو؟

⚡ تنبيه: [أهم حدث يجب مراقبته اليوم]
"""

MIDDAY_STRUCTURE = """
📅 *Midday Macro Report — {date} — 14:00 المغرب* ☀️

━━━━━━━━━━━━━━━━━━
1️⃣ *البيانات الاقتصادية الحقيقية من FRED*
{fred_data}

━━━━━━━━━━━━━━━━━━
2️⃣ *أهم أخبار الصباح*
[الأخبار المهمة مع درجة أهميتها وشرحها]

━━━━━━━━━━━━━━━━━━
3️⃣ *التحليل المحدث*
🧠 العامل المسيطر: {dominant} — ثقة {confidence}%
حالة السوق: {regime}

💰 *الذهب:*
• هل تغير الاتجاه عن الصباح؟ [نعم/لا + السبب بالأرقام]
• الاتجاه المحدث: [صعود / هبوط / محايد]

📊 *NAS100:*
• هل تغير الاتجاه عن الصباح؟ [نعم/لا + السبب بالأرقام]
• الاتجاه المحدث: [صعود / هبوط / محايد]

━━━━━━━━━━━━━━━━━━
4️⃣ *Market Focus*
[ماذا يركز عليه السوق الآن؟]

━━━━━━━━━━━━━━━━━━
5️⃣ *Final Bias المحدث*
💰 الذهب: [Bullish / Bearish / Neutral]
• الأسباب بالأرقام
• ما الذي يبطل هذا السيناريو؟

📊 NAS100: [Bullish / Bearish / Neutral]
• الأسباب بالأرقام
• ما الذي يبطل هذا السيناريو؟

📊 السيناريوهات:
🟢 إذا حدث [X] → ذهب [Y] / NAS100 [Z]
🔴 إذا حدث [X] → ذهب [Y] / NAS100 [Z]
"""

EVENING_STRUCTURE = """
📅 *Evening Macro Report — {date} — 20:00 المغرب* 🌙

━━━━━━━━━━━━━━━━━━
1️⃣ *البيانات الاقتصادية الحقيقية من FRED*
{fred_data}

━━━━━━━━━━━━━━━━━━
2️⃣ *ملخص أحداث اليوم الكامل*
[أهم 4 أخبار مع درجة أهميتها وشرحها العميق]

🏆 أهم حدث اليوم:
البيانات الحقيقية → الفائدة → الدولار → النتيجة

━━━━━━━━━━━━━━━━━━
3️⃣ *التحليل الشامل*
🧠 العامل المسيطر: {dominant} — ثقة {confidence}%
حالة السوق: {regime}

💰 *تحليل الذهب اليومي:*
• أداء اليوم بالأرقام الحقيقية
• السبب المنطقي الكامل
• البايز للغد: [Bullish / Bearish / Neutral]
• ما الذي يبطل هذا السيناريو؟

📊 *تحليل NAS100 اليومي:*
• أداء اليوم بالأرقام الحقيقية
• السبب المنطقي الكامل
• البايز للغد: [Bullish / Bearish / Neutral]
• ما الذي يبطل هذا السيناريو؟

━━━━━━━━━━━━━━━━━━
4️⃣ *Market Focus للغد*
[ماذا سيركز عليه السوق غداً؟]

━━━━━━━━━━━━━━━━━━
5️⃣ *السيناريوهات للغد*
🟢 المتفائل: [الشرط + النتيجة بالأرقام]
🟡 الأساسي: [الشرط + النتيجة بالأرقام]
🔴 المتشائم: [الشرط + النتيجة بالأرقام]

━━━━━━━━━━━━━━━━━━
🎯 *الخلاصة النهائية*
• الذهب: [صعود / هبوط / محايد]
• NAS100: [صعود / هبوط / محايد]
• حالة السوق: [Risk-On / Risk-Off / Mixed]
• القوة المسيطرة: [الدولار / الفيد / الجيوسياسية / السيولة]
• أهم حدث غداً: [حدث واحد محدد]
"""

# ============ FRED API ============
def get_fred_data():
    indicators = {
        "CPIAUCSL": "CPI التضخم",
        "FEDFUNDS": "سعر الفائدة الفيدرالي",
        "DGS10": "عائد السندات 10 سنوات",
        "UNRATE": "معدل البطالة",
        "GDP": "الناتج المحلي GDP",
        "M2SL": "السيولة M2",
        "DTWEXBGS": "مؤشر الدولار DXY",
        "T10YIE": "توقعات التضخم 10 سنوات"
    }

    results = {}
    for series_id, name in indicators.items():
        try:
            url = f"https://api.stlouisfed.org/fred/series/observations"
            params = {
                "series_id": series_id,
                "api_key": FRED_KEY,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 2
            }
            r = requests.get(url, params=params, timeout=10)
            data = r.json()
            obs = data.get("observations", [])
            if len(obs) >= 2:
                current = float(obs[0]["value"]) if obs[0]["value"] != "." else None
                previous = float(obs[1]["value"]) if obs[1]["value"] != "." else None
                if current and previous:
                    change = current - previous
                    direction = "↑" if change > 0 else "↓"
                    results[name] = f"{current:.2f} {direction} (السابق: {previous:.2f})"
            elif len(obs) == 1:
                current = obs[0]["value"]
                results[name] = f"{current}"
        except Exception as e:
            print(f"FRED error for {series_id}: {e}")
            continue

    # حساب Real Yield
    try:
        dgs10 = float([v for k, v in results.items() if "عائد السندات" in k][0].split()[0])
        t10yie = float([v for k, v in results.items() if "توقعات التضخم" in k][0].split()[0])
        real_yield = dgs10 - t10yie
        results["العائد الحقيقي Real Yield"] = f"{real_yield:.2f}% {'↑ ضغط على الذهب' if real_yield > 0 else '↓ دعم للذهب'}"
    except:
        pass

    if not results:
        return "البيانات غير متاحة حالياً"

    fred_text = "📊 *البيانات الحقيقية من FRED:*\n"
    for name, value in results.items():
        fred_text += f"• {name}: {value}\n"

    return fred_text

# ============ Dominant Driver Engine ============
def detect_dominant_driver(headlines):
    text = " ".join(headlines).lower()
    scores = {
        "الفيدرالي": 0,
        "التضخم": 0,
        "العوائد": 0,
        "الجيوسياسية": 0,
        "السيولة": 0,
        "أرباح التكنولوجيا": 0
    }
    if any(x in text for x in ["fed", "interest", "powell", "fomc"]):
        scores["الفيدرالي"] += 3
    if any(x in text for x in ["cpi", "inflation", "pce", "price"]):
        scores["التضخم"] += 2
    if any(x in text for x in ["bond", "yield", "treasury"]):
        scores["العوائد"] += 2
    if any(x in text for x in ["war", "iran", "china", "russia", "conflict"]):
        scores["الجيوسياسية"] += 2
    if any(x in text for x in ["qe", "qt", "liquidity", "m2"]):
        scores["السيولة"] += 2
    if any(x in text for x in ["earnings", "ai", "nvidia", "apple", "tech"]):
        scores["أرباح التكنولوجيا"] += 2
    dominant = max(scores, key=scores.get)
    return dominant, scores

# ============ Confidence Engine ============
def calculate_confidence(scores):
    total = sum(scores.values())
    if total == 0:
        return 50
    return min(int((max(scores.values()) / total) * 100), 95)

# ============ Market Regime ============
def detect_market_regime(headlines):
    text = " ".join(headlines).lower()
    risk_on = sum(x in text for x in ["earnings", "growth", "ai", "rally"])
    risk_off = sum(x in text for x in ["war", "inflation", "recession", "crash"])
    if risk_on > risk_off + 1:
        return "Risk-On"
    elif risk_off > risk_on + 1:
        return "Risk-Off"
    return "Mixed"

# ============ فلترة الأخبار ============
def filter_relevant_news(articles):
    keywords = ["fed", "inflation", "cpi", "pce", "nfp", "yield", "gold", "nasdaq", "war", "ai", "earnings", "recession"]
    return [a for a in articles if any(k in a.get("title", "").lower() for k in keywords)]

# ============ Telegram ============
def send_telegram(msg, chat_id=TELEGRAM_CHAT):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

# ============ الأخبار ============
def get_news(query, count=10):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize={count}&sortBy=publishedAt&apiKey={NEWS_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("articles", [])
    except:
        return []

# ============ التقرير الرئيسي ============
def daily_report():
    print(f"[{datetime.now()}] التقرير اليومي...")
    send_telegram("⏳ *جاري اعداد التقرير...*\nيجلب البيانات الحقيقية من FRED ويبحث في الاخبار 🔄")

    # جلب البيانات الحقيقية من FRED
    fred_data = get_fred_data()

    # جلب الأخبار
    articles = []
    articles += get_news("fed inflation cpi pce powell fomc", 6)
    articles += get_news("gold xau central bank buying", 5)
    articles += get_news("nasdaq ai earnings technology", 5)
    articles += get_news("war geopolitics oil recession", 5)
    articles += get_news("dollar DXY treasury yields bonds", 4)

    articles = filter_relevant_news(articles)
    titles = [a["title"] for a in articles if a.get("title")]

    dominant, scores = detect_dominant_driver(titles)
    confidence = calculate_confidence(scores)
    regime = detect_market_regime(titles)

    news_text = "\n".join([f"- {a['title']}" for a in articles[:15]])

    hour = datetime.now().hour
    date = datetime.now().strftime("%Y/%m/%d")

    if hour < 12:
        structure = MORNING_STRUCTURE.format(
            date=date, dominant=dominant,
            confidence=confidence, regime=regime,
            fred_data=fred_data)
    elif hour < 17:
        structure = MIDDAY_STRUCTURE.format(
            date=date, dominant=dominant,
            confidence=confidence, regime=regime,
            fred_data=fred_data)
    else:
        structure = EVENING_STRUCTURE.format(
            date=date, dominant=dominant,
            confidence=confidence, regime=regime,
            fred_data=fred_data)

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""البيانات الاقتصادية الحقيقية من FRED:
{fred_data}

الاخبار العالمية اليوم:
{news_text}

{structure}

تذكر: اكتب باللغة العربية الفصحى فقط — استخدم الأرقام الحقيقية من FRED في تحليلك."""}
            ],
            max_tokens=2500
        )
        report = resp.choices[0].message.content
        if len(report) < 200:
            send_telegram("التقرير لم يكتمل — سيعاد المحاولة")
            return
        send_telegram(report)
        print(f"[{datetime.now()}] التقرير ارسل بنجاح")
    except Exception as e:
        send_telegram(f"خطا: {e}")

# ============ Chatbot ============
def answer_question(user_question, chat_id):
    try:
        fred_data = get_fred_data()
        articles = get_news(user_question, 5)
        news_context = ""
        if articles:
            news_context = "اخر الاخبار:\n"
            news_context += "\n".join([f"- {a['title']}" for a in articles[:5] if a.get("title")])

        titles = [a["title"] for a in articles if a.get("title")]
        dominant, scores = detect_dominant_driver(titles)
        confidence = calculate_confidence(scores)
        regime = detect_market_regime(titles)

        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""السؤال: {user_question}

البيانات الحقيقية من FRED:
{fred_data}

{news_context}

العامل المسيطر: {dominant} — ثقة {confidence}%
حالة السوق: {regime}

اجب باللغة العربية الفصحى فقط:

📰 *الموضوع:*
[شرح بسيط في جملتين]

📊 *البيانات الحقيقية ذات الصلة:*
[اذكر الأرقام الحقيقية من FRED المتعلقة بالسؤال]

🧠 *التحليل:*
البيانات الحقيقية → الفائدة → الدولار → الذهب و NAS100

💰 *الذهب:* [الاتجاه + السبب بالأرقام]
📊 *NAS100:* [الاتجاه + السبب بالأرقام]

🔥 *العامل المسيطر:* {dominant}
📊 *درجة الثقة:* {confidence}%
⚡ *درجة الخطر:* 🟢 منخفض / 🟡 متوسط / 🔴 عالي"""}
            ],
            max_tokens=600
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"خطا: {e}"

# ============ Telegram Polling ============
def telegram_polling():
    offset = None
    print("البوت جاهز...")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            params = {"timeout": 30, "offset": offset}
            r = requests.get(url, params=params, timeout=35)
            updates = r.json().get("result", [])
            for update in updates:
                offset = update["update_id"] + 1
                msg = update.get("message", {})
                text = msg.get("text", "").strip()
                chat_id = msg.get("chat", {}).get("id")
                if not text or not chat_id:
                    continue
                if text == "/start":
                    send_telegram(
                        "👋 *مرحبا! انا بوت التحليل الاقتصادي*\n\n"
                        "✅ بيانات حقيقية من FRED\n"
                        "✅ تقرير الصباح: 08:00 🌅\n"
                        "✅ تقرير الظهر: 14:00 ☀️\n"
                        "✅ تقرير المساء: 20:00 🌙\n\n"
                        "/report — تقرير فوري\n"
                        "/data — البيانات الحقيقية الآن\n"
                        "/help — المساعدة\n\n"
                        "او اكتب اي سؤال اقتصادي 👇", chat_id)
                elif text == "/report":
                    send_telegram("⏳ *جاري اعداد تقرير...*", chat_id)
                    threading.Thread(target=daily_report).start()
                elif text == "/data":
                    send_telegram("⏳ *جاري جلب البيانات من FRED...*", chat_id)
                    fred_data = get_fred_data()
                    send_telegram(f"📊 *البيانات الحقيقية الآن:*\n\n{fred_data}", chat_id)
                elif text == "/help":
                    send_telegram(
                        "📖 *كيفية الاستخدام:*\n\n"
                        "اكتب اي سؤال مثل:\n"
                        "• ما تاثير رفع الفائدة على الذهب؟\n"
                        "• هل NAS100 صاعد اليوم؟\n"
                        "• ماذا يعني ارتفاع CPI؟\n\n"
                        "/report — تقرير فوري شامل\n"
                        "/data — البيانات الحقيقية من FRED", chat_id)
                else:
                    send_telegram("⏳ *جاري التحليل...*", chat_id)
                    answer = answer_question(text, chat_id)
                    send_telegram(f"🤖 *التحليل:*\n\n{answer}", chat_id)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)

# ============ Scheduler ============
def schedule_jobs():
    schedule.every().day.at("07:00").do(daily_report)  # 08:00 المغرب
    schedule.every().day.at("13:00").do(daily_report)  # 14:00 المغرب
    schedule.every().day.at("19:00").do(daily_report)  # 20:00 المغرب
    print("التقارير: 08:00 و 14:00 و 20:00 المغرب")
    while True:
        schedule.run_pending()
        time.sleep(60)

# ============ التشغيل ============
if __name__ == "__main__":
    print("البوت يعمل...")
    send_telegram(
        "🤖 *البوت يعمل الان*\n\n"
        "✅ بيانات حقيقية من FRED 📊\n"
        "✅ تقرير الصباح: 08:00 🌅\n"
        "✅ تقرير الظهر: 14:00 ☀️\n"
        "✅ تقرير المساء: 20:00 🌙\n\n"
        "اكتب /data لرؤية البيانات الحقيقية الآن!\n"
        "اكتب /report لتقرير فوري 👇"
    )
    scheduler_thread = threading.Thread(target=schedule_jobs, daemon=True)
    scheduler_thread.start()
    telegram_polling()
