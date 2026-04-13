import os
import time
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI

class منشئ_الصور_المصغرة:
    """منشئ صور مصغرة يدعم OpenAI Images مع بديل محلي باستخدام Pillow."""

    def __init__(self):
        self.مجلد_الإخراج = Path("static/images/generated")
        self.مجلد_الإخراج.mkdir(parents=True, exist_ok=True)

    def إنشاء_صورة_مصغرة(self, العنوان, النمط="احترافي حديث"):
        if os.getenv("OPENAI_API_KEY"):
            try:
                return self._إنشاء_باستخدام_openai(العنوان, النمط)
            except Exception:
                return self._إنشاء_محلي(العنوان, النمط)
        return self._إنشاء_محلي(العنوان, النمط)

    def _إنشاء_باستخدام_openai(self, العنوان, النمط):
        العميل = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        الطلب = f"صورة مصغرة احترافية ليوتيوب باللغة العربية، نسبة 16:9، تباين عال، نص عربي واضح، العنوان: {العنوان}، النمط: {النمط}. بدون شعارات علامات تجارية."
        الاستجابة = العميل.images.generate(model="dall-e-3", prompt=الطلب, size="1792x1024", quality="standard", n=1)
        رابط = الاستجابة.data[0].url
        محتوى = requests.get(رابط, timeout=30).content
        المسار = self.مجلد_الإخراج / f"thumbnail-{int(time.time())}.png"
        المسار.write_bytes(محتوى)
        return المسار

    def _إنشاء_محلي(self, العنوان, النمط):
        العرض, الارتفاع = 1280, 720
        الصورة = Image.new("RGB", (العرض, الارتفاع), "#090d1f")
        الرسم = ImageDraw.Draw(الصورة)
        for س in range(العرض):
            نسبة = س / العرض
            لون = (int(20 + 80 * نسبة), int(24 + 30 * نسبة), int(70 + 120 * نسبة))
            الرسم.line([(س, 0), (س, الارتفاع)], fill=لون)
        الرسم.rounded_rectangle((55, 55, العرض - 55, الارتفاع - 55), radius=42, outline="#7dd3fc", width=8)
        الرسم.ellipse((العرض - 360, -120, العرض + 160, 400), fill="#f97316")
        الرسم.ellipse((-180, الارتفاع - 280, 300, الارتفاع + 180), fill="#22c55e")
        خط_كبير = self._خط(76)
        خط_صغير = self._خط(34)
        y = 220
        for سطر in self._تقسيم(العنوان, 18)[:4]:
            صندوق = الرسم.textbbox((0, 0), سطر, font=خط_كبير)
            x = العرض - 95 - (صندوق[2] - صندوق[0])
            الرسم.text((x + 4, y + 4), سطر, font=خط_كبير, fill="#111827")
            الرسم.text((x, y), سطر, font=خط_كبير, fill="#ffffff")
            y += 90
        الرسم.rounded_rectangle((80, 90, 430, 155), radius=22, fill="#facc15")
        الرسم.text((115, 106), النمط[:28], font=خط_صغير, fill="#111827")
        المسار = self.مجلد_الإخراج / f"thumbnail-{int(time.time())}.png"
        الصورة.save(المسار, "PNG")
        return المسار

    def _خط(self, الحجم):
        المرشحات = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
        for مسار in المرشحات:
            if Path(مسار).exists():
                return ImageFont.truetype(مسار, الحجم)
        return ImageFont.load_default()

    def _تقسيم(self, النص, الحد):
        الكلمات = النص.split()
        الأسطر, الحالي = [], ""
        for كلمة in الكلمات:
            تجربة = f"{الحالي} {كلمة}".strip()
            if len(تجربة) <= الحد:
                الحالي = تجربة
            else:
                if الحالي:
                    الأسطر.append(الحالي)
                الحالي = كلمة
        if الحالي:
            الأسطر.append(الحالي)
        return الأسطر
