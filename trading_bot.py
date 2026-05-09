import requests
import threading
import schedule
import time
from datetime import datetime
from groq import Groq

# ============ المفاتيح ============
GROQ_KEY = "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"
TELEGRAM_TOKEN = "8705246619:AAEocz5YRx8-ixRCsDJERirWFr-UYY28rZs"
TELEGRAM_CHAT = "8607532338"
NEWS_KEY = "08ab77f19e6847eaa2fccf75afc252d4"

client = Groq(api_key=GROQ_KEY)

def send_telegram(msg, chat_id=TELEGRAM_CHAT):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "Markdown"
        }, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

def get_news(query="gold OR nasdaq OR fed OR inflation OR economy", count=8):
    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={query}&language=en&pageSize={count}"
        f"&sortBy=publishedAt&apiKey={NEWS_KEY}"
    )
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        return data.get("articles", [])
    except Exception as e:
        print(f"News error: {e}")
        return []

def analyze_news(title):
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""أنت محلل اقتصادي عالمي خبير مثل Goldman Sachs.
حلل هذا الخبر بدقة:
{title}

أجب بهذا الشكل فقط:
🥇 الذهب: صعود/هبوط/محايد
💻 NAS100: صعود/هبوط/محايد
⚡ الأهمية: 1-10
📊 التحليل: (جملتان واضحتان بالعربية تشرح السبب المنطقي)"""}],
            max_tokens=300
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"خطأ في التحليل: {e}"

def daily_report():
    print(f"[{datetime.now()}] بدء التقرير اليومي...")
    send_telegram("⏳ *جاري إعداد التقرير اليومي الشامل...*\nالرجاء الانتظار 30 ثانية")
    articles = get_news(
        query="gold price OR XAU OR nasdaq100 OR NQ100 OR federal reserve OR inflation OR CPI OR GDP OR unemployment",
        count=10
    )
    if not articles:
        send_telegram("⚠️ *لم يتم العثور على أخبار كافية للتقرير اليوم*")
        return
    headlines = "\n".join([f"- {a['title']}" for a in articles[:10] if a.get('title')])
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""أنت محلل اقتصادي كبير في Goldman Sachs متخصص في الذهب و NAS100.

بناءً على هذه الأخبار العالمية اليوم:
{headlines}

اكتب تقريراً يومياً شاملاً بهذا الهيكل الدقيق:

📅 *التقرير اليومي — {datetime.now().strftime('%Y/%m/%d')}*

━━━━━━━━━━━━━━━━━━
🥇 *تحليل الذهب XAU/USD*
• الاتجاه العام: صعود/هبوط/محايد
• الـ Bias الأساسي: (شرح 3 جمل)
• العوامل الداعمة: (نقطتان)
• المخاطر: (نقطة واحدة)

━━━━━━━━━━━━━━━━━━
💻 *تحليل NAS100*
• الاتجاه العام: صعود/هبوط/محايد
• الـ Bias الأساسي: (شرح 3 جمل)
• العوامل الداعمة: (نقطتان)
• المخاطر: (نقطة واحدة)

━━━━━━━━━━━━━━━━━━
⚡ *الخلاصة التنفيذية*
• أولوية اليوم: (جملة واحدة حاسمة)
• تحذير: (إن وجد)"""}],
            max_tokens=1000
        )
        report = resp.choices[0].message.content
        if len(report) < 200:
            send_telegram("⚠️ *التقرير لم يكن كافياً — سيُعاد المحاولة لاحقاً*")
            return
        send_telegram(f"📊 {report}")
    except Exception as e:
        send_telegram(f"⚠️ خطأ في التقرير: {e}")

def answer_question(user_question, chat_id):
    try:
        news_context = ""
        articles = get_news(query=user_question, count=5)
        if articles:
            news_context = "آخر الأخبار ذات الصلة:\n"
            news_context += "\n".join([f"- {a['title']}" for a in articles[:5] if a.get('title')])
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"""أنت محلل اقتصادي خبير في الذهب و NAS100.
المستخدم سألك: "{user_question}"
{news_context}
أجب بشكل مباشر ومفيد بالعربية في 3-5 جمل.
ركز على التأثير على الذهب و NAS100."""}],
            max_tokens=400
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ خطأ: {e}"

def telegram_polling():
    offset = None
    print("🤖 Chatbot جاهز...")
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
                        "👋 *مرحباً! أنا بوت التحليل الاقتصادي*\n\n"
                        "• اكتب أي سؤال اقتصادي\n"
                        "• /report — تقرير فوري\n"
                        "• /news — آخر الأخبار\n"
                        "• /help — المساعدة", chat_id)
                elif text == "/report":
                    send_telegram("⏳ *جاري إعداد تقرير فوري...*", chat_id)
                    threading.Thread(target=daily_report).start()
                elif text == "/news":
                    articles = get_news(count=5)
                    if articles:
                        news_text = "📰 *آخر الأخبار:*\n\n"
                        for a in articles[:5]:
                            news_text += f"• {a['title'][:100]}\n"
                        send_telegram(news_text, chat_id)
                    else:
                        send_telegram("⚠️ لا توجد أخبار الآن", chat_id)
                elif text == "/help":
                    send_telegram(
                        "📖 *كيفية الاستخدام:*\n\n"
                        "اكتب مثلاً:\n"
                        "- ما تأثير رفع الفائدة على الذهب؟\n"
                        "- هل NAS100 صاعد اليوم؟\n\n"
                        "/report — تقرير يومي\n"
                        "/news — آخر الأخبار", chat_id)
                else:
                    send_telegram("⏳ *جاري التحليل...*", chat_id)
                    answer = answer_question(text, chat_id)
                    send_telegram(f"🤖 *التحليل:*\n\n{answer}", chat_id)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)

def schedule_jobs():
    schedule.every().day.at("13:00").do(daily_report)
    print("📅 التقرير مجدول 14:00 توقيت المغرب")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("🚀 البوت يعمل...")
    send_telegram(
        "🤖 *البوت يعمل الآن 24/7!*\n\n"
        "✅ Chatbot: جاهز\n"
        "✅ التقرير اليومي: 14:00 توقيت المغرب\n\n"
        "اكتب /help 👇"
    )
    scheduler_thread = threading.Thread(target=schedule_jobs, daemon=True)
    scheduler_thread.start()
    telegram_polling()
