import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

INDEX_FILE = "index.txt"

def read_index():
    try:
        with open(INDEX_FILE, "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 1

def write_index(value):
    with open(INDEX_FILE, "w") as f:
        f.write(str(value))

def register_account():
    index = read_index()
    username = f"adam_auto_{index}"
    email = f"{username}@bot.com"
    password = "Strong123"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://ichancy.com/register",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": password
        # إذا فيه CSRF أو حماية إضافية، نضيفها هنا
    }

    try:
        response = requests.post("https://ichancy.com/register", data=payload, headers=headers)
        if "success" in response.text.lower():
            write_index(index + 1)
            return f"✅ تم إنشاء الحساب: {username}"
        else:
            return f"❌ فشل التسجيل، الرد:\n{response.text[:200]}"
    except Exception as e:
        return f"💥 خطأ أثناء التسجيل: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 أهلاً بك في بوت إيتشاني! استخدم /create لتسجيل حساب جديد.")

async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = register_account()
    await update.message.reply_text(result)

def main():
    TOKEN = "8075411215:AAEf6hDRpaZ69bVmueXnHLYTOgzHM_lsB9U"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create", create))
    app.run_polling()

if __name__ == "__main__":
    main()
