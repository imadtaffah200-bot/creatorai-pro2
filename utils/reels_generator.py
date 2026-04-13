import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ✅ FIX: moviepy الجديد ما فيهش .editor
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip


class منشئ_الريلز:
    """أداة أولية لإنشاء فيديو ريلز عمودي من نص عربي."""

    def __init__(self):
        self.مجلد_الإخراج = Path("static/videos/generated")
        self.مجلد_الإخراج.mkdir(parents=True, exist_ok=True)
        self.مجلد_الشرائح = Path("static/images/reels")
        self.مجلد_الشرائح.mkdir(parents=True, exist_ok=True)

    def إنشاء_فيديو_نصي(self, العنوان, النص, ملف_صوت=None):
        المقاطع = []
        الشرائح = self._إنشاء_شرائح(العنوان, النص)

        for شريحة in الشرائح:
            المقاطع.append(
                ImageClip(str(شريحة))
                .set_duration(3)
                .resize(height=1920)
            )

        الفيديو = concatenate_videoclips(المقاطع, method="compose")

        if ملف_صوت:
            الصوت = AudioFileClip(ملف_صوت)
            الفيديو = الفيديو.set_audio(الصوت)

            # FIX: تجنب crash إذا الصوت أطول/أقصر
            الفيديو = الفيديو.set_duration(min(الفيديو.duration, الصوت.duration))

        المسار = self.مجلد_الإخراج / f"reel-{int(time.time())}.mp4"

        الفيديو.write_videofile(
            str(المسار),
            fps=24,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )

        return المسار

    def _إنشاء_شرائح(self, العنوان, النص):
        الجمل = [
            جملة.strip()
            for جملة in النص.replace("؟", ".").replace("!", ".").split(".")
            if جملة.strip()
        ]

        الشرائح = []

        for رقم, جملة in enumerate([العنوان] + الجمل[:8]):
            شريحة = self.مجلد_الشرائح / f"slide-{int(time.time())}-{رقم}.png"
            self._رسم_شريحة(جملة, شريحة, رقم)
            الشرائح.append(شريحة)

        return الشرائح

    def _رسم_شريحة(self, النص, المسار, رقم):
        العرض, الارتفاع = 1080, 1920
        الصورة = Image.new("RGB", (العرض, الارتفاع), "#09090f")
        الرسم = ImageDraw.Draw(الصورة)

        ألوان = ["#38bdf8", "#a78bfa", "#f97316", "#22c55e"]

        الرسم.rounded_rectangle(
            (70, 90, العرض - 70, الارتفاع - 90),
            radius=60,
            outline=ألوان[رقم % len(ألوان)],
            width=10
        )

        الخط = self._خط(68)
        y = 620

        for سطر in self._تقسيم(النص, 18)[:7]:
            صندوق = الرسم.textbbox((0, 0), سطر, font=الخط)
            x = (العرض - (صندوق[2] - صندوق[0])) / 2

            الرسم.text((x, y), سطر, font=الخط, fill="#ffffff")
            y += 94

        الرسم.text(
            (90, الارتفاع - 190),
            "مساعد صانع المحتوى العربي",
            font=self._خط(38),
            fill="#d1d5db"
        )

        الصورة.save(str(mسار) if False else str(المسار), "PNG")  # FIX صغير للـ safety

    def _خط(self, الحجم):
        مسار = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

        if مسار.exists():
            return ImageFont.truetype(str(مسار), الحجم)

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