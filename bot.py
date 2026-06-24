import os
import logging
import requests
import anthropic
from datetime import datetime

# ── إعداد السجل ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ── المتغيرات البيئية ─────────────────────────────────────────
TELEGRAM_TOKEN  = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID      = os.environ.get("CHANNEL_ID")
ANTHROPIC_KEY   = os.environ.get("ANTHROPIC_API_KEY")

# ── تهيئة عميل Anthropic ─────────────────────────────────────
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# ── إرسال رسالة إلى تيليغرام ─────────────────────────────────
def send_telegram(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        log.info("✅ تم الإرسال بنجاح")
        return True
    except Exception as e:
        log.error(f"❌ فشل الإرسال: {e}")
        return False

# ── توليد الأخبار عبر Claude ─────────────────────────────────
def generate_news() -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    prompt = f"""أنت محرر أخبار عسكرية وسياسية متخصص في شؤون الشرق الأوسط.
الوقت الحالي: {now}

ابحث عن أبرز الأخبار العسكرية والسياسية في الساعات الـ24 الماضية وقدّم منشوراً
احترافياً لقناة تيليغرام باللغة العربية يحتوي على:

• 3 أخبار مهمة كحدٍّ أدنى
• لكل خبر: عنوان قصير جريء + فقرة تفصيلية (3-4 أسطر)
• ركّز على: العراق، إيران، إسرائيل، سوريا، الخليج، الولايات المتحدة، روسيا، أوكرانيا
• أضف مصدراً أو إشارة للمصدر عند الإمكان
• اختم بجملة تحريرية موجزة

صيغة كل خبر:
🔴 <b>العنوان</b>
النص التفصيلي...
📌 المصدر: ...

افصل بين الأخبار بـ ─────────────────"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1800,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[{"role": "user", "content": prompt}]
        )
        text_parts = [b.text for b in response.content if hasattr(b, "text") and b.text]
        return "\n".join(text_parts).strip()
    except Exception as e:
        log.error(f"❌ خطأ في Claude API: {e}")
        return ""

# ── الدورة الكاملة: توليد + إرسال ───────────────────────────
def run_cycle():
    log.info("⏳ بدء دورة جديدة...")
    timestamp = datetime.utcnow().strftime("%d/%m/%Y — %H:%M UTC")
    header = f"📡 <b>نشرة رؤية الإخبارية</b>\n🕐 {timestamp}\n\n"

    news = generate_news()
    if not news:
        log.warning("⚠️ لم يُنتج Claude محتوى")
        return

    full_message = header + news + "\n\n<i>— قناة رؤية | @rouwya</i>"

    if len(full_message) > 4096:
        full_message = full_message[:4090] + "…"

    send_telegram(full_message)

# ── نقطة الدخول ──────────────────────────────────────────────
if __name__ == "__main__":
    log.info("🚀 بوت رؤية يعمل")

    if not all([TELEGRAM_TOKEN, CHANNEL_ID, ANTHROPIC_KEY]):
        log.critical("❌ متغيرات البيئة ناقصة")
        exit(1)

    run_cycle()
