# 🤖 بوت رؤية الإخبارية — Rouwya News Bot

بوت تلقائي يجمع آخر الأخبار العسكرية والسياسية عبر Claude AI وينشرها في قناة تيليغرام.

---

## 📁 هيكل الملفات

```
rouwya-bot/
├── bot.py              # الكود الأساسي
├── requirements.txt    # المكتبات المطلوبة
├── render.yaml         # إعداد Render.com
└── README.md
```

---

## 🚀 خطوات النشر على Render.com

### 1. رفع المشروع على GitHub
- أنشئ مستودعاً جديداً على https://github.com
- ارفع الملفات الثلاثة: `bot.py` و `requirements.txt` و `render.yaml`

### 2. إنشاء الخدمة على Render
- افتح https://render.com وسجّل دخولاً مجانياً
- اضغط **New +** ثم **Background Worker**
- اربطه بمستودع GitHub الذي أنشأته
- اختر:
  - **Runtime:** Python 3
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `python bot.py`

### 3. إضافة المتغيرات البيئية
في قسم **Environment Variables** أضف:

| Key | Value |
|-----|-------|
| `TELEGRAM_TOKEN` | `8508380856:AAGx05GfzC8sREW-isEkLxHftXgKcjO5aSE` |
| `CHANNEL_ID` | `-1001331674265` |
| `ANTHROPIC_API_KEY` | مفتاح Anthropic الخاص بك |
| `INTERVAL_HOURS` | `3` (أو أي رقم تريده) |

### 4. تشغيل الخدمة
- اضغط **Deploy** — سيبدأ البوت تلقائياً وينشر أول نشرة فور الإطلاق

---

## ⚙️ تخصيص التوقيت

في `render.yaml` أو في Environment Variables:
- `INTERVAL_HOURS=1` → كل ساعة
- `INTERVAL_HOURS=3` → كل 3 ساعات (الافتراضي)
- `INTERVAL_HOURS=6` → كل 6 ساعات

---

## 📝 ملاحظات

- الخطة المجانية في Render تُوقف الخدمة بعد عدم النشاط — استخدم **Background Worker** وليس Web Service
- تأكد أن البوت مُضاف كـ **Admin** في قناة @rouwya
- مفتاح Anthropic متاح من: https://console.anthropic.com
