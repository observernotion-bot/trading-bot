import requests
import threading
import schedule
import time
from datetime import datetime
from groq import Groq

# ============ المفاتيح ============
import os
GROQ_KEY = os.environ.get("GROQ_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT")
NEWS_KEY = os.environ.get("NEWS_KEY")

client = Groq(api_key=GROQ_KEY)
sent_news = set()

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
    print(f"[{datetime.now()}] مراقبة الاخبار العاجلة...")
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
                    messages=[{"role": "user", "content": f"هل هذا الخبر مهم جدا ويؤثر بشكل كبير على الذهب او NAS100؟\nالخبر: {title}\nاجب بكلمة واحدة فقط: نعم او لا"}],
                    max_tokens=10
                )
                answer = check.choices[0].message.content.strip()
                if "نعم" in answer or "yes" in answer.lower():
                    content = f"{title}. {description}" if description else title
                    resp = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"""انت محلل كبير في JPMorgan. حلل هذا الخبر العاجل.
اكتب باللغة العربية الفصحى فقط — ممنوع تماما اي حروف صينية او يابانية او اي لغة اخرى.

الخبر: {content}

اكتب بهذا الشكل:

نوع الحدث: [حرب / سياسة نقدية / تضخم / اقتصاد / جيوسياسي / طاقة]

درجة الخطر: [🟢 عادي او 🟡 مهم او 🔴 خطر عالي]

🥇 تاثير الذهب: [صعود قوي / صعود / محايد / هبوط / هبوط قوي]
السبب: [جملة واحدة بالعربية فقط]

💻 تاثير NAS100: [صعود قوي / صعود / محايد / هبوط / هبوط قوي]
السبب: [جملة واحدة بالعربية فقط]

وقت التاثير: [فوري / قصير المدى / طويل المدى]

السيناريو المتوقع: [جملتان بالعربية فقط]"""}],
                        max_tokens=400
                    )
                    analysis = resp.choices[0].message.content
                    msg = f"🚨 *خبر عاجل*\n\n📰 *{title[:150]}*\n\n{analysis}\n\n⏰ {datetime.now().strftime('%H:%M')} توقيت المغرب"
                    send_telegram(msg)
                    sent_news.add(url)
                    time.sleep(5)
            except Exception as e:
                print(f"Error: {e}")
                continue

def daily_report():
    print(f"[{datetime.now()}] التقرير اليومي...")
    send_telegram("⏳ *جاري اعداد التقرير اليومي الشامل...*\nالرجاء الانتظار دقيقة 🔄")

    a1 = get_news(query="federal reserve interest rate inflation CPI GDP", count=6)
    a2 = get_news(query="gold price XAU precious metals", count=4)
    a3 = get_news(query="nasdaq technology stocks earnings", count=4)
    a4 = get_news(query="war conflict geopolitical oil energy", count=4)

    all_articles = a1 + a2 + a3 + a4
    if not all_articles:
        send_telegram("تعذر الحصول على اخبار كافية اليوم")
        return

    headlines = "\n".join([f"- {a['title']}" for a in all_articles[:20] if a.get('title')])

    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""انت كبير المحللين في JPMorgan متخصص في الذهب XAU/USD و NAS100.

اكتب تقريرا يوميا شاملا باللغة العربية الفصحى فقط.
ممنوع تماما كتابة اي حروف صينية او يابانية او انجليزية داخل النص — العربية فقط.

الاخبار العالمية اليوم:
{headlines}

اكتب التقرير بهذا الهيكل:

📅 *التقرير اليومي الشامل — {datetime.now().strftime('%Y/%m/%d')}*
🏦 *تحليل على غرار JPMorgan*

━━━━━━━━━━━━━━━━━━
📰 *اولا: ملخص الاخبار الاقتصادية*
[اذكر اهم 4 اخبار واثرها المتوقع في جملة لكل خبر]

━━━━━━━━━━━━━━━━━━
🥇 *ثانيا: تحليل الذهب XAU/USD*
• الاتجاه العام: [صعود قوي / صعود / محايد / هبوط / هبوط قوي]
• التحيز الاساسي: [3 جمل منطقية بالعربية فقط]
• العوامل الداعمة:
  1. [عامل اول]
  2. [عامل ثاني]
• المخاطر: [خطر رئيسي واحد]
• مستويات مهمة: دعم ... مقاومة ...

━━━━━━━━━━━━━━━━━━
💻 *ثالثا: تحليل NAS100*
• الاتجاه العام: [صعود قوي / صعود / محايد / هبوط / هبوط قوي]
• التحيز الاساسي: [3 جمل منطقية بالعربية فقط]
• العوامل الداعمة:
  1. [عامل اول]
  2. [عامل ثاني]
• المخاطر: [خطر رئيسي واحد]
• مستويات مهمة: دعم ... مقاومة ...

━━━━━━━━━━━━━━━━━━
⚡ *رابعا: الخلاصة التنفيذية*
• توصية الذهب: [جملة حاسمة]
• توصية NAS100: [جملة حاسمة]
• اهم حدث للمراقبة: [حدث واحد]
• مستوى الخطر: 🟢 منخفض / 🟡 متوسط / 🔴 عالي"""}],
            max_tokens=1500
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
            messages=[{"role": "user", "content": f"""انت محلل اقتصادي كبير في JPMorgan.
السؤال: {user_question}
{news_context}
اجب باللغة العربية الفصحى فقط — ممنوع تماما اي حروف صينية او يابانية.
اجب في 4 جمل واضحة ومنظمة عن تاثير الموضوع على الذهب و NAS100.
اذكر درجة الخطر: منخفض / متوسط / عالي."""}],
            max_tokens=500
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
                    send_telegram("👋 *مرحبا! انا بوت التحليل الاقتصادي*\n\n✅ اراقب الاخبار العاجلة تلقائيا كل 30 دقيقة\n✅ تقرير شامل كل يوم 14:00\n\n/report — تقرير فوري\n/news — اخر الاخبار\n/help — المساعدة\n\nاو اكتب اي سؤال 👇", chat_id)
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
                    send_telegram("📖 *الاستخدام:*\n\naكتب اي سؤال مثل:\n• ما تاثير رفع الفائدة على الذهب؟\n• هل NAS100 صاعد اليوم؟\n\n/report — تقرير شامل\n/news — اخر الاخبار\n\n🚨 التنبيهات العاجلة تصلك تلقائيا!", chat_id)
                else:
                    send_telegram("⏳ *جاري التحليل...*", chat_id)
                    answer = answer_question(text, chat_id)
                    send_telegram(f"🤖 *التحليل:*\n\n{answer}", chat_id)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)

def schedule_jobs():
    schedule.every().day.at("13:00").do(daily_report)
    schedule.every(30).minutes.do(monitor_breaking_news)
    print("التقرير اليومي: 14:00 المغرب")
    print("مراقبة الاخبار: كل 30 دقيقة")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("البوت يعمل...")
    send_telegram(
        "🤖 *البوت يعمل الان 24/7*\n\n"
        "✅ مراقبة الاخبار العاجلة: كل 30 دقيقة\n"
        "✅ تقرير يومي شامل: 14:00 المغرب\n"
        "✅ Chatbot: جاهز\n\n"
        "🚨 ستصلك تنبيهات فورية عند اي خبر مهم!\n\n"
        "اكتب /help 👇"
    )
    threading.Thread(target=monitor_breaking_news, daemon=True).start()
    scheduler_thread = threading.Thread(target=schedule_jobs, daemon=True)
    scheduler_thread.start()
    telegram_polling()
