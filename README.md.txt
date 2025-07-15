# 🤖 Ichancy Telegram Bot | بوت إيتشاني تيليجرام

أداة آلية تستخدم عبر تيليجرام لإنشاء حسابات على موقع [Ichancy](https://ichancy.com) مع تجاوز الحماية، مثل التحقق من الهيدر، ومنع الـ IP، وحقول CSRF.

---

## 🧠 الميزات Features

- 🚀 تسجيل تلقائي لحسابات جديدة في موقع Ichancy
- ⚙️ تخطي حماية الموقع باستخدام headers مخصصة
- 🔢 تخزين عدد الحسابات المنفذة في ملف `index.txt`
- 💬 تشغيل مباشر عبر أوامر تيليجرام

---

## 📦 المتطلبات Requirements

- Python 3.10+
- مكتبات:
  - `requests`
  - `python-telegram-bot==20.6`

---

## 🧪 الأوامر داخل البوت Telegram Commands

| الأمر | الوصف |
|-------|-------|
| `/start` | بدء التفاعل مع البوت |
| `/create` | تسجيل حساب جديد تلقائي |
| `/status` | (اختياري) عرض عدد الحسابات المُسجلة |
| `/reset_index` | (اختياري) إعادة العد من البداية |

---

## ⚙️ طريقة التشغيل Run Locally

```bash
pip install -r requirements.txt
bash start.sh
