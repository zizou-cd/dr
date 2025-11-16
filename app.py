from flask import Flask, render_template, url_for, Response, request
from datetime import datetime, timezone
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

SITE = {
    "name": "Dr. Abdelaziz Guitouni",
    "role": "Medical Doctor",
    "org": "CHU de Constantine",
    "org_full": "University Hospital Center of Constantine (CHU de Constantine)",
    "location": "Constantine, Algeria",
    # إظهار الإيميل على الموقع اختياري (لن نستخدمه في الإرسال)
    "show_email": False,
    "email": "dr.guitouni@example.com",   # لن يُستخدم للإرسال، فقط للعرض إذا فعلت show_email=True
    "cv_url": "",                         # e.g., "https://example.com/Dr_Guitouni_CV.pdf"
    # ضع رابط Sarahah هنا (استبدل yourusername باسم حسابك)
    "sarahah_url": "https://sarahah.pro/medboss",
    "tagline": "Compassionate care. Continuous learning. Thoughtful use of technology.",
    "interests": ["Programming", "Artificial Intelligence", "Reading"],
    "experience": [
        {
            "role": "Medical Doctor",
            "org": "CHU de Constantine",
            "place": "Constantine, Algeria",
            "period": "Present",
            "desc": "Clinical practice and patient-centered care at a university hospital center.",
        }
    ],
    "publications_note": "Add selected publications or projects here.",
}

def _photo_src():
    photo_path = os.path.join(app.static_folder, "images", "photo.jpg")
    if os.path.exists(photo_path):
        return url_for("static", filename="images/photo.jpg")
    return url_for("static", filename="images/avatar.svg")

@app.route("/")
def index():
    now_utc = datetime.now(timezone.utc)
    return render_template(
        "index.html",
        site=SITE,
        photo_src=_photo_src(),
        year=now_utc.year,
        last_updated=now_utc.date().isoformat(),
    )

# (اختياري) robots + sitemap
@app.route("/robots.txt")
def robots():
    base = request.url_root.rstrip("/")
    return Response(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    base = request.url_root.rstrip("/")
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{base}/</loc></url>
</urlset>'''
    return Response(xml, mimetype="application/xml")

if __name__ == "__main__":
    print(f"Serving: {SITE['name']}")
    print("Open: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)