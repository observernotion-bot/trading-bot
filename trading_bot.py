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
sent_news = set()

SYSTEM_PROMPT = """انت محلل اقتصادي كبير متخصص في الذهب XAU/USD و NAS100.

قواعد صارمة جدا:
1. اكتب باللغة العربية الفصحى فقط — ممنوع تماما اي حرف صيني او ياباني او كوري او روسي او فارسي او اي لغة اخرى غير العربية والارقام الانجليزية
2. لا تستخدم كلمات مثل قد / ربما / من المحتمل — كن حاسما ومباشرا
3. اشرح دائما المنطق الكامل: لماذا يحدث هذا وكيف يؤثر على الاسواق
4. فكر دائما بهذه السلسلة: الحدث → تاثيره على الفائدة → تاثيره على الدولار → تاثيره على الذهب و NAS100
5. كن دقيقا ومحددا مثل محللي Goldman Sachs و JPMorgan"""

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

def monitor_breaking_news():
    print(f"[{datetime.now()}] مراقبة الاخبار...")
    queries = [
        "war OR conflict OR attack OR crisis",
        "federal reserve interest rate decision",
        "gold price surge crash",
        "nasdaq crash rally",
        "china US trade tariffs",
        "inflation CPI data"
    ]
    for query in queries:
        articles = get_news(query=query, count=3)
        for article in articles:
            title = article.get("title", "")
            url = article.get("url", "")
            description = article.get("description", "")
            if not title or url in sent_news:
                continue
            try:
                check = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"هل هذا الخبر مهم جدا ويؤثر بشكل كبير على الذهب او NAS100؟\nالخبر: {title}\nاجب بكلمة واحدة فقط: نعم او لا"}
                    ],
                    max_tokens=10
                )
                answer = check.choices[0].message.content.strip()
                if "نعم" in answer or "yes" in answer.lower():
                    content = f"{title}. {description}" if description else title
                    resp = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"""حلل هذا الخبر العاجل. اكتب باللغة العربية الفصحى فقط بدون اي كلمات اجنبية.

الخبر: {content}

اكتب بهذا الشكل الدقيق:

🚨 *ماذا حدث؟*
[اشرح الخبر بجملتين بسيطتين كانك تشرح لشخص عادي]

❓ *لماذا هذا مهم للاسواق؟*
[اشرح السبب المنطقي في جملة واحدة]

نوع الحدث: [حرب / سياسة نقدية / تضخم / اقتصاد / جيوسياسي / طاقة]
درجة الخطر: [🟢 عادي / 🟡 مهم / 🔴 خطر عالي]

🔗 *المنطق الاقتصادي الكامل:*
الحدث → [تاثيره على توقعات الفائدة] → [تاثيره على الدولار] → [النتيجة النهائية على الذهب و NAS100]

🥇 *الذهب:* [صعود قوي / صعود / محايد / هبوط / هبوط قوي]
*السبب:* [اشرح لماذا بجملة واحدة محددة وحاسمة]

💻 *NAS100:* [صعود قوي / صعود / محايد / هبوط / هبوط قوي]
*السبب:* [اشرح لماذا بجملة واحدة محددة وحاسمة]

⏱ وقت التاثير: [فوري / ايام / اسابيع]"""}
                        ],
                        max_tokens=600
                    )
                    analysis = resp.choices[0].message.content
                    msg = f"🚨 *خبر عاجل — {datetime.now().strftime('%H:%M')} المغرب*\n\n📰 *{title[:150]}*\n\n{analysis}"
                    send_telegram(msg)
                    sent_news.add(url)
                    time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
                continue

def daily_report():
    print(f"[{datetime.now()}] التقرير اليومي...")
    send_telegram("⏳ *جاري اعداد التقرير اليومي الشامل...*\nيبحث البوت في كل الاخبار العالمية الان 🔄")

    a1 = get_news(query="federal reserve interest rate inflation CPI GDP unemployment", count=8)
    a2 = get_news(query="gold price XAU precious metals central bank", count=5)
    a3 = get_news(query="nasdaq technology stocks earnings AI", count=5)
    a4 = get_news(query="war conflict geopolitical china russia oil energy", count=5)
    a5 = get_news(query="dollar DXY treasury bonds yields", count=5)

    all_articles = a1 + a2 + a3 + a4 + a5
    if not all_articles:
        send_telegram("تعذر الحصول على اخبار كافية اليوم")
        return

    headlines = "\n".join([f"- {a['title']}" for a in all_articles[:25] if a.get('title')])
    
    hour = datetime.now().hour
    if hour < 12:
        period = "الصباحي"
    elif hour < 17:
        period = "الظهري"
    else:
        period = "المسائي"

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"""اكتب تقريرا يوميا شاملا باللغة العربية الفصحى فقط — ممنوع اي كلمة اجنبية.

الاخبار العالمية اليوم:
{headlines}

اكتب التقرير {period} بهذا الهيكل الدقيق:

📅 *التقرير {period} — {datetime.now().strftime('%Y/%m/%d')} — {datetime.now().strftime('%H:%M')} المغرب*

━━━━━━━━━━━━━━━━━━
📰 *اولا: اهم الاحداث الاقتصادية اليوم*

لكل حدث اكتب:
• *الحدث:* [ماذا حدث بالضبط]
• *الشرح:* [لماذا هذا مهم بجملة بسيطة]
• *التاثير الفوري:* [كيف يؤثر على الاسواق]

[اذكر 4 احداث على الاقل]

━━━━━━━━━━━━━━━━━━
🔗 *ثانيا: المنطق الاقتصادي الكامل اليوم*

اشرح كيف تتصل الاحداث ببعضها:
الاحداث اليوم → تاثيرها على توقعات الفائدة → تاثيرها على الدولار → النتيجة على الذهب و NAS100

━━━━━━━━━━━━━━━━━━
🥇 *ثالثا: تحليل الذهب XAU/USD*

• *الاتجاه:* [صعود قوي / صعود / محايد / هبوط / هبوط قوي]
• *لماذا؟* [3 اسباب منطقية محددة وحاسمة]
• *العوامل الداعمة:*
  1. [عامل محدد]
  2. [عامل محدد]
• *المخاطر الرئيسية:* [خطر واحد محدد]
• *مستويات مهمة:* دعم ... / مقاومة ...

━━━━━━━━━━━━━━━━━━
💻 *رابعا: تحليل NAS100*

• *الاتجاه:* [صعود قوي / صعود / محايد / هبوط / هبوط قوي]
• *لماذا؟* [3 اسباب منطقية محددة وحاسمة]
• *العوامل الداعمة:*
  1. [عامل محدد]
  2. [عامل محدد]
• *المخاطر الرئيسية:* [خطر واحد محدد]
• *مستويات مهمة:* دعم ... / مقاومة ...

━━━━━━━━━━━━━━━━━━
📊 *خامسا: السيناريوهات المحتملة*

🟢 *السيناريو المتفائل:*
الشرط: [ما يجب ان يحدث]
النتيجة على الذهب: [اتجاه + سبب]
النتيجة على NAS100: [اتجاه + سبب]

🟡 *السيناريو الاساسي الاكثر ترجيحا:*
الشرط: [ما يجب ان يحدث]
النتيجة على الذهب: [اتجاه + سبب]
النتيجة على NAS100: [اتجاه + سبب]

🔴 *السيناريو المتشائم:*
الشرط: [ما يجب ان يحدث]
النتيجة على الذهب: [اتجاه + سبب]
النتيجة على NAS100: [اتجاه + سبب]

━━━━━━━━━━━━━━━━━━
⚡ *سادسا: الخلاصة التنفيذية*

• *توصية الذهب:* [جملة حاسمة واحدة]
• *توصية NAS100:* [جملة حاسمة واحدة]
• *اهم حدث يجب مراقبته:* [حدث واحد محدد]
• *مستوى الخطر العام:* 🟢 منخفض / 🟡 متوسط / 🔴 عالي"""}
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

اجب باللغة العربية الفصحى فقط — ممنوع اي كلمة اجنبية.

اكتب بهذا الشكل:

📰 *الموضوع:*
[اشرح الموضوع بجملتين بسيطتين]

🔗 *المنطق الاقتصادي:*
الحدث → [تاثير على الفائدة] → [تاثير على الدولار] → [تاثير على الذهب و NAS100]

🥇 *الذهب:* [الاتجاه الحاسم]
السبب: [جملة واحدة محددة]

💻 *NAS100:* [الاتجاه الحاسم]
السبب: [جملة واحدة محددة]

⚡ درجة الخطر: 🟢 منخفض / 🟡 متوسط / 🔴 عالي"""}
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
                        "✅ تقرير المساء: 20:00\n"
                        "✅ تنبيهات عاجلة تلقائية\n\n"
                        "/report — تقرير فوري شامل\n"
                        "/news — اخر الاخبار\n"
                        "/help — المساعدة\n\n"
                        "او اكتب اي سؤال اقتصادي 👇", chat_id)
                elif text == "/report":
                    send_telegram("⏳ *جاري اعداد تقرير شامل...*", chat_id)
                    threading.Thread(target=daily_report).start()
                elif text == "/news":
                    articles = get_news(count=5)
                    if articles:
                        news_text = "📰 *اخر الاخبار:*\n\n"
                        for i, a in enumerate(articles[:5], 1):
                            news_text += f"{i}. {a['title'][:120]}\n\n"
                        send_telegram(news_text, chat_id)
                    else:
                        send_telegram("لا توجد اخبار الان", chat_id)
                elif text == "/help":
                    send_telegram(
                        "📖 *كيفية الاستخدام:*\n\n"
                        "اكتب اي سؤال مثل:\n"
                        "• ما تاثير رفع الفائدة على الذهب؟\n"
                        "• هل NAS100 صاعد اليوم؟\n"
                        "• ماذا يعني ارتفاع التضخم؟\n\n"
                        "/report — تقرير يومي شامل\n"
                        "/news — اخر الاخبار\n\n"
                        "🚨 التنبيهات العاجلة تصلك تلقائيا!", chat_id)
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
    schedule.every(30).minutes.do(monitor_breaking_news)
    print("التقارير: 08:00 و 14:00 و 20:00 توقيت المغرب")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("البوت يعمل...")
    send_telegram(
        "🤖 *البوت يعمل الان 24/7*\n\n"
        "✅ تقرير الصباح: 08:00\n"
        "✅ تقرير الظهر: 14:00\n"
        "✅ تقرير المساء: 20:00\n"
        "✅ تنبيهات عاجلة: كل 30 دقيقة\n\n"
        "اكتب /help 👇"
    )
    threading.Thread(target=monitor_breaking_news, daemon=True).start()
    scheduler_thread = threading.Thread(target=schedule_jobs, daemon=True)
    scheduler_thread.start()
    telegram_polling()
