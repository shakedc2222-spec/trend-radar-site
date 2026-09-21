/*!
 * daily-engine.js — מנוע היומי של Trend Radar
 * אלגוריתם בלבד: בחירה + סידור + שיבוץ סרטונים. בלי DOM.
 * עובד בדפדפן (window.DailyEngine) וב-Node (require) לבדיקות.
 *
 * עקרונות:
 *  1. כל הלוח נגזר מתאריך (Asia/Jerusalem) => כולם רואים אותו לוח באותו יום, ולמחרת הכול משתנה.
 *  2. "שקית ערבוב" (shuffle bag) דטרמיניסטית: פריט לא חוזר עד שכל המאגר הוצג, ואין חזרות ביום עוקב.
 *  3. סרטון ייחודי לכל כרטיסייה (מאגר סרטונים נפרד, אותו מנגנון שקית).
 *  4. הפריסה (top/left/rot) נוצרת מחדש כל יום - לא נשמרת בנתונים.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.DailyEngine = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ───────────── 1. תאריך + זרע ───────────── */

  const EPOCH = Date.UTC(2026, 0, 1); // יום 0 של הרצף. לא לשנות אחרי עלייה לאוויר (משנה את כל הרצף).

  // מחזיר 'YYYY-MM-DD'. ?date=2026-10-01 ב-URL (או opts.date) מאפשר לצפות בכל יום שרוצים.
  function dateKey(opts) {
    opts = opts || {};
    if (opts.date && /^\d{4}-\d{2}-\d{2}$/.test(opts.date)) return opts.date;
    const now = opts.now || new Date();
    if (opts.tz === 'local') {
      const p = n => String(n).padStart(2, '0');
      return now.getFullYear() + '-' + p(now.getMonth() + 1) + '-' + p(now.getDate());
    }
    const parts = new Intl.DateTimeFormat('en-US', {
      timeZone: opts.tz || 'Asia/Jerusalem', year: 'numeric', month: '2-digit', day: '2-digit'
    }).formatToParts(now);
    const g = t => parts.find(x => x.type === t).value;
    return g('year') + '-' + g('month') + '-' + g('day');
  }

  function dayIndex(key) {
    const [y, m, d] = key.split('-').map(Number);
    return Math.max(0, Math.round((Date.UTC(y, m - 1, d) - EPOCH) / 864e5));
  }

  // האש טוב למחרוזות (xmur3) + PRNG (mulberry32). ה-LCG הישן עם סכום תווים יצר התנגשויות בין ימים.
  function xmur3(str) {
    let h = 1779033703 ^ str.length;
    for (let i = 0; i < str.length; i++) {
      h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
      h = (h << 13) | (h >>> 19);
    }
    return function () {
      h = Math.imul(h ^ (h >>> 16), 2246822507);
      h = Math.imul(h ^ (h >>> 13), 3266489909);
      return (h ^= h >>> 16) >>> 0;
    };
  }
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const rngFrom = str => mulberry32(xmur3(str)());

  function shuffle(arr, rnd) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(rnd() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  /* ───────────── 2. בחירה יומית (shuffle bag) ─────────────
   * מדמה את כל הימים מיום 0 ועד היום. זול (מאות ימים × ~16 פריטים) ונותן:
   *  - אפס חזרות ביום, ואפס חזרות ביום שאחריו
   *  - מגבלת פריטים לאותו badge (cap) ואותו מקור תמונה (uniqueFn) - עם "הרפיה" אם המאגר קטן מדי
   */
  function pickDaily(items, o) {
    const take = Math.min(o.take, items.length);
    if (take >= items.length) return items.slice();
    const capBase = o.cap || Infinity;
    let bag = [], refills = 0, last = [], result = [];

    for (let d = 0; d <= o.dayIndex; d++) {
      const picks = [], counts = Object.create(null), seenU = new Set();
      let relaxed = false;

      const grab = () => {
        for (let i = 0; i < bag.length && picks.length < take;) {
          const it = bag[i];
          const k = o.keyFn ? o.keyFn(it) : '';
          const u = !relaxed && o.uniqueFn ? o.uniqueFn(it) : null;
          const capOk = relaxed || (counts[k] || 0) < capBase;
          if (capOk && !(u && seenU.has(u))) {
            picks.push(it);
            counts[k] = (counts[k] || 0) + 1;
            if (u) seenU.add(u);
            bag.splice(i, 1);
          } else i++;
        }
      };

      grab();
      let stalls = 0;
      while (picks.length < take && stalls < 6) {
        const inBag = new Set(bag), inPicks = new Set(picks);
        let fresh = items.filter(it => !inBag.has(it) && !inPicks.has(it));
        if (fresh.length) {
          shuffle(fresh, rngFrom(o.salt + ':bag:' + (refills++)));
          const lastSet = new Set(last); // מה שהוצג אתמול - לסוף התור, כדי שלא יחזור מיד
          fresh = fresh.filter(x => !lastSet.has(x)).concat(fresh.filter(x => lastSet.has(x)));
          bag = bag.concat(fresh);
        }
        const before = picks.length;
        grab();
        if (picks.length === before) { stalls++; if (stalls >= 2) relaxed = true; }
      }
      last = picks;
      result = picks;
    }
    return result;
  }

  /* ───────────── 3. סרטונים ───────────── */

  function ytId(s) {
    if (!s) return null;
    if (/^[\w-]{11}$/.test(s)) return s;
    const m = String(s).match(/(?:v=|youtu\.be\/|embed\/|shorts\/)([\w-]{11})/);
    return m ? m[1] : null;
  }

  // מקבל רשומת וידאו ({id|url, platform}) ומחזיר כתובת embed תקינה
  function embedUrl(v) {
    const p = (v.platform || (v.url && /tiktok\.com/.test(v.url) ? 'tiktok' : v.url && /instagram\.com/.test(v.url) ? 'instagram' : 'youtube'));
    if (p === 'tiktok') {
      const u = v.url || '';
      const id = (u.match(/video\/(\d+)/) || u.match(/embed\/v2\/(\d+)/) || [])[1] || (/^\d+$/.test(v.id || '') ? v.id : null);
      return id ? 'https://www.tiktok.com/embed/v2/' + id : v.url;
    }
    if (p === 'instagram') {
      const m = (v.url || '').match(/instagram\.com\/(p|reel|tv)\/([\w-]+)/);
      return m ? 'https://www.instagram.com/' + m[1] + '/' + m[2] + '/embed' : v.url;
    }
    const id = ytId(v.id) || ytId(v.url);
    return id ? 'https://www.youtube-nocookie.com/embed/' + id + '?rel=0&modestbranding=1&playsinline=1' : null;
  }

  function sanitizeVideos(list) {
    const seen = new Set(), out = [];
    (Array.isArray(list) ? list : []).forEach(v => {
      if (!v || typeof v !== 'object') return;
      const e = embedUrl(v);
      if (!e || seen.has(e)) return;
      seen.add(e);
      out.push(Object.assign({}, v, { embed: e }));
    });
    return out;
  }

  // כרטיסייה = סרטון אחד ייחודי. העדפה להתאמת topic, אחרת כל סרטון פנוי.
  function assignVideos(cards, dayVideos, rnd) {
    if (!dayVideos.length) return;
    const pool = shuffle(dayVideos.slice(), rnd);
    const used = new Set();
    shuffle(cards.map((_, i) => i), rnd).forEach((ci, n) => {
      const c = cards[ci];
      if (c.lockVideo && c.videoUrl) return;
      let v = pool.find(x => !used.has(x) && c.topic && x.topic === c.topic) || pool.find(x => !used.has(x));
      if (!v) v = pool[n % pool.length]; // מאגר קטן מדי => חוזרים (עדיף על כרטיסייה ריקה)
      used.add(v);
      c.videoUrl = v.embed;
      c.videoMeta = { title: v.title, channel: v.channel, platform: v.platform || 'youtube' };
    });
  }

  /* ───────────── 4. סידור + פריסה ───────────── */

  function sanitizeContent(list) {
    const seen = new Set(), out = [];
    (Array.isArray(list) ? list : []).forEach(it => {
      if (!it || !it.title || seen.has(it.title)) return;
      seen.add(it.title);
      const c = Object.assign({ layer: 'top', type: 'image', badge: 'Trend', sub: '', height: 160, styleClass: 'card-pinterest-style' }, it);
      delete c.left; delete c.top; delete c.rot; // מיקום נוצר יומית - מתעלמים ממה שנשמר בקובץ
      out.push(c);
    });
    return out;
  }

  // סדר קריאה (משמש גם למובייל, שם CSS גריד של 2 בשורה):
  // כרטיס-פתיחה חזק (וידאו/מגזין), אחר כך זוגות בגובה דומה בלי badge זהה בשורה או בשורה שמעל.
  function orderForGrid(items, rnd) {
    const pool = shuffle(items.slice(), rnd);
    const heroes = pool.filter(x => x.type === 'video' || x.magazineName);
    if (heroes.length) {
      const h = heroes[Math.floor(rnd() * heroes.length)];
      pool.splice(pool.indexOf(h), 1); pool.unshift(h);
    }
    const out = [];
    while (pool.length) {
      const a = pool.shift(); out.push(a);
      if (!pool.length) break;
      const above = [out[out.length - 3], out[out.length - 2]].filter(Boolean);
      let best = 0, bestScore = Infinity;
      for (let i = 0; i < Math.min(6, pool.length); i++) {
        const b = pool[i];
        let s = Math.abs((b.height || 160) - (a.height || 160));
        if (b.badge === a.badge) s += 200;
        if (above.some(x => x.badge === b.badge)) s += 90;
        if (s < bestScore) { bestScore = s; best = i; }
      }
      out.push(pool.splice(best, 1)[0]);
    }
    return out;
  }

  function cardSize(it) {
    const cls = it.styleClass || '';
    if (it.type === 'vinyl' || cls.includes('card-vinyl-standalone')) return { w: 190, h: 214 };
    const w = cls.includes('card-magazine-clean') ? 240 : 250;
    const extra = it.magazineName ? 26 : it.igUser ? 18 : 0;
    return { w, h: (it.height || 160) + 50 + extra };
  }

  // קולאז' בשכבות: 2 עמודות "רופפות", גלישה אנכית קלה, הסטת X, סיבוב אקראי. רקע = חופף יותר.
  function layoutDesktop(items, rnd, o) {
    o = o || {};
    const width = o.width || 750, pad = o.pad || 20;
    const cols = o.cols || (width >= 1000 ? 3 : 2), maxW = 250;
    const span = width - 2 * pad - maxW;
    const step = span / (cols - 1) * (o.squeeze || 0.82);
    const start = pad + (span - step * (cols - 1)) / 2;
    const bottoms = Array.from({ length: cols }, (_, i) => (i === 0 ? 0 : 50 + rnd() * 110));
    let maxBottom = 0;

    const placed = items.map(it => {
      const { w, h } = cardSize(it);
      let c = 0, best = Infinity;
      for (let i = 0; i < cols; i++) {
        const s = bottoms[i] + rnd() * 45;
        if (s < best) { best = s; c = i; }
      }
      const left = clamp(start + c * step + (maxW - w) / 2 + (rnd() - 0.5) * 28, 6, width - w - 6);
      const gap = it.layer === 'background' ? -(8 + rnd() * 28) : -10 + rnd() * 34;
      const top = bottoms[c] === 0 ? 8 + rnd() * 10 : bottoms[c] + gap;
      bottoms[c] = top + h;
      maxBottom = Math.max(maxBottom, bottoms[c]);
      const rot = (rnd() < 0.5 ? -1 : 1) * (0.5 + rnd() * 1.8);
      return Object.assign({}, it, { pos: { left: Math.round(left), top: Math.round(top), rot: +rot.toFixed(2) } });
    });
    return { items: placed, height: Math.round(maxBottom + 30) };
  }

  function layoutLabels(labels, height, width, rnd) {
    labels = labels || [];
    const slice = height / (labels.length + 1);
    return labels.map((l, i) => Object.assign({}, l, {
      top: Math.round(slice * (i + 1) + (rnd() - 0.5) * slice * 0.5),
      left: Math.round(width / 2 - 75 + (rnd() - 0.5) * 120),
      rot: +((rnd() < 0.5 ? -1 : 1) * (0.8 + rnd() * 1.6)).toFixed(2)
    }));
  }

  /* ───────────── 5. הרכבה ───────────── */

  /**
   * compose({ content, videos }, opts) -> { dateKey, dayIndex, items, labels, height, stats }
   * opts: { count=16, width=750, tz, date, labels }
   */
  function compose(data, opts) {
    opts = opts || {};
    const key = dateKey(opts), di = dayIndex(key);
    const content = sanitizeContent(data.content);
    const videos = sanitizeVideos(data.videos);
    const count = Math.min(opts.count || 16, content.length);

    const picked = pickDaily(content, {
      take: count, dayIndex: di, salt: 'content',
      keyFn: x => x.badge, cap: Math.max(2, Math.ceil(count / 4)),
      uniqueFn: x => x.source || null
    });
    const dayVideos = videos.length ? pickDaily(videos, { take: count, dayIndex: di, salt: 'video' }) : [];

    const rnd = rngFrom(key + ':layout');
    const ordered = orderForGrid(picked, rnd);
    assignVideos(ordered, dayVideos, rnd);
    const lay = layoutDesktop(ordered, rnd, { width: opts.width || 750 });
    const labels = layoutLabels(opts.labels, lay.height, opts.width || 750, rnd);

    return {
      dateKey: key, dayIndex: di, items: lay.items, labels, height: lay.height,
      stats: { pool: content.length, videoPool: videos.length, shown: lay.items.length, uniqueVideos: new Set(lay.items.map(i => i.videoUrl)).size }
    };
  }

  /* ───────────── 6. טעינה (Vercel same-origin, עם fallback) ───────────── */

  async function fetchJson(url, version) {
    const r = await fetch(url + (url.includes('?') ? '&' : '?') + 'v=' + encodeURIComponent(version), { cache: 'no-cache' });
    if (!r.ok) throw new Error(url + ' -> ' + r.status);
    return r.json();
  }

  async function load(o) {
    o = o || {};
    const v = o.version || dateKey(o);
    let content = [], videos = [];
    if (typeof fetch === 'function') {
      try { content = await fetchJson(o.contentUrl || 'trends-data.json', v); }
      catch (e) { console.warn('[DailyEngine] content pool נכשל, משתמש ב-fallback:', e.message); }
      try { videos = await fetchJson(o.videoUrl || 'video-pool.json', v); }
      catch (e) { console.warn('[DailyEngine] video pool נכשל, משתמש ב-fallback:', e.message); }
    }
    // איחוד עם ה-fallback המוטמע (לפי title) - יותר מגוון, וגם עובד כשפותחים את הקובץ מהדיסק (file://)
    const merged = sanitizeContent([].concat(Array.isArray(content) ? content : [], o.fallbackContent || []));
    const vids = sanitizeVideos([].concat(Array.isArray(videos) ? videos : [], (Array.isArray(videos) && videos.length) ? [] : (o.fallbackVideos || [])));
    if (vids.length < (o.count || 16)) {
      console.warn('[DailyEngine] במאגר הסרטונים ' + vids.length + ' סרטונים בלבד - סרטונים יחזרו בין כרטיסיות. הריצו update_site.py.');
    }
    return { content: merged, videos: vids };
  }

  return { compose, load, dateKey, dayIndex, embedUrl, _internals: { pickDaily, orderForGrid, layoutDesktop, rngFrom, sanitizeContent, sanitizeVideos } };
});
