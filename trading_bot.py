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

client = Groq(api_key=GROQ_API_KEY)

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """
أنت محلل اقتصادي متخصص في الأسواق المالية مع خبرة عميقة في الذهب XAUUSD و NAS100.

⚠️ قواعد صارمة:
- اكتب بالعربية الفصحى فقط — ممنوع أي حرف أجنبي
- لا تستخدم قد / ربما / من المحتمل
- اختر اتجاه واحد حاسم لكل أصل
- اربط دائماً: حدث → فائدة → دولار → أصل
- لا تتحدث عن أي أصل غير الذهب و NAS100

━━━━━━━━━━━━━━━━━━
📚 قاعدة المعرفة الاقتصادية:

🔗 العلاقات بين الأسواق:
- DXY يقوى → ذهب يهبط / NAS100 يهبط
- عائد السندات يرتفع → ذهب يهبط / NAS100 يهبط
- عائد السندات يهبط → ذهب يصعد / NAS100 يصعد
- Risk-On → NAS100 يصعد / ذهب يهبط
- Risk-Off → ذهب يصعد / NAS100 يهبط

💰 محركات الذهب بالترتيب:
1. العائد الحقيقي Real Yield = عائد السندات - التضخم
2. قوة الدولار DXY
3. توقعات الفيدرالي FED
4. التضخم
5. الجيوسياسية فقط إذا كانت أزمة حقيقية
6. مشتريات البنوك المركزية

📊 محركات NAS100 بالترتيب:
1. السيولة في الأسواق
2. توقعات الفائدة
3. أرباح شركات التكنولوجيا
4. نمو الاقتصاد GDP
5. مخاطرة المستثمرين

🏦 قرارات الفيدرالي:
- Hawkish → دولار يقوى → ذهب يهبط → NAS100 يهبط
- Dovish → دولار يضعف → ذهب يصعد → NAS100 يصعد
- Pause → NAS100 يصعد
- Pivot → ذهب يصعد قوياً / NAS100 يصعد قوياً
- المفاجأة أهم من القرار نفسه
- QE → ذهب يصعد / NAS100 يصعد
- QT → ذهب يهبط / NAS100 يهبط

📈 البيانات الاقتصادية:
- CPI فوق التوقعات → فيد يتشدد → ذهب يهبط / NAS100 يهبط
- CPI دون التوقعات → فيد يلين → ذهب يصعد / NAS100 يصعد
- NFP قوي فوق 200 ألف → دولار يقوى → ذهب يهبط
- NFP ضعيف → فيد يفكر في خفض → ذهب يصعد
- GDP سلبي ربعين = ركود → ذهب يصعد / NAS100 يهبط
- ISM فوق 50 = توسع → Risk-On
- ISM دون 50 = انكماش → Risk-Off

⚠️ الجيوسياسية:
- حرب فجائية → ذهب يصعد فوراً
- توترات USA-China → NAS100 يهبط
- أزمة مصرفية → ذهب يصعد / NAS100 يهبط بقوة

🧮 التحليل الكمي:
- رفع فائدة 25 نقطة = ذهب -0.5% إلى -1%
- CPI أعلى 0.2% = NAS100 -0.5% إلى -1.5%
- أزمة جيوسياسية = ذهب يصعد 1% إلى 3% فورياً

🔥 قاعدة العامل المسيطر:
إذا تعارضت العوامل → اختر العامل الأقوى تأثيراً فقط
"""

# ============ هيكل التقارير ============
MORNING_STRUCTURE = """اكتب تقرير الصباح:

📅 *تقرير الصباح — {date} — 08:00 المغرب* 🌅

━━━━━━━━━━━━━━━━━━
📌 *ملخص الليل والصباح*
🌏 آسيا: [أهم حدث + تأثيره]
🌍 أوروبا: [أهم حدث + تأثيره]
🌎 أمريكا: [ما ينتظر اليوم]

━━━━━━━━━━━━━━━━━━
🧠 *العامل المسيطر اليوم: {dominant}*
درجة الثقة: {confidence}%
حالة السوق: {regime}

━━━━━━━━━━━━━━━━━━
🔗 *سلسلة التأثير:*
الحدث → الفائدة → الدولار → الأصول

━━━━━━━━━━━━━━━━━━
💰 *الذهب XAUUSD*
• الاتجاه: [صعود / هبوط / محايد]
• السبب: [جملة حاسمة]
• المستويات: دعم ... / مقاومة ...

📊 *NAS100*
• الاتجاه: [صعود / هبوط / محايد]
• السبب: [جملة حاسمة]
• المستويات: دعم ... / مقاومة ...

━━━━━━━━━━━━━━━━━━
🔥 *البايز الصباحي*
💰 الذهب: [Bullish / Bearish / Neutral]
📊 NAS100: [Bullish / Bearish / Neutral]
⚡ تنبيه: [أهم حدث يجب مراقبته اليوم]"""

MIDDAY_STRUCTURE = """اكتب تقرير الظهر:

📅 *تقرير الظهر — {date} — 14:00 المغرب* ☀️

━━━━━━━━━━━━━━━━━━
📌 *ملخص الصباح*
[أهم ما حدث من الصباح حتى الآن]

📊 *البيانات الصادرة اليوم*
[الفعلي مقابل التوقعات → المفاجأة → رد فعل السوق]

━━━━━━━━━━━━━━━━━━
🧠 *العامل المسيطر الآن: {dominant}*
درجة الثقة: {confidence}%
حالة السوق: {regime}

━━━━━━━━━━━━━━━━━━
💰 *الذهب XAUUSD*
• الاتجاه المحدث: [صعود / هبوط / محايد]
• هل تغير عن الصباح؟ [نعم/لا + السبب]
• المستويات: دعم ... / مقاومة ...

📊 *NAS100*
• الاتجاه المحدث: [صعود / هبوط / محايد]
• هل تغير عن الصباح؟ [نعم/لا + السبب]
• المستويات: دعم ... / مقاومة ...

━━━━━━━━━━━━━━━━━━
📊 *السيناريوهات لبقية اليوم*
🟢 إذا حدث [X] → ذهب [Y] / NAS100 [Z]
🔴 إذا حدث [X] → ذهب [Y] / NAS100 [Z]

━━━━━━━━━━━━━━━━━━
🔥 *البايز الظهري*
💰 الذهب: [Bullish / Bearish / Neutral]
📊 NAS100: [Bullish / Bearish / Neutral]
⚡ القوة المسيطرة: [الدولار / الفيد / الجيوسياسية]"""

EVENING_STRUCTURE = """اكتب تقرير المساء:

📅 *تقرير المساء — {date} — 20:00 المغرب* 🌙

━━━━━━━━━━━━━━━━━━
📌 *ملخص اليوم الكامل*
[أهم 4 أحداث اليوم]

🏆 *أهم حدث اليوم:*
الحدث → الفائدة → الدولار → النتيجة

━━━━━━━━━━━━━━━━━━
🧠 *العامل المسيطر اليوم: {dominant}*
درجة الثقة: {confidence}%
حالة السوق: {regime}

━━━━━━━━━━━━━━━━━━
💰 *تحليل الذهب اليومي*
• أداء اليوم: [صعد / هبط / ثبت]
• السبب: [جملة حاسمة]
• البايز للغد: [Bullish / Bearish / Neutral]
• المستويات غداً: دعم ... / مقاومة ...

📊 *تحليل NAS100 اليومي*
• أداء اليوم: [صعد / هبط / ثبت]
• السبب: [جملة حاسمة]
• البايز للغد: [Bullish / Bearish / Neutral]
• المستويات غداً: دعم ... / مقاومة ...

━━━━━━━━━━━━━━━━━━
📊 *السيناريوهات للغد*
🟢 المتفائل: [الشرط + النتيجة]
🟡 الأساسي: [الشرط + النتيجة]
🔴 المتشائم: [الشرط + النتيجة]

━━━━━━━━━━━━━━━━━━
🎯 *الخلاصة النهائية*
• الذهب: [صعود / هبوط / محايد]
• NAS100: [صعود / هبوط / محايد]
• حالة السوق: [Risk-On / Risk-Off / Mixed]
• القوة المسيطرة: [الدولار / الفيد / الجيوسياسية]
• أهم حدث غداً: [حدث واحد محدد]"""

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
    if any(x in text for x in ["qe", "qt", "liquidity"]):
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
    send_telegram("⏳ *جاري اعداد التقرير...*\nيبحث البوت في الاخبار العالمية 🔄")

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
        structure = MORNING_STRUCTURE.format(date=date, dominant=dominant, confidence=confidence, regime=regime)
    elif hour < 17:
        structure = MIDDAY_STRUCTURE.format(date=date, dominant=dominant, confidence=confidence, regime=regime)
    else:
        structure = EVENING_STRUCTURE.format(date=date, dominant=dominant, confidence=confidence, regime=regime)

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""الاخبار العالمية اليوم:
{news_text}

{structure}

تذكر: اكتب باللغة العربية الفصحى فقط — ممنوع اي حرف اجنبي."""}
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
{news_context}

العامل المسيطر: {dominant}
درجة الثقة: {confidence}%
حالة السوق: {regime}

اجب باللغة العربية الفصحى فقط:

📰 *الموضوع:*
[شرح بسيط في جملتين]

🧠 *التحليل:*
الحدث → الفائدة → الدولار → الذهب و NAS100

💰 *الذهب:* [الاتجاه + السبب]
📊 *NAS100:* [الاتجاه + السبب]

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
                        "✅ تقرير الصباح: 08:00 🌅\n"
                        "✅ تقرير الظهر: 14:00 ☀️\n"
                        "✅ تقرير المساء: 20:00 🌙\n\n"
                        "/report — تقرير فوري\n"
                        "/help — المساعدة\n\n"
                        "او اكتب اي سؤال اقتصادي 👇", chat_id)
                elif text == "/report":
                    send_telegram("⏳ *جاري اعداد تقرير...*", chat_id)
                    threading.Thread(target=daily_report).start()
                elif text == "/help":
                    send_telegram(
                        "📖 *كيفية الاستخدام:*\n\n"
                        "اكتب اي سؤال مثل:\n"
                        "• ما تاثير رفع الفائدة على الذهب؟\n"
                        "• هل NAS100 صاعد اليوم؟\n"
                        "• ماذا يعني ارتفاع CPI؟\n\n"
                        "/report — تقرير فوري شامل", chat_id)
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
        "✅ تقرير الصباح: 08:00 🌅\n"
        "✅ تقرير الظهر: 14:00 ☀️\n"
        "✅ تقرير المساء: 20:00 🌙\n\n"
        "اكتب /report لتقرير فوري 👇"
    )
    scheduler_thread = threading.Thread(target=schedule_jobs, daemon=True)
    scheduler_thread.start()
    telegram_polling()
