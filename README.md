# مساعد صانع المحتوى العربي

مشروع Flask عربي كامل لصناع المحتوى العرب. يدعم توليد سكريبتات ريلز، عناوين وأوصاف SEO لليوتيوب، صور مصغرة احترافية، وبحث YouTube API.

## التشغيل المحلي

~~~bash
pip install -r requirements.txt
cp .env.example .env
python app.py
~~~

## المتغيرات المطلوبة

- OPENAI_API_KEY: مفتاح OpenAI.
- YOUTUBE_API_KEY: مفتاح YouTube Data API.
- SESSION_SECRET: مفتاح جلسة آمن.

## الصفحات

- /: الصفحة الرئيسية.
- /dashboard: لوحة توليد محتوى يوتيوب.
- /reels: توليد سكريبتات الريلز.
- /thumbnails: إنشاء الصور المصغرة.
