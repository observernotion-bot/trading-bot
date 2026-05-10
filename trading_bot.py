import requests
import threading
import schedule
import time
import os
from datetime import datetime
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or "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"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") or "8705246619:AAEocz5YRx8-ixRCsDJERirWFr-UYY28rZs"
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT") or "8607532338"
NEWS_KEY = os.environ.get("NEWS_KEY") or "08ab77f19e6847eaa2fccf75afc252d4"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """انت نظام ذكاء اصطناعي متخصص في تحليل الاسواق المالية للمتداولين.

هدفك الوحيد: تحويل الاخبار الاقتصادية والجيوسياسية واخبار البنوك المركزية الى تحليل سوقي واضح ومباشر يركز فقط على:
- الذهب XAUUSD
- مؤشر النازداك NAS100

قواعد صارمة جدا:
1. اكتب باللغة العربية الفصحى فقط — ممنوع تماما اي حرف صيني او ياباني او كوري او روسي او فارسي
2. لا تستخدم كلمات مثل قد او ربما او من المحتمل — كن حاسما ومباشرا
3. لا تعطي اخبار بدون تحليل
4. لا تعطي تحليل بدون بايز
5. لا تتكلم عن اصول اخرى غير الذهب والنازداك
6. كل شيء مبني على منطق اقتصادي حقيقي"""

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

    a1 = get_news(query="federal reserve FED interest rate inflation CPI", count=8)
    a2 = get_news(query="gold price XAU central bank", count=5)
    a3 = get_news(query="nasdaq technology stocks earnings", count=5)
    a4 = get_news(query="war conflict geopolitical oil energy", count=5)
    a5 = get_news(query="dollar DXY treasury yields bonds", count=5)
    a6 = get_news(query="ECB europe economy recession", count=4)

    all_articles = a1 + a2 + a3 + a4 + a5 + a6
    if not all_articles:
        send_telegram("تعذر الحصول على اخبار كافية")
        return

    headlines = "\n".join([
        f"[{a.get('publishedAt', '')[:16].replace('T', ' ')}] {a['title']}"
        for a in all_articles[:25] if a.get('title')
    ])

    hour = datetime.now().hour
    if hour < 12:
        period = "الصباحي 🌅"
    elif hour < 17:
        period = "الظهري ☀️"
    else:
        period = "المسائي 🌙"

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""اكتب التقرير {period} باللغة العربية الفصحى فقط — ممنوع اي كلمة اجنبية.

الاخبار العالمية خلال اخر 24 ساعة:
{headlines}

اكتب التقرير بهذا الهيكل الدقيق:

📅 *التقرير {period}*
🕐 *{datetime.now().strftime('%Y/%m/%d — %H:%M')} توقيت المغرب*

━━━━━━━━━━━━━━━━━━
📌 *اولا: اهم الاخبار العالمية*

اعرض اهم الاحداث مع التوقيت:

🌍 *الوضع الاقتصادي العالمي:*
[اذكر اهم الاحداث الاقتصادية مع التوقيت — التضخم / النمو / الركود]

🏦 *البنوك المركزية:*
[اذكر اي تصريحات او قرارات للفيدرالي او المركزي الاوروبي]

⚠️ *الجيوسياسية:*
[اذكر اهم التوترات والاحداث الدولية]

━━━━━━━━━━━━━━━━━━
🧠 *ثانيا: التحليل*

💰 *تحليل الذهب XAUUSD:*
- كيف تؤثر الاخبار على الذهب؟
- هل تدعم الصعود ام الهبوط؟
- السبب المنطقي: الدولار / الفيدرالي / المخاطرة
- مدة التاثير: ساعات / 1-3 ايام / اسبوع

📊 *تحليل النازداك NAS100:*
- تاثير الاخبار على الاسهم التقنية
- هل السوق في وضع مخاطرة ام تحوط؟
- تاثير الفائدة والسيولة
- السبب المنطقي والواضح

━━━━━━━━━━━━━━━━━━
🧭 *ثالثا: الربط بين الاسواق*

اشرح العلاقة بين الذهب والنازداك والدولار الان:
- هل نحن في وضع مخاطرة ام تحوط؟
- كيف يؤثر الدولار على الاثنين؟

━━━━━━━━━━━━━━━━━━
🔥 *رابعا: بايز السوق — القرار النهائي*

💰 *بايز الذهب:*
[Bullish / Bearish / Neutral]
السبب: [سبب واحد او اثنان فقط مبني على الفيدرالي / الدولار / المخاطرة / التضخم]
المدة: [قصير المدى / 1-3 ايام / اسبوعي]

📊 *بايز النازداك:*
[Bullish / Bearish / Neutral]
السبب: [سبب واحد او اثنان فقط مبني على الفائدة / النمو / السيولة / المخاطرة]
المدة: [قصير المدى / 1-3 ايام / اسبوعي]

━━━━━━━━━━━━━━━━━━
🎯 *خامسا: الخلاصة النهائية*

- اتجاه الذهب: [صعود / هبوط / محايد]
- اتجاه النازداك: [صعود / هبوط / محايد]
- حالة السوق: [Risk-On / Risk-Off / Mixed]
- القوة المسيطرة: [الدولار / الفيدرالي / الجيوسياسية / السيولة]"""}
            ],
            max_tokens=2500
        )
        report = resp.choices[0].message.content
        if len(report) < 300:
            send_telegram("التقرير لم يكتمل")
            return
        send_telegram(report)
        print(f"[{datetime.now()}] التقرير ارسل")
    except Exception as e:
        send_telegram(f"خطا: {e}")

def answer_question(user_question, chat_id):
    try:
        articles = get_news(query=user_question, count=5)
        news_context = ""
        if articles:
            news_context = "اخر الاخبار:\n"
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
[المنطق الاقتصادي — الحدث ← الفائدة ← الدولار ← الذهب و NAS100]

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
                        "✅ تقرير الصباح: 08:00\n"
                        "✅ تقرير الظهر: 14:00\n"
                        "✅ تقرير المساء: 20:00\n\n"
                        "/report — تقرير فوري\n"
                        "/help — المساعدة\n\n"
                        "او اكتب اي سؤال 👇", chat_id)
                elif text == "/report":
                    send_telegram("⏳ *جاري اعداد تقرير...*", chat_id)
                    threading.Thread(target=daily_report).start()
                elif text == "/help":
                    send_telegram(
                        "📖 *الاستخدام:*\n\n"
                        "اكتب اي سؤال مثل:\n"
                        "• ما تاثير رفع الفائدة على الذهب؟\n"
                        "• هل NAS100 صاعد اليوم؟\n\n"
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
        "✅ تقرير الصباح: 08:00\n"
        "✅ تقرير الظهر: 14:00\n"
        "✅ تقرير المساء: 20:00\n\n"
        "اكتب /report لتقرير فوري 👇"
    )
    scheduler_thread = threading.Thread(target=schedule_jobs, daemon=True)
    scheduler_thread.start()
    telegram_polling()
