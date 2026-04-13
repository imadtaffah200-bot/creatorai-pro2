from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from pathlib import Path
from ai_engine import مولد_المحتوى_العربي
from youtube_api import عميل_يوتيوب
from utils.image_generator import منشئ_الصور_المصغرة
from utils.reels_generator import منشئ_الريلز
import os

load_dotenv()

التطبيق = Flask(__name__)
التطبيق.config["SECRET_KEY"] = os.getenv("SESSION_SECRET", "مفتاح-جلسة-محلي")
الذكاء = مولد_المحتوى_العربي()
يوتيوب = عميل_يوتيوب()
الصور = منشئ_الصور_المصغرة()
الريلز = منشئ_الريلز()

@التطبيق.route("/")
def الصفحة_الرئيسية():
    return render_template("index.html")

@التطبيق.route("/dashboard")
def لوحة_التحكم():
    return render_template("dashboard.html")

@التطبيق.route("/reels")
def صفحة_الريلز():
    return render_template("reels.html")

@التطبيق.route("/thumbnails")
def صفحة_الصور_المصغرة():
    return render_template("thumbnails.html")

@التطبيق.post("/api/generate/reels-script")
def توليد_سكريبت_ريلز():
    البيانات = request.get_json(silent=True) or {}
    الموضوع = البيانات.get("topic", "").strip()
    اللهجة = البيانات.get("dialect", "العربية الفصحى").strip()
    المدة = البيانات.get("duration", "30 ثانية").strip()
    if not الموضوع:
        return jsonify({"نجاح": False, "رسالة": "يرجى إدخال موضوع الريلز."}), 400
    النتيجة = الذكاء.توليد_سكريبت_ريلز(الموضوع, اللهجة, المدة)
    return jsonify({"نجاح": True, "النتيجة": النتيجة})

@التطبيق.post("/api/generate/youtube-seo")
def توليد_سيو_يوتيوب():
    البيانات = request.get_json(silent=True) or {}
    الموضوع = البيانات.get("topic", "").strip()
    الكلمات = البيانات.get("keywords", "").strip()
    اللهجة = البيانات.get("dialect", "العربية الفصحى").strip()
    if not الموضوع:
        return jsonify({"نجاح": False, "رسالة": "يرجى إدخال موضوع الفيديو."}), 400
    النتيجة = الذكاء.توليد_سيو_يوتيوب(الموضوع, الكلمات, اللهجة)
    return jsonify({"نجاح": True, "النتيجة": النتيجة})

@التطبيق.post("/api/generate/thumbnail")
def توليد_صورة_مصغرة():
    البيانات = request.get_json(silent=True) or {}
    العنوان = البيانات.get("title", "").strip()
    النمط = البيانات.get("style", "احترافي حديث").strip()
    if not العنوان:
        return jsonify({"نجاح": False, "رسالة": "يرجى إدخال عنوان الصورة المصغرة."}), 400
    المسار = الصور.إنشاء_صورة_مصغرة(العنوان, النمط)
    return jsonify({"نجاح": True, "مسار": f"/{المسار.as_posix()}"})

@التطبيق.post("/api/youtube/search")
def بحث_يوتيوب():
    البيانات = request.get_json(silent=True) or {}
    عبارة_البحث = البيانات.get("query", "").strip()
    if not عبارة_البحث:
        return jsonify({"نجاح": False, "رسالة": "يرجى إدخال عبارة البحث."}), 400
    النتائج = يوتيوب.بحث_عن_فيديوهات(عبارة_البحث)
    return jsonify({"نجاح": True, "النتائج": النتائج})

@التطبيق.post("/api/reels/create-video")
def إنشاء_فيديو_ريلز():
    البيانات = request.get_json(silent=True) or {}
    النص = البيانات.get("script", "").strip()
    العنوان = البيانات.get("title", "ريلز جديد").strip()
    if not النص:
        return jsonify({"نجاح": False, "رسالة": "يرجى إدخال سكريبت الريلز."}), 400
    المسار = الريلز.إنشاء_فيديو_نصي(العنوان, النص)
    return jsonify({"نجاح": True, "مسار": f"/{المسار.as_posix()}"})

@التطبيق.get("/download/<path:اسم_الملف>")
def تنزيل_ملف(اسم_الملف):
    المسار = Path("static") / اسم_الملف
    if not المسار.exists():
        return jsonify({"نجاح": False, "رسالة": "الملف غير موجود."}), 404
    return send_file(المسار, as_attachment=True)

if __name__ == "__main__":
    التطبيق.run(host="0.0.0.0", port=5000, debug=False)
