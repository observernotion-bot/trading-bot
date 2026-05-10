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

# ============ المعرفة الاقتصادية ============
SYSTEM_PROMPT = """
أنت محلل اقتصادي متخصص في الأسواق المالية مع خبرة عميقة في الذهب XAUUSD و NAS100.

━━━━━━━━━━━━━━━━━━
📚 قاعدة المعرفة الاقتصادية الكاملة:

🔗 1. العلاقات بين الأسواق:
- دولار DXY يقوى → ذهب يهبط (علاقة عكسية قوية جداً)
- عائد السندات US10Y يرتفع → ذهب يهبط / NAS100 يهبط
- عائد السندات يهبط → ذهب يصعد / NAS100 يصعد
- S&P500 يصعد مع دولار يضعف = Risk-On حقيقي
- البنوك المركزية تشتري الذهب = دعم هيكلي طويل المدى
- منحنى العائد مقلوب = إشارة ركود قادم

💰 2. محركات الذهب بالترتيب:
1. العائد الحقيقي Real Yield = عائد السندات - التضخم المتوقع
   → Real Yield يرتفع = ذهب يهبط
   → Real Yield يهبط = ذهب يصعد
2. قوة الدولار DXY
3. توقعات الفيدرالي FED
4. التضخم Inflation Expectations
5. الجيوسياسية فقط إذا كانت أزمة حقيقية
6. مشتريات البنوك المركزية
7. طلب المستثمرين على صناديق الذهب ETF

📊 3. محركات NAS100 بالترتيب:
1. السيولة في الأسواق Liquidity
2. توقعات الفائدة الحقيقية
3. أرباح شركات التكنولوجيا الكبرى
4. نمو الاقتصاد الأمريكي GDP
5. مخاطرة المستثمرين Risk Appetite
6. تأثير الذكاء الاصطناعي AI

🏦 4. قراءة قرارات الفيدرالي FED:
- Hawkish = يريد رفع الفائدة → دولار يقوى → ذهب يهبط → NAS100 يهبط
- Dovish = يريد خفض الفائدة → دولار يضعف → ذهب يصعد → NAS100 يصعد
- Pause = يوقف الرفع → السوق يتفاءل → NAS100 يصعد
- Pivot = يبدأ دورة خفض → ذهب يصعد قوياً → NAS100 يصعد قوياً
- المفاجأة أهم من القرار نفسه
- QE = ضخ سيولة → ذهب يصعد / NAS100 يصعد
- QT = سحب سيولة → ذهب يهبط / NAS100 يهبط

📈 5. قراءة البيانات الاقتصادية:
CPI: فوق التوقعات → فيد يتشدد → ذهب يهبط / NAS100 يهبط
PCE: مرتفع → فيد يتشدد أكثر / منخفض → فيد يخفض قريباً
NFP: قوي فوق 200 ألف → دولار يقوى → ذهب يهبط
GDP: سلبي ربعين = ركود → Risk-Off → ذهب يصعد / NAS100 يهبط
ISM: فوق 50 = توسع → Risk-On / دون 50 = انكماش → Risk-Off
البطالة: ترتفع بسرعة → فيد يخفض → ذهب يصعد

⚠️ 6. الجيوسياسية:
- حرب فجائية → ذهب يصعد فوراً
- أزمة رفعت النفط → تضخم → فيد يتشدد → ذهب يتراجع لاحقاً
- توترات USA-China → NAS100 يهبط
- أزمة مصرفية → ذهب يصعد قوياً / NAS100 يهبط بقوة
- ضغط سياسي على الفيد → ذهب يصعد
- حرب عملات → ذهب يصعد

🔄 7. دورة الاقتصاد:
- توسع → Risk-On → NAS100 يصعد / ذهب محايد
- ذروة → تضخم → فيد يرفع → NAS100 يتراجع / ذهب يصعد
- انكماش → ركود → Risk-Off → ذهب يصعد / NAS100 يهبط
- انتعاش → فيد يخفض → NAS100 يصعد قوياً

💡 8. Risk-On vs Risk-Off:
Risk-On: NAS100 يصعد / ذهب يهبط / دولار يضعف
Risk-Off: ذهب يصعد / NAS100 يهبط / دولار يقوى
Mixed Stagflation: ذهب يصعد / NAS100 متذبذب

🧮 9. التحليل الكمي:
- رفع فائدة 25 نقطة = ذهب -0.5% إلى -1%
- CPI أعلى 0.2% من التوقعات = NAS100 -0.5% إلى -1.5%
- NFP أعلى 100 ألف من التوقعات = دولار يقوى 0.3% إلى 0.5%
- أزمة جيوسياسية مفاجئة = ذهب يصعد 1% إلى 3% فورياً

🏛 10. البنوك المركزية العالمية:
- FED = الأهم عالمياً
- ECB = يؤثر على اليورو والدولار
- BOJ = سياسة فائدة سلبية تؤثر على تدفق الأموال
- PBoC = مشترٍ رئيسي للذهب
- البنوك المركزية اشترت أكثر من 1000 طن ذهب سنوياً منذ 2022

━━━━━━━━━━━━━━━━━━
⚠️ قواعد التحليل الصارمة:
1. اكتب باللغة العربية الفصحى فقط — ممنوع أي حرف أجنبي
2. لا تقل قد / ربما / من المحتمل — كن حاسماً
3. دائماً اشرح السلسلة: الحدث → الفائدة → الدولار → الأصول
4. لا تتحدث عن أصول غير الذهب و NAS100
5. استخدم الأرقام والنسب عند الإمكان
6. المفاجأة أهم من الرقم نفسه
"""

# ============ هيكل التقارير ============
MORNING_STRUCTURE = """اكتب تقرير الصباح بهذا الهيكل:

📅 *تقرير الصباح — {date} — 08:00 المغرب* 🌅

━━━━━━━━━━━━━━━━━━
📌 *ملخص الليل والصباح الباكر*
🌏 آسيا: [أهم حدث + تأثيره]
🌍 أوروبا: [أهم حدث + تأثيره]
🌎 أمريكا: [ما ينتظر اليوم من بيانات]

━━━━━━━━━━━━━━━━━━
🏦 *البنوك المركزية والسياسة النقدية*
[أي تصريحات أو قرارات خلال الليل]

⚠️ *الجيوسياسية*
[أهم التوترات الحالية وتأثيرها]

━━━━━━━━━━━━━━━━━━
🧠 *التحليل والمنطق الاقتصادي*
الأحداث → الفائدة → الدولار → النتيجة

━━━━━━━━━━━━━━━━━━
💰 *الذهب XAUUSD*
• الاتجاه: [صعود / هبوط / محايد]
• السبب الرئيسي: [جملة حاسمة]
• المستويات: دعم ... / مقاومة ...
• مدة التأثير: [ساعات / أيام]

📊 *NAS100*
• الاتجاه: [صعود / هبوط / محايد]
• السبب الرئيسي: [جملة حاسمة]
• المستويات: دعم ... / مقاومة ...
• مدة التأثير: [ساعات / أيام]

━━━━━━━━━━━━━━━━━━
🔥 *البايز الصباحي*
💰 الذهب: [Bullish / Bearish / Neutral]
📊 NAS100: [Bullish / Bearish / Neutral]
🌡 حالة السوق: [Risk-On / Risk-Off / Mixed]
⚡ تنبيه الصباح: [أهم حدث يجب مراقبته اليوم]"""

MIDDAY_STRUCTURE = """اكتب تقرير الظهر بهذا الهيكل:

📅 *تقرير الظهر — {date} — 14:00 المغرب* ☀️

━━━━━━━━━━━━━━━━━━
📌 *ملخص الصباح*
[أهم ما حدث من الصباح حتى الآن]

📊 *البيانات الاقتصادية الصادرة اليوم*
[CPI / NFP / GDP مع التوقعات والنتائج الفعلية]

━━━━━━━━━━━━━━━━━━
🧠 *التحليل العميق*
البيانات الفعلية مقابل التوقعات → المفاجأة → رد فعل السوق

━━━━━━━━━━━━━━━━━━
💰 *الذهب XAUUSD*
• الاتجاه المحدث: [صعود / هبوط / محايد]
• هل تغير الاتجاه عن الصباح؟ [نعم/لا + السبب]
• المستويات: دعم ... / مقاومة ...

📊 *NAS100*
• الاتجاه المحدث: [صعود / هبوط / محايد]
• هل تغير الاتجاه عن الصباح؟ [نعم/لا + السبب]
• المستويات: دعم ... / مقاومة ...

━━━━━━━━━━━━━━━━━━
📊 *السيناريوهات لبقية اليوم*
🟢 إذا حدث [X] → الذهب [Y] / NAS100 [Z]
🔴 إذا حدث [X] → الذهب [Y] / NAS100 [Z]

━━━━━━━━━━━━━━━━━━
🔥 *البايز الظهري المحدث*
💰 الذهب: [Bullish / Bearish / Neutral]
📊 NAS100: [Bullish / Bearish / Neutral]
🌡 حالة السوق: [Risk-On / Risk-Off / Mixed]
⚡ القوة المسيطرة: [الدولار / الفيد / الجيوسياسية / السيولة]"""

EVENING_STRUCTURE = """اكتب تقرير المساء بهذا الهيكل:

📅 *تقرير المساء — {date} — 20:00 المغرب* 🌙

━━━━━━━━━━━━━━━━━━
📌 *ملخص اليوم الكامل*
[أهم 4 أحداث اقتصادية وجيوسياسية اليوم]

🏆 أهم حدث اليوم:
الحدث → الفائدة → الدولار → النتيجة

━━━━━━━━━━━━━━━━━━
🧠 *التحليل الشامل لليوم*
[ربط كل أحداث اليوم وشرح الصورة الكاملة]

━━━━━━━━━━━━━━━━━━
💰 *تحليل الذهب اليومي*
• أداء اليوم: [صعد / هبط / ثبت]
• السبب الرئيسي: [جملة حاسمة]
• البايز للغد: [Bullish / Bearish / Neutral]
• المستويات غداً: دعم ... / مقاومة ...

📊 *تحليل NAS100 اليومي*
• أداء اليوم: [صعد / هبط / ثبت]
• السبب الرئيسي: [جملة حاسمة]
• البايز للغد: [Bullish / Bearish / Neutral]
• المستويات غداً: دعم ... / مقاومة ...

━━━━━━━━━━━━━━━━━━
📊 *السيناريوهات للغد*
🟢 المتفائل: الشرط [X] → الذهب [Y] / NAS100 [Z]
🟡 الأساسي الأرجح: الشرط [X] → الذهب [Y] / NAS100 [Z]
🔴 المتشائم: الشرط [X] → الذهب [Y] / NAS100 [Z]

━━━━━━━━━━━━━━━━━━
🎯 *الخلاصة النهائية ليوم غد*
• اتجاه الذهب: [صعود / هبوط / محايد]
• اتجاه NAS100: [صعود / هبوط / محايد]
• حالة السوق: [Risk-On / Risk-Off / Mixed]
• القوة المسيطرة: [الدولار / الفيد / الجيوسياسية / السيولة]
• أهم حدث غداً: [حدث واحد محدد]"""

# ============ الدوال الأساسية ============
def send_telegram(msg, chat_id=TELEGRAM_CHAT):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

def get_news(query="gold OR nasdaq OR fed OR inflation", count=10):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize={count}&sortBy=publishedAt&apiKey={NEWS_KEY}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("articles", [])
    except:
        return []

def daily_report():
    print(f"[{datetime.now()}] التقرير اليومي...")
    send_telegram("⏳ *جاري اعداد التقرير...*\nيبحث البوت في الاخبار العالمية الان 🔄")

    a1 = get_news(query="federal reserve FED interest rate inflation CPI PCE", count=8)
    a2 = get_news(query="gold price XAU central bank buying", count=5)
    a3 = get_news(query="nasdaq technology stocks earnings AI", count=5)
    a4 = get_news(query="war conflict geopolitical china russia oil", count=5)
    a5 = get_news(query="dollar DXY treasury yields bonds recession", count=5)
    a6 = get_news(query="ECB BOJ economy GDP unemployment NFP", count=4)

    all_articles = a1 + a2 + a3 + a4 + a5 + a6
    if not all_articles:
        send_telegram("تعذر الحصول على اخبار كافية")
        return

    headlines = "\n".join([
        f"[{a.get('publishedAt', '')[:16].replace('T', ' ')}] {a['title']}"
        for a in all_articles[:25] if a.get('title')
    ])

    hour = datetime.now().hour
    date = datetime.now().strftime('%Y/%m/%d')

    if hour < 12:
        structure = MORNING_STRUCTURE.format(date=date)
    elif hour < 17:
        structure = MIDDAY_STRUCTURE.format(date=date)
    else:
        structure = EVENING_STRUCTURE.format(date=date)

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""الاخبار العالمية خلال اخر 24 ساعة:
{headlines}

{structure}

تذكر: اكتب باللغة العربية الفصحى فقط — ممنوع اي حرف اجنبي."""}
            ],
            max_tokens=2500
        )
        report = resp.choices[0].message.content
        if len(report) < 300:
            send_telegram("التقرير لم يكتمل — سيعاد المحاولة")
            return
        send_telegram(report)
        print(f"[{datetime.now()}] التقرير ارسل بنجاح")
    except Exception as e:
        send_telegram(f"خطا في التقرير: {e}")

def answer_question(user_question, chat_id):
    try:
        articles = get_news(query=user_question, count=5)
        news_context = ""
        if articles:
            news_context = "اخر الاخبار ذات الصلة:\n"
            news_context += "\n".join([f"- {a['title']}" for a in articles[:5] if a.get('title')])
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""السؤال: {user_question}
{news_context}

اجب باللغة العربية الفصحى فقط بهذا الشكل:

📰 *الموضوع:*
[شرح بسيط في جملتين]

🧠 *التحليل:*
الحدث → الفائدة → الدولار → الذهب و NAS100

💰 *الذهب:* [الاتجاه الحاسم + السبب]
📊 *NAS100:* [الاتجاه الحاسم + السبب]

⚡ *درجة الخطر:* 🟢 منخفض / 🟡 متوسط / 🔴 عالي"""}
            ],
            max_tokens=600
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"خطا: {e}"

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

def schedule_jobs():
    schedule.every().day.at("07:00").do(daily_report)  # 08:00 المغرب
    schedule.every().day.at("13:00").do(daily_report)  # 14:00 المغرب
    schedule.every().day.at("19:00").do(daily_report)  # 20:00 المغرب
    print("التقارير: 08:00 و 14:00 و 20:00 المغرب")
    while True:
        schedule.run_pending()
        time.sleep(60)

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
