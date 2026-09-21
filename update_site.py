#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_site.py - מרענן את video-pool.json (מאגר הסרטונים ש-daily-engine.js בוחר ממנו כל יום).

מה זה עושה:
  1. מחפש ב-YouTube Data API v3 סרטוני עיצוב עדכניים (45 הימים האחרונים) לפי רשימת QUERIES.
  2. מסנן: רק סרטונים ציבוריים, ניתנים להטמעה (embeddable), לא חסומים בישראל, באורך סביר.
  3. בודק מחדש סרטונים שכבר במאגר (וזורק כאלה שנמחקו / הפכו פרטיים).
  4. שומר רשומות ידניות ("manual": true) - כאן מוסיפים TikTok / Instagram ידנית (אין API חיפוש חינמי להם).
  5. כותב את video-pool.json (עד MAX_POOL רשומות, החדשים קודם).

הרצה:
  YOUTUBE_API_KEY=xxxx python update_site.py

עלות מכסה: כל חיפוש = 100 יחידות, מכסה יומית חינמית = 10,000. ~12 חיפושים = ~1,200 יחידות.
"""
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/youtube/v3"
POOL_FILE = "video-pool.json"
MAX_POOL = 120        # גודל מאגר מקסימלי
DAYS_BACK = 45        # "עדכני" = פורסם בחודש וחצי האחרונים
PER_QUERY = 12        # תוצאות לכל חיפוש
MIN_SEC, MAX_SEC = 30, 90 * 60
REGION = "IL"

# (topic, query). ה-topic משמש את המנוע להתאמה עדינה לכרטיסיות עם אותו topic.
QUERIES = [
    ("ui", "UI design trends 2026"),
    ("ui", "Figma prototype design process"),
    ("ui", "product design case study"),
    ("brand", "brand identity design process"),
    ("brand", "branding studio logo design"),
    ("brand", "packaging design"),
    ("motion", "motion design 2026"),
    ("motion", "kinetic typography animation"),
    ("type", "typography design trends"),
    ("editorial", "editorial design magazine layout"),
    ("spatial", "spatial UI design Unity 3D"),
    ("illustration", "illustration process design"),
]


class QuotaExceeded(Exception):
    pass


def api(endpoint, **params):
    """קריאה ל-YouTube Data API. מחזיר dict. זורק QuotaExceeded / RuntimeError."""
    url = "%s/%s?%s" % (API, endpoint, urllib.parse.urlencode(params))
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        if e.code == 403 and "quota" in body.lower():
            raise QuotaExceeded(body)
        raise RuntimeError("HTTP %s: %s" % (e.code, body[:300]))


def parse_duration(iso):
    m = re.match(r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def usable(item):
    """האם סרטון (מתוך videos.list) מתאים להטמעה באתר."""
    st, cd = item.get("status", {}), item.get("contentDetails", {})
    if st.get("privacyStatus") != "public" or not st.get("embeddable"):
        return False
    if not (MIN_SEC <= parse_duration(cd.get("duration")) <= MAX_SEC):
        return False
    rr = cd.get("regionRestriction", {})
    if REGION in rr.get("blocked", []):
        return False
    if "allowed" in rr and REGION not in rr["allowed"]:
        return False
    return True


def verify(ids, key):
    """מחזיר {id: item} רק לסרטונים שעדיין תקינים. 50 ids לקריאה (יחידה אחת)."""
    ok = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        data = api("videos", part="status,contentDetails,snippet", id=",".join(chunk), key=key)
        for it in data.get("items", []):
            if usable(it):
                ok[it["id"]] = it
    return ok


def search(topic, query, key, published_after):
    data = api(
        "search", part="snippet", type="video", q=query, maxResults=PER_QUERY,
        videoEmbeddable="true", videoSyndicated="true", order="relevance",
        publishedAfter=published_after, relevanceLanguage="en", safeSearch="moderate", key=key,
    )
    return [(it["id"]["videoId"], topic) for it in data.get("items", []) if it.get("id", {}).get("videoId")]


def load_pool():
    try:
        with open(POOL_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_pool(pool):
    tmp = POOL_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, POOL_FILE)


def entry(item, topic, today):
    sn = item.get("snippet", {})
    return {
        "id": item["id"], "platform": "youtube", "topic": topic,
        "title": sn.get("title", ""), "channel": sn.get("channelTitle", ""),
        "published": (sn.get("publishedAt") or "")[:10], "addedAt": today,
    }


def main():
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        print("חסר YOUTUBE_API_KEY (משתנה סביבה / GitHub Secret).")
        return 1

    today = datetime.date.today().isoformat()
    after = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=DAYS_BACK)).strftime("%Y-%m-%dT%H:%M:%SZ")
    existing = load_pool()
    manual = [e for e in existing if e.get("manual")]
    auto_old = [e for e in existing if not e.get("manual") and e.get("platform", "youtube") == "youtube" and e.get("id")]
    print("מאגר קיים: %d (ידניים: %d)" % (len(existing), len(manual)))

    # 1. סרטונים חדשים
    found, seen = [], set()
    try:
        for topic, q in QUERIES:
            try:
                for vid, t in search(topic, q, key, after):
                    if vid not in seen:
                        seen.add(vid)
                        found.append((vid, t))
            except RuntimeError as e:
                print("דילגתי על '%s': %s" % (q, e))
    except QuotaExceeded:
        print("המכסה היומית נגמרה - ממשיך עם מה שנאסף עד כה.")

    # 2. אימות: חדשים + ישנים (ישנים = לזרוק מתים)
    try:
        ok_new = verify([v for v, _ in found], key)
        ok_old = verify([e["id"] for e in auto_old], key)
    except (QuotaExceeded, RuntimeError) as e:
        print("שגיאה באימות, המאגר לא שונה:", e)
        return 0

    fresh = [entry(ok_new[v], t, today) for v, t in found if v in ok_new]
    kept_old = [e for e in auto_old if e["id"] in ok_old and e["id"] not in {f["id"] for f in fresh}]
    dropped = len(auto_old) - len(kept_old)

    # 3. איחוד: ידניים תמיד נשארים; אוטומטיים - חדשים קודם, חתוך ל-MAX_POOL
    autos = sorted(fresh + kept_old, key=lambda e: (e.get("addedAt", ""), e.get("published", "")), reverse=True)
    autos = autos[: max(0, MAX_POOL - len(manual))]
    pool = manual + autos

    if not autos and not manual and existing:
        print("לא נמצאו תוצאות - משאיר את המאגר כמו שהוא.")
        return 0

    save_pool(pool)
    print("נכתב %s: %d סרטונים (חדשים: %d, הוסרו כלא-תקינים: %d)" % (POOL_FILE, len(pool), len(fresh), dropped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
