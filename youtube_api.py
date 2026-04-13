import os
from googleapiclient.discovery import build

class عميل_يوتيوب:
    """طبقة اتصال مبسطة مع YouTube Data API."""

    def __init__(self):
        self.مفتاح_يوتيوب = os.getenv("YOUTUBE_API_KEY")
        self.الخدمة = build("youtube", "v3", developerKey=self.مفتاح_يوتيوب) if self.مفتاح_يوتيوب else None

    def _تأكد_من_الاتصال(self):
        if not self.الخدمة:
            raise RuntimeError("يرجى ضبط المتغير YOUTUBE_API_KEY قبل استخدام YouTube API.")

    def بحث_عن_فيديوهات(self, عبارة_البحث, الحد=10):
        self._تأكد_من_الاتصال()
        الطلب = self.الخدمة.search().list(q=عبارة_البحث, part="snippet", type="video", maxResults=الحد, relevanceLanguage="ar", safeSearch="moderate")
        البيانات = الطلب.execute()
        النتائج = []
        for عنصر in البيانات.get("items", []):
            المقتطف = عنصر.get("snippet", {})
            النتائج.append({
                "معرف": عنصر.get("id", {}).get("videoId"),
                "عنوان": المقتطف.get("title"),
                "قناة": المقتطف.get("channelTitle"),
                "وصف": المقتطف.get("description"),
                "صورة": المقتطف.get("thumbnails", {}).get("high", {}).get("url"),
            })
        return النتائج

    def إحصاءات_فيديو(self, معرف_الفيديو):
        self._تأكد_من_الاتصال()
        الطلب = self.الخدمة.videos().list(part="statistics,snippet", id=معرف_الفيديو)
        البيانات = الطلب.execute()
        العناصر = البيانات.get("items", [])
        if not العناصر:
            return None
        العنصر = العناصر[0]
        return {"عنوان": العنصر.get("snippet", {}).get("title"), "إحصاءات": العنصر.get("statistics", {})}

    def اقتراح_كلمات_من_نتائج(self, عبارة_البحث, الحد=10):
        النتائج = self.بحث_عن_فيديوهات(عبارة_البحث, الحد)
        الكلمات = []
        for نتيجة in النتائج:
            الكلمات.extend((نتيجة.get("عنوان") or "").split())
        كلمات_منقاة = [كلمة.strip("،.!؟:؛").lower() for كلمة in الكلمات if len(كلمة) > 3]
        return sorted(set(كلمات_منقاة))[:30]
