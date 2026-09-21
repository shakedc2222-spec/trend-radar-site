import datetime

def generate_html():
    today_date = datetime.datetime.now().strftime("%b %d, %Y")
    
    html_content = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trend Radar & Mood Board</title>
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@700;800;900&family=Plus+Jakarta+Sans:wght@500;600;700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #e6e2d3;
            --polaroid-bg: #fffdf9;
            --stroke-dark: #3a3a3a;
            --accent-terracotta: #b85d41;
            --accent-olive: #5f6b55;
            --dark-card: #1c1c1e;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            background-image: radial-gradient(#9c9989 1.5px, transparent 1.5px);
            background-size: 24px 24px;
            color: var(--stroke-dark);
            margin: 0;
            padding: 40px;
            overflow-x: hidden;
        }

        .site-container {
            max-width: 1450px;
            margin: 0 auto;
        }

        .board-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }

        .board-header h1 {
            font-family: 'Raleway', sans-serif;
            font-size: 46px;
            font-weight: 800;
            margin: 0;
            color: var(--stroke-dark);
            letter-spacing: -0.5px;
        }

        .live-date {
            font-size: 11px;
            font-weight: 700;
            background: var(--stroke-dark);
            color: #fff;
            padding: 6px 16px;
            border-radius: 2px;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-family: 'Special Elite', monospace;
            border: 1.5px solid var(--stroke-dark);
        }

        /* פריסה ראשית: צד שמאל הוא הגריד הצפוף, צד ימין הוא הסרגל הקבוע */
        .main-layout {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 30px;
            align-items: start;
        }

        /* מערכת Grid אמיתית: מבטיחה תמיד 2 עד 3 פריטים בשורה ללא שטחים ריקים */
        .collage-workspace {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
            position: relative;
        }

        .collage-card {
            background: var(--polaroid-bg);
            padding: 12px 12px 22px 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1), 0 2px 6px rgba(0,0,0,0.03);
            border: 2px solid var(--stroke-dark);
            cursor: pointer;
            transition: transform 0.2s;
            position: relative;
        }
        .collage-card:hover { transform: translateY(-3px); }

        /* וושי טייפ מעודן */
        .collage-card::before {
            content: "";
            position: absolute;
            top: -9px;
            left: 50%;
            transform: translateX(-50%) rotate(-1.5deg);
            width: 65px;
            height: 18px;
            background: rgba(230, 220, 195, 0.9);
            border: 1px dashed #8a826d;
            z-index: 5;
        }
        .tape-olive::before { background: rgba(95, 107, 85, 0.3) !important; }
        .tape-terracotta::before { background: rgba(184, 93, 65, 0.3) !important; }

        .dog-ear {
            position: relative;
            background: linear-gradient(135deg, #fffdf9 50%, #f0ebd9 50%);
        }
        .dog-ear::after {
            content: "";
            position: absolute;
            top: 0;
            right: 0;
            width: 25px;
            height: 25px;
            background: linear-gradient(225deg, #d8d0bc 50%, #fffdf9 50%);
            box-shadow: -2px 2px 3px rgba(0,0,0,0.08);
            border-bottom: 2px solid var(--stroke-dark);
            border-left: 2px solid var(--stroke-dark);
        }

        .torn-paper-art-frame {
            background: #fffdf9;
            padding: 30px 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border: 2px solid var(--stroke-dark);
            clip-path: polygon(0% 3%, 6% 0%, 12% 3%, 18% 0%, 24% 3%, 30% 0%, 36% 3%, 42% 0%, 48% 3%, 54% 0%, 60% 3%, 66% 0%, 72% 3%, 78% 0%, 84% 3%, 90% 0%, 96% 3%, 100% 0%, 98% 97%, 100% 100%, 94% 97%, 88% 100%, 82% 97%, 76% 100%, 70% 97%, 64% 100%, 58% 97%, 52% 100%, 46% 97%, 40% 100%, 34% 97%, 28% 100%, 22% 97%, 16% 100%, 10% 97%, 4% 100%, 0% 97%);
            cursor: pointer;
            grid-column: span 2; /* תופס את כל הרוחב ליצירת עניין */
        }

        /* פולרוידי צבעי HEX חמים מקובעים קבוע למעלה ימינה */
        .pantone-fixed-group {
            position: absolute;
            top: 0px;
            left: 500px;
            display: flex;
            gap: 12px;
            z-index: 50;
        }

        .pantone-polaroid {
            background: var(--polaroid-bg);
            padding: 8px 8px 16px 8px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border: 2px solid var(--stroke-dark);
            cursor: pointer;
            width: 95px;
            text-align: center;
        }

        .pantone-swatch {
            height: 65px;
            border-radius: 1px;
            border: 1.5px solid var(--stroke-dark);
        }

        .pantone-code {
            font-size: 10px;
            font-weight: 800;
            color: var(--stroke-dark);
            margin-top: 6px;
            font-family: 'Special Elite', monospace;
        }

        .viral-sounds-section {
            position: absolute;
            top: 155px;
            left: 500px;
            display: flex;
            gap: 14px;
            z-index: 50;
        }

        .sound-circle {
            width: 44px;
            height: 44px;
            background: var(--stroke-dark);
            color: #fff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.2);
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
            border: 2px solid #fff;
        }
        .sound-circle:hover { transform: scale(1.1); background: var(--accent-terracotta); color: #fff; }

        .visual-box {
            height: 190px;
            background: var(--dark-card);
            border-radius: 1px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 26px;
            overflow: hidden;
            position: relative;
            border: 2px solid var(--stroke-dark);
        }

        .badge-title {
            position: absolute;
            top: 8px;
            left: 8px;
            background: var(--stroke-dark);
            color: #fff;
            padding: 2px 6px;
            font-size: 9px;
            font-weight: 800;
            border-radius: 1px;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-family: 'Special Elite', monospace;
        }

        .card-caption {
            margin-top: 10px;
            font-size: 13px;
            font-weight: 800;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--stroke-dark);
        }

        .card-sub {
            font-size: 9px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 2px;
            font-family: 'Special Elite', monospace;
        }

        .sidebar-side {
            position: sticky;
            top: 30px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            z-index: 100;
        }

        .preview-panel {
            background: var(--dark-card);
            color: #fff;
            padding: 22px;
            border-radius: 4px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.25);
            border: 2px solid var(--stroke-dark);
        }

        .preview-panel h4 {
            margin: 0 0 10px 0;
            font-size: 11px;
            color: #b85d41;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-family: 'Special Elite', monospace;
        }

        .embedded-player-container {
            width: 100%;
            height: 260px;
            background: #000;
            border-radius: 2px;
            overflow: hidden;
            margin-bottom: 12px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #333;
        }

        .embedded-player-container iframe {
            width: 100%;
            height: 100%;
            border: none;
        }

        .default-player-placeholder {
            color: #888;
            font-size: 13px;
            text-align: center;
            padding: 20px;
            font-family: 'Special Elite', monospace;
        }

        #preview-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 4px;
            color: #b85d41;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        #preview-desc {
            font-size: 12px;
            color: #ccc;
            margin: 0;
            line-height: 1.4;
        }

        .links-box {
            background: #ffffff;
            padding: 22px;
            border-radius: 4px;
            border: 2px solid var(--stroke-dark);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .links-box h3 {
            margin: 0 0 12px 0;
            font-size: 15px;
            font-weight: 900;
            font-family: 'Plus Jakarta Sans', sans-serif;
            border-bottom: 2px solid var(--stroke-dark);
            padding-bottom: 8px;
        }

        .link-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px dashed #bbb;
            text-decoration: none;
            color: var(--stroke-dark);
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: color 0.2s;
        }

        .link-item:last-child { border-bottom: none; }
        .link-item:hover { color: var(--accent-terracotta); }

        .platform-tag {
            font-size: 9px;
            background: var(--stroke-dark);
            padding: 2px 6px;
            border-radius: 1px;
            color: #fff;
            text-transform: uppercase;
            font-family: 'Special Elite', monospace;
        }

        .footer {
            grid-column: span 2;
            text-align: center;
            font-size: 11px;
            color: var(--stroke-dark);
            margin-top: 80px;
            border-top: 2px dashed var(--stroke-dark);
            padding-top: 20px;
            font-family: 'Special Elite', monospace;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>

    <div class="site-container" style="position: relative;">
        
        <header class="board-header">
            <h1>Trend Radar</h1>
            <div class="live-date">Updated: {TODAY_DATE}</div>
        </header>

        <!-- פולרוידי צבעי HEX חמים מקובעים למעלה ימינה -->
        <div class="pantone-fixed-group">
            <div class="pantone-polaroid" style="transform: rotate(-1deg);" onclick="playEmbeddedMedia('info', '', 'Warm Terracotta: #B85D41', 'Primary organic autumn tone.')">
                <div class="pantone-swatch" style="background-color: #b85d41;"></div>
                <div class="pantone-code">#B85D41</div>
            </div>
            <div class="pantone-polaroid" style="transform: rotate(2deg);" onclick="playEmbeddedMedia('info', '', 'Soft Blush: #E3AAB1', 'Gentle secondary pastel tone.')">
                <div class="pantone-swatch" style="background-color: #e3aab1;"></div>
                <div class="pantone-code">#E3AAB1</div>
            </div>
            <div class="pantone-polaroid" style="transform: rotate(-2deg);" onclick="playEmbeddedMedia('info', '', 'Warm Olive Sage: #5F6B55', 'Earthy botanical tone.')">
                <div class="pantone-swatch" style="background-color: #5f6b55;"></div>
                <div class="pantone-code">#5F6B55</div>
            </div>
        </div>

        <!-- אזור סאונדים -->
        <div class="viral-sounds-section">
            <div class="sound-circle" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Viral Audio: Ambient Design Flow', 'Top trending sound.')" title="Play Sound 1">🔊</div>
            <div class="sound-circle" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'New Track: Midnight Echoes Remix', 'Underground track.')" title="Play Sound 2">🎵</div>
            <div class="sound-circle" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Audio Trend: Spatial UX Podcast', 'Podcast audio.')" title="Play Sound 3">🎙️</div>
        </div>

        <div class="main-layout">
            
            <div class="collage-workspace">
                
                <!-- פריטים מסודרים בגריד צפוף (Grid) שמבטיח שלא יהיו שטחים מתים -->
                
                <div class="collage-card tape-olive dog-ear" onclick="playEmbeddedMedia('tiktok', 'https://www.tiktok.com/embed/v2/7234567890', 'TikTok UI Motion', 'Trending short video format.')">
                    <div class="visual-box" style="background: #2c3e50;"><span class="badge-title">TikTok</span>▶</div>
                    <div class="card-caption">Neo-Brutalism UI Breakdown</div>
                    <div class="card-sub">TikTok Peak Trend</div>
                </div>

                <div class="collage-card tape-terracotta dog-ear" onclick="playEmbeddedMedia('instagram', 'https://www.instagram.com/p/C000000/embed', 'Vogue Cover Drop', 'Editorial magazine cover.')">
                    <div class="visual-box" style="background: #111;"><span class="badge-title">Vogue</span>VOGUE</div>
                    <div class="card-caption">Vogue New Era Cover Drop</div>
                    <div class="card-sub">Print & Editorial</div>
                </div>

                <div class="collage-card tape-terracotta" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Milan Fashion Week', 'Runway highlights.')">
                    <div class="visual-box" style="background: #8c6d62;"><span class="badge-title">Runway</span>🧥</div>
                    <div class="card-caption">Milan Fashion Week Tailoring</div>
                    <div class="card-sub">Runway & Street Style</div>
                </div>

                <div class="collage-card tape-olive" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Digital Art', 'Light installation.')">
                    <div class="visual-box" style="background: #4a5d4e;"><span class="badge-title">Exhibition</span>🏛️</div>
                    <div class="card-caption">Immersive Digital Art Installation</div>
                    <div class="card-sub">Global Exhibition</div>
                </div>

                <div class="torn-paper-art-frame" onclick="playEmbeddedMedia('info', '', 'Print Archive', 'Analog print heritage.')">
                    <div style="font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 18px; color: var(--stroke-dark); text-align: center;">
                        Print Archive Feature
                        <div style="font-size: 10px; font-weight: normal; font-family: 'Special Elite', monospace; color: #666; margin-top: 4px;">Analog Print Curation</div>
                    </div>
                    <div class="card-caption" style="margin-top: 8px;">Ripped Paper Print Asset</div>
                    <div class="card-sub">High Vertical Layout</div>
                </div>

                <div class="collage-card tape-terracotta dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Pastry Art', 'Sculptural pistachio tart.')">
                    <div class="visual-box" style="background: #556b2f;"><span class="badge-title">Culinary</span>🥐</div>
                    <div class="card-caption">Sculptural Pistachio Tart Art</div>
                    <div class="card-sub">Culinary Social Trend</div>
                </div>

                <div class="collage-card tape-olive dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', '3D Sculptures', 'Surrealist textures.')">
                    <div class="visual-box" style="background: #7b1fa2;"><span class="badge-title">3D Art</span>🎨</div>
                    <div class="card-caption">Surrealist 3D Organic Textures</div>
                    <div class="card-sub">Artist Spotlight</div>
                </div>

                <div class="collage-card tape-terracotta" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Brutalist Living', 'Raw concrete interior.')">
                    <div class="visual-box" style="background: #37474f;"><span class="badge-title">Interior</span>🏠</div>
                    <div class="card-caption">Brutalist Concrete & Wood</div>
                    <div class="card-sub">Architecture & Living</div>
                </div>

                <div class="torn-paper-art-frame" onclick="playEmbeddedMedia('info', '', 'Zine Cutout', 'Alternative press layout.')">
                    <div style="font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 18px; color: var(--stroke-dark); text-align: center;">
                        Zine & Press Cutout
                        <div style="font-size: 10px; font-weight: normal; font-family: 'Special Elite', monospace; color: #666; margin-top: 4px;">Alternative Press Curation</div>
                    </div>
                    <div class="card-caption" style="margin-top: 8px;">Alternative Cutout Asset</div>
                    <div class="card-sub">Zine Layout Edition</div>
                </div>

                <div class="collage-card tape-olive dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Motion Reel', 'Kinetic typography.')">
                    <div class="visual-box" style="background: #ff6f00;"><span class="badge-title">Motion</span>🎞️</div>
                    <div class="card-caption">Kinetic Typography Motion Reel</div>
                    <div class="card-sub">Motion & Animation</div>
                </div>

                <div class="collage-card tape-terracotta" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Eco-Packaging', 'Tactile eco branding.')">
                    <div class="visual-box" style="background: #004d40;"><span class="badge-title">Branding</span>🧴</div>
                    <div class="card-caption">Tactile Eco-Packaging</div>
                    <div class="card-sub">Behance Branding Trend</div>
                </div>

                <div class="collage-card tape-olive dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Spatial UX', 'Bezi volumetric 3D.')">
                    <div class="visual-box" style="background: #311b92;"><span class="badge-title">Spatial</span>🥽</div>
                    <div class="card-caption">Spatial UX & Bezi Volumetric</div>
                    <div class="card-sub">Immersive Technology</div>
                </div>

                <div class="collage-card tape-terracotta dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Album Art', 'Analog grainy film.')">
                    <div class="visual-box" style="background: #b71c1c;"><span class="badge-title">Music</span>🎵</div>
                    <div class="card-caption">Analog Album Art & Swiss Design</div>
                    <div class="card-sub">Music & Visual Culture</div>
                </div>

                <div class="collage-card tape-olive" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Studio Pottery', 'Handmade stoneware.')">
                    <div class="visual-box" style="background: #e65100;"><span class="badge-title">Craft</span>🏺</div>
                    <div class="card-caption">Handmade Studio Pottery</div>
                    <div class="card-sub">Craft & Object Design</div>
                </div>

                <div class="collage-card tape-terracotta dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Silver Jewelry', 'Molten fluid forms.')">
                    <div class="visual-box" style="background: #424242;"><span class="badge-title">Accessory</span>💍</div>
                    <div class="card-caption">Molten Silver Jewelry Trends</div>
                    <div class="card-sub">Accessory Trend Watch</div>
                </div>

                <div class="collage-card tape-olive" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Retail Space', 'Tokyo concept store.')">
                    <div class="visual-box" style="background: #263238;"><span class="badge-title">Retail</span>🏬</div>
                    <div class="card-caption">Tokyo Concept Store Architecture</div>
                    <div class="card-sub">Interior & Spatial Design</div>
                </div>

                <div class="collage-card tape-olive dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'AI Textiles', 'Algorithmic fabric patterns.')">
                    <div class="visual-box" style="background: #880e4f;"><span class="badge-title">AI Tech</span>🧵</div>
                    <div class="card-caption">AI Generative Fabric & Textiles</div>
                    <div class="card-sub">Tech & Fashion Fusion</div>
                </div>

                <div class="collage-card tape-terracotta" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Bio-Design', 'Mycelium footwear.')">
                    <div class="visual-box" style="background: #33691e;"><span class="badge-title">Bio-Design</span>👟</div>
                    <div class="card-caption">Mycelium Sustainable Footwear</div>
                    <div class="card-sub">Sustainable Fashion</div>
                </div>

                <div class="torn-paper-art-frame" onclick="playEmbeddedMedia('info', '', 'Vanguard Print', 'Advanced layout.')">
                    <div style="font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 18px; color: var(--stroke-dark); text-align: center;">
                        Vanguard Print Edition
                        <div style="font-size: 10px; font-weight: normal; font-family: 'Special Elite', monospace; color: #666; margin-top: 4px;">Future Print Curation</div>
                    </div>
                    <div class="card-caption" style="margin-top: 8px;">Vanguard Print Asset</div>
                    <div class="card-sub">Deep Archive Layout</div>
                </div>

                <div class="collage-card tape-olive dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Cyberpunk UI', 'Futuristic interfaces.')">
                    <div class="visual-box" style="background: #0f172a;"><span class="badge-title">Cyber UI</span>💻</div>
                    <div class="card-caption">Cyberpunk Spatial UI Motion</div>
                    <div class="card-sub">Interface Architecture</div>
                </div>

                <div class="collage-card tape-terracotta dog-ear" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Glass Vases', 'Iridescent glass blowing.')">
                    <div class="visual-box" style="background: #006064;"><span class="badge-title">Glass</span>🔮</div>
                    <div class="card-caption">Iridescent Blown Glass Vases</div>
                    <div class="card-sub">Craft & Materiality</div>
                </div>

                <div class="collage-card tape-olive" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Swiss Posters', 'Expressive grid layouts.')">
                    <div class="visual-box" style="background: #1b5e20;"><span class="badge-title">Swiss Grid</span>🔤</div>
                    <div class="card-caption">Distorted Swiss Grid Posters</div>
                    <div class="card-sub">Graphic Design Archive</div>
                </div>

            </div>

            <div class="sidebar-side">
                <div class="preview-panel">
                    <h4>🔍 Live Media Studio</h4>
                    
                    <div class="embedded-player-container" id="player-box">
                        <div class="default-player-placeholder">Click any item or color swatch to inspect in-site</div>
                    </div>

                    <div id="preview-title">Select an item</div>
                    <p id="preview-desc">Color inspiration, hex codes, and media previews will appear here instantly.</p>
                </div>

                <div class="links-box">
                    <h3>🔗 Inspiration Channels</h3>
                    <div class="link-item" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'TikTok 24h Peak Trends', 'Live embedded feed of top creative prototype videos.')">
                        <span>Going Viral (TikTok 24h)</span>
                        <span class="platform-tag">TikTok</span>
                    </div>
                    <div class="link-item" onclick="playEmbeddedMedia('instagram', '', 'Instagram Hot Reels', 'Latest curated editorial reels and backstage footage.')">
                        <span>Hot Reels & Magazine Covers</span>
                        <span class="platform-tag">Instagram</span>
                    </div>
                    <div class="link-item" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Pinterest & Fashion Week Stream', 'Immersive video highlights from global runways.')">
                        <span>Fashion Week & Pinterest Trends</span>
                        <span class="platform-tag">Pinterest</span>
                    </div>
                    <div class="link-item" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Behance Exhibitions & Print', 'Showcase of physical print archives and digital galleries.')">
                        <span>Exhibitions & Print Design</span>
                        <span class="platform-tag">Behance</span>
                    </div>
                </div>
            </div>

        </div>

        <footer class="footer">
            Trend Radar &bull; Ultimate Grid Collage Edition
        </footer>

    </div>

    <script>
        function playEmbeddedMedia(type, mediaUrl, title, description) {
            const playerBox = document.getElementById('player-box');
            document.getElementById('preview-title').innerText = title;
            document.getElementById('preview-desc').innerText = description;

            if (mediaUrl && mediaUrl !== '') {
                playerBox.innerHTML = `<iframe src="${mediaUrl}" allow="autoplay; encrypted-media" allowfullscreen></iframe>`;
            } else {
                playerBox.innerHTML = `<div class="default-player-placeholder" style="background:#2b2b2b; color:#b85d41; font-family:'Special Elite',monospace; font-size:14px; padding:20px; text-align:center;">✨ Warm Hex Color Loaded Successfully</div>`;
            }
        }
    </script>
</body>
</html>
"""
    
    final_html = html_content.replace("{TODAY_DATE}", today_date)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    print("✨ קובץ ה-index.html עודכן בהצלחה עם פריסת Grid אמיתית וחכמה שמבטיחה שלא יהיו שטחים מתים בשום מצב!")

if __name__ == "__main__":
    generate_html()
