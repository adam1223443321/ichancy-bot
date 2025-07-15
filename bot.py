import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, filters
import requests
import os

# إعدادات البوت
BOT_TOKEN = "8075411215:AAEf6hDRpaZ69bVmueXnHLYTOgzHM_lsB9U"
SCRAPINGBEE_API_KEY = "CDED2GCYEA18TN6CABK52EK0LE062V2F85VZDYHY0NLNPKS04HEO8SJJ0EWHVSFN3GYOWGASNNF6JLXV"
PARENT_ID = "2456049"
COUNTER_FILE = "user_counter.txt"

logging.basicConfig(level=logging.INFO)
ASK_NAME, ASK_PASSWORD = range(2)

def get_next_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("35")
    with open(COUNTER_FILE, "r") as f:
        current = int(f.read().strip())
    next_counter = current + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(next_counter))
    return next_counter

def register_player(login_raw, password):
    counter = get_next_counter()
    login = f"c-{login_raw}-{counter}"
    email = f"{login}@agent.nsp"

    payload = {
        "email": email,
        "login": login,
        "password": password,
        "parentId": PARENT_ID
    }

    params = {
        "api_key": SCRAPINGBEE_API_KEY,
        "url": "https://agents.ichancy.com/global/api/Player/registerPlayer",
        "render_js": True,
        "wait": 3000,
        "block_resources": False,
        "premium_proxy": True
    }

    print("📦 إرسال الطلب عبر ScrapingBee:", payload)
    response = requests.post("https://app.scrapingbee.com/api/v1/", params=params, json=payload)
    print("🔍 حالة الرد:", response.status_code)
    print("📄 الرد الخام (أول 500 حرف):", response.text[:500])

    try:
        result = response.json()
        if result.get("status") == "success":
            return f"✅ تم إنشاء الحساب: {login}"
        else:
            return f"❌ فشل الإنشاء: {result.get('message', 'حدث خطأ غير معروف.')}"
    except Exception:
        return f"⚠️ تعذر قراءة الرد. ربما الرد ليس بصيغة JSON.\nتم طباعته في الطرفية."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أدخل الاسم الأساسي للحساب الجديد:")
    return ASK_NAME

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name_raw"] = update.message.text.strip()
    await update.message.reply_text("🔒 أدخل كلمة المرور:")
    return ASK_PASSWORD

async def receive_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_raw = context.user_data.get("name_raw")
    password = update.message.text.strip()
    result = register_player(name_raw, password)
    if len(result) > 4000:
        await update.message.reply_text("⚠️ الرد طويل جدًا، تحقق من الطرفية.")
    else:
        await update.message.reply_text(result)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم إلغاء العملية.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
