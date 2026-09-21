import datetime

def generate_html():
    today_date = datetime.datetime.now().strftime("%b %d, %Y")
    
    html_content = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shaked's Ultimate Trend Radar & Mood Board</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #e8e2d5;
            --polaroid-bg: #fffbf2;
            --text-main: #111;
            --accent-pink: #ff3399;
            --accent-blue: #3b82f6;
            --dark-card: #1c1c1e;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            background-image: radial-gradient(#d5cebc 1px, transparent 1px);
            background-size: 24px 24px;
            color: var(--text-main);
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
            margin-bottom: 40px;
            border-bottom: 3px solid #111;
            padding-bottom: 15px;
        }

        .board-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 46px;
            font-weight: 900;
            font-style: italic;
            margin: 0;
            color: #111;
            letter-spacing: -1px;
        }

        .live-date {
            font-size: 13px;
            font-weight: 700;
            background: #111;
            color: #fff;
            padding: 6px 16px;
            border-radius: 4px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .main-layout {
            display: grid;
            grid-template-columns: 1fr 400px;
            gap: 40px;
            align-items: start;
        }

        /* מרחב קולאז' פראי ועמוק עם חפיפות */
        .collage-workspace {
            position: relative;
            min-height: 4500px;
        }

        /* בסיס לכל כרטיסיית קולאז' בסגנון פולרויד / עיתון גזור */
        .collage-card {
            position: absolute;
            background: var(--polaroid-bg);
            padding: 14px 14px 28px 14px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.18), 0 5px 15px rgba(0,0,0,0.08);
            border: 1px solid #dcd4c0;
            cursor: pointer;
            width: 270px;
            transition: z-index 0.2s;
        }
        .collage-card:hover { z-index: 100 !important; }

        /* סרטי הדבקה (Washi Tape) בפינות הכרטיסיות */
        .collage-card::before {
            content: "";
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%) rotate(-2deg);
            width: 70px;
            height: 20px;
            background: rgba(255, 235, 150, 0.85);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            z-index: 5;
        }

        .tape-blue::before { background: rgba(147, 197, 253, 0.85) !important; transform: translateX(-50%) rotate(3deg) !important; }
        .tape-pink::before { background: rgba(252, 165, 165, 0.85) !important; transform: translateX(-50%) rotate(-1deg) !important; }

        /* פולרוידים של פנטון בעיצוב עיתונות ניאוני */
        .pantone-polaroid {
            position: absolute;
            background: var(--polaroid-bg);
            padding: 10px 10px 20px 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.12);
            border: 1px solid #dcd4c0;
            cursor: pointer;
            width: 110px;
            text-align: center;
            z-index: 10;
        }

        .pantone-swatch {
            height: 80px;
            border-radius: 2px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
        }

        .pantone-code {
            font-size: 10px;
            font-weight: 800;
            color: #111;
            margin-top: 8px;
            font-family: 'Special Elite', monospace;
        }

        /* מסגרת נייר קרוע אמנותית (Zine style) */
        .torn-paper-art-frame {
            position: absolute;
            background: #fff;
            padding: 35px 25px;
            box-shadow: 0 20px 45px rgba(0,0,0,0.2);
            border: none;
            clip-path: polygon(0% 3%, 6% 0%, 12% 3%, 18% 0%, 24% 3%, 30% 0%, 36% 3%, 42% 0%, 48% 3%, 54% 0%, 60% 3%, 66% 0%, 72% 3%, 78% 0%, 84% 3%, 90% 0%, 96% 3%, 100% 0%, 98% 97%, 100% 100%, 94% 97%, 88% 100%, 82% 97%, 76% 100%, 70% 97%, 64% 100%, 58% 97%, 52% 100%, 46% 97%, 40% 100%, 34% 97%, 28% 100%, 22% 97%, 16% 100%, 10% 97%, 4% 100%, 0% 97%);
            cursor: pointer;
            width: 290px;
        }

        .visual-box {
            height: 170px;
            background: var(--dark-card);
            border-radius: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 28px;
            overflow: hidden;
            position: relative;
            border: 1px solid #333;
        }

        .badge-title {
            position: absolute;
            top: 10px;
            left: 10px;
            background: #ff3399;
            color: #fff;
            padding: 3px 8px;
            font-size: 10px;
            font-weight: 800;
            border-radius: 2px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-family: 'Special Elite', monospace;
        }

        .card-caption {
            margin-top: 10px;
            font-size: 13px;
            font-weight: 800;
            font-family: 'Playfair Display', serif;
        }

        .card-sub {
            font-size: 10px;
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
            border-radius: 6px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.25);
            border: 2px solid #333;
        }

        .preview-panel h4 {
            margin: 0 0 10px 0;
            font-size: 11px;
            color: #ff3399;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-family: 'Special Elite', monospace;
        }

        .embedded-player-container {
            width: 100%;
            height: 260px;
            background: #000;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 12px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #444;
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
            color: #ff3399;
            font-family: 'Playfair Display', serif;
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
            border-radius: 6px;
            border: 2px solid #111;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .links-box h3 {
            margin: 0 0 12px 0;
            font-size: 15px;
            font-weight: 900;
            font-family: 'Playfair Display', serif;
            border-bottom: 2px solid #eee;
            padding-bottom: 8px;
        }

        .link-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px dashed #ddd;
            text-decoration: none;
            color: #111;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: color 0.2s;
        }

        .link-item:last-child { border-bottom: none; }
        .link-item:hover { color: var(--accent-pink); }

        .platform-tag {
            font-size: 9px;
            background: #111;
            padding: 2px 6px;
            border-radius: 2px;
            color: #fff;
            text-transform: uppercase;
            font-family: 'Special Elite', monospace;
        }

        .viral-sounds-section {
            position: absolute;
            top: 450px;
            left: 5px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            z-index: 50;
        }

        .sound-circle {
            width: 55px;
            height: 55px;
            background: #111;
            color: #ff3399;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
            border: 2px solid #fff;
        }
        .sound-circle:hover { transform: scale(1.1); background: #ff3399; color: #fff; }

        .footer {
            grid-column: span 2;
            text-align: center;
            font-size: 11px;
            color: #555;
            margin-top: 150px;
            border-top: 2px dashed #111;
            padding-top: 20px;
            font-family: 'Special Elite', monospace;
        }
    </style>
</head>
<body>

    <div class="site-container">
        
        <header class="board-header">
            <h1>Shaked's Trend Radar</h1>
            <div class="live-date">Updated: {TODAY_DATE}</div>
        </header>

        <div class="main-layout">
            
            <div class="collage-workspace">
                
                <!-- שורה 1: חופפים באמנותיות עם סרטטי הדבקה -->
                <div class="collage-card tape-blue" style="top: 0px; left: 15px; transform: rotate(-4deg); z-index: 3;" onclick="playEmbeddedMedia('tiktok', 'https://www.tiktok.com/embed/v2/7234567890', 'Going Viral Now: TikTok UI Motion', 'The absolute #1 trending short video format showcasing rapid Figma prototyping.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #ff3399, #3b82f6);"><span class="badge-title">Going Viral</span>▶</div>
                    <div class="card-caption">Neo-Brutalism UI Breakdown</div>
                    <div class="card-sub">TikTok 24h Peak Trend</div>
                </div>

                <div class="collage-card tape-pink" style="top: 25px; left: 300px; transform: rotate(3deg); z-index: 4;" onclick="playEmbeddedMedia('instagram', 'https://www.instagram.com/p/C000000/embed', 'Hot Instagram Reels: Vogue Cover Drop', 'Behind-the-scenes editorial reel of the latest groundbreaking magazine cover.')">
                    <div class="visual-box" style="background: #111;"><span class="badge-title">Hot IG</span>VOGUE</div>
                    <div class="card-caption">Vogue New Era Cover Drop</div>
                    <div class="card-sub">Print & Editorial IG Reel</div>
                </div>

                <!-- פולרוידי פנטון מעוצבים כגזרי עיתון -->
                <div class="pantone-polaroid" style="top: 10px; left: 595px; transform: rotate(-2deg);" onclick="playEmbeddedMedia('info', '', 'Pantone 18-1443: Terracotta Ochre', 'Primary organic autumn tone driving luxury branding, packaging, and interior styling.')">
                    <div class="pantone-swatch" style="background-color: #C86D51;"></div>
                    <div class="pantone-code">PANTONE<br>C86D51</div>
                </div>

                <div class="pantone-polaroid" style="top: 10px; left: 715px; transform: rotate(4deg);" onclick="playEmbeddedMedia('info', '', 'Pantone 13-1404: Soft Blush Dust', 'Gentle secondary pastel tone for delicate UI backgrounds and editorial fashion editorials.')">
                    <div class="pantone-swatch" style="background-color: #E3AAB1;"></div>
                    <div class="pantone-code">PANTONE<br>E3AAB1</div>
                </div>

                <div class="pantone-polaroid" style="top: 10px; left: 835px; transform: rotate(-1deg);" onclick="playEmbeddedMedia('info', '', 'Pantone 17-0618: Warm Olive Sage', 'Earthy botanical tone bridging digital interfaces, nature, and architectural spaces.')">
                    <div class="pantone-swatch" style="background-color: #8A9A86;"></div>
                    <div class="pantone-code">PANTONE<br>8A9A86</div>
                </div>

                <!-- שורה 2 -->
                <div class="collage-card tape-pink" style="top: 280px; left: 50px; transform: rotate(3deg); z-index: 5;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Milan Fashion Week Highlights', 'Sculptural silhouettes and structured blazers dominating international runways.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #8c6d62, #111);">🧥</div>
                    <div class="card-caption">Milan Fashion Week Highlights</div>
                    <div class="card-sub">Runway & Street Style</div>
                </div>

                <div class="collage-card tape-blue" style="top: 300px; left: 330px; transform: rotate(-2deg); z-index: 2;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Digital Art Installation', 'Contemporary digital light installation exploring boundaries.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #4a5d4e, #111);">🏛️</div>
                    <div class="card-caption">Digital Art Installation</div>
                    <div class="card-sub">Global Exhibition Drop</div>
                </div>

                <div class="collage-card" style="top: 260px; left: 610px; transform: rotate(2deg); z-index: 4;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Sculptural Pistachio Tart Trend', 'Architectural pastry taking over food design feeds.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #556b2f, #111);">🥐</div>
                    <div class="card-caption">Sculptural Pistachio Tart Art</div>
                    <div class="card-sub">Culinary Social Trend</div>
                </div>

                <!-- שורה 3: מסגרת נייר קרוע -->
                <div class="torn-paper-art-frame" style="top: 550px; left: 20px; transform: rotate(-2deg); z-index: 6;" onclick="playEmbeddedMedia('info', '', 'Print Archive: Ripped Paper Edition', 'Custom artistic ripped paper frame bridging analog print heritage with modern curation.')">
                    <div style="height: 150px; display: flex; flex-direction: column; justify-content: center; font-family: 'Playfair Display', serif; font-style: italic; font-size: 21px; color: #111; text-align: center;">
                        Print Archive Feature
                        <span style="font-size: 11px; font-style: normal; font-family: 'Special Elite', monospace; color: #555; margin-top: 8px;">Zine Culture & Typography</span>
                    </div>
                    <div class="card-caption" style="margin-top: 15px;">Expanded Ripped Paper Asset</div>
                    <div class="card-sub">High Vertical Layout</div>
                </div>

                <div class="collage-card tape-blue" style="top: 580px; left: 340px; transform: rotate(1.5deg); z-index: 4;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', '3D Surrealist Sculptures', 'New digital sculptures exploring organic textures.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #7b1fa2, #111);">🎨</div>
                    <div class="card-caption">Surrealist 3D Sculptures</div>
                    <div class="card-sub">Artist Spotlight</div>
                </div>

                <div class="collage-card tape-pink" style="top: 560px; left: 620px; transform: rotate(-3deg); z-index: 5;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Brutalist Interior Spaces', 'Raw concrete and warm wood interiors.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #37474f, #111);">🏠</div>
                    <div class="card-caption">Brutalist Interior Spaces</div>
                    <div class="card-sub">Architecture & Living</div>
                </div>

                <!-- שורה 4 -->
                <div class="collage-card tape-pink" style="top: 870px; left: 40px; transform: rotate(-1deg); z-index: 3;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Kinetic Typography Reel', 'Fluid motion graphics and rhythmic typography.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #ff6f00, #111);">🎞️</div>
                    <div class="card-caption">Kinetic Typography Reel</div>
                    <div class="card-sub">Motion & Animation</div>
                </div>

                <div class="collage-card tape-blue" style="top: 890px; left: 320px; transform: rotate(2.5deg); z-index: 4;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Tactile Eco-Packaging', 'Eco-friendly luxury branding with embossed typography.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #004d40, #111);">🧴</div>
                    <div class="card-caption">Tactile Eco-Packaging</div>
                    <div class="card-sub">Behance Branding Trend</div>
                </div>

                <div class="collage-card" style="top: 860px; left: 600px; transform: rotate(-2deg); z-index: 2;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Spatial UX & Bezi 3D', 'Immersive 3D interfaces and volumetric windows.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #311b92, #111);">🥽</div>
                    <div class="card-caption">Spatial UX & Bezi 3D</div>
                    <div class="card-sub">Immersive Technology</div>
                </div>

                <!-- שורה 5: מסגרת נייר קרוע שנייה -->
                <div class="collage-card tape-blue" style="top: 1140px; left: 30px; transform: rotate(2deg); z-index: 4;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Analog Album Art Design', 'Grainy film photography with Swiss typography.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #b71c1c, #111);">🎵</div>
                    <div class="card-caption">Analog Album Art Design</div>
                    <div class="card-sub">Music & Visual Culture</div>
                </div>

                <div class="collage-card tape-pink" style="top: 1160px; left: 310px; transform: rotate(-2.5deg); z-index: 3;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Handmade Studio Pottery', 'Hand-thrown ceramics featuring raw stoneware.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #e65100, #111);">🏺</div>
                    <div class="card-caption">Handmade Studio Pottery</div>
                    <div class="card-sub">Craft & Object Design</div>
                </div>

                <div class="torn-paper-art-frame" style="top: 1120px; left: 590px; transform: rotate(1.5deg); z-index: 6;" onclick="playEmbeddedMedia('info', '', 'Print Archive: Right Wing Edition', 'Balanced vertical print asset maintaining layout harmony.')">
                    <div style="height: 140px; display: flex; flex-direction: column; justify-content: center; font-family: 'Playfair Display', serif; font-style: italic; font-size: 20px; color: #111; text-align: center;">
                        Editorial Balance
                        <span style="font-size: 11px; font-style: normal; font-family: 'Special Elite', monospace; color: #555; margin-top: 6px;">Symmetrical Print Element</span>
                    </div>
                    <div class="card-caption" style="margin-top: 12px;">Right Balance Ripped Asset</div>
                    <div class="card-sub">Vertical Symmetry</div>
                </div>

                <!-- שורה 6 -->
                <div class="collage-card tape-pink" style="top: 1430px; left: 50px; transform: rotate(-3deg); z-index: 5;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Molten Silver Jewelry', 'Organic silver pieces inspired by fluid water forms.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #424242, #111);">💍</div>
                    <div class="card-caption">Molten Silver Jewelry</div>
                    <div class="card-sub">Accessory Trend Watch</div>
                </div>

                <div class="collage-card tape-blue" style="top: 1410px; left: 330px; transform: rotate(2deg); z-index: 3;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Tokyo Concept Store Retail', 'Concrete walls and floating clothing racks.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #263238, #111);">🏬</div>
                    <div class="card-caption">Tokyo Concept Store Retail</div>
                    <div class="card-sub">Interior & Spatial Design</div>
                </div>

                <!-- שורה 7 -->
                <div class="collage-card tape-blue" style="top: 1700px; left: 20px; transform: rotate(2.5deg); z-index: 4;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Bio-Design Footwear', 'Futuristic footwear crafted from mycelium and algae composites.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #33691e, #111);">👟</div>
                    <div class="card-caption">Bio-Design Footwear Trends</div>
                    <div class="card-sub">Sustainable Fashion</div>
                </div>

                <div class="collage-card tape-pink" style="top: 1680px; left: 300px; transform: rotate(-2deg); z-index: 3;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Editorial Grid Breaking', 'Asymmetrical layouts and overlapping typography in indie zines.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #b71c1c, #111);">📰</div>
                    <div class="card-caption">Indie Zine Grid Breaking</div>
                    <div class="card-sub">Editorial Print Design</div>
                </div>

                <div class="collage-card" style="top: 1710px; left: 590px; transform: rotate(1deg); z-index: 5;" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'AI Generative Textiles', 'Algorithmic fabric patterns generated via generative AI tools.')">
                    <div class="visual-box" style="background: linear-gradient(135deg, #880e4f, #111);">🧵</div>
                    <div class="card-caption">AI Generative Textiles</div>
                    <div class="card-sub">Tech & Fashion Fusion</div>
                </div>

                <div class="viral-sounds-section">
                    <div class="sound-circle" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Viral Audio: Ambient Design Flow', 'Top trending sound on TikTok & IG Reels.')" title="Play Sound 1">🔊</div>
                    <div class="sound-circle" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'New Track: Midnight Echoes Remix', 'Underground electronic track.')" title="Play Sound 2">🎵</div>
                    <div class="sound-circle" onclick="playEmbeddedMedia('youtube', 'https://www.youtube.com/embed/dQw4w9WgXcQ', 'Audio Trend: Spatial UX Podcast', 'Hot discussion on future spatial computing.')" title="Play Sound 3">🎙️</div>
                </div>

            </div>

            <div class="sidebar-side">
                <div class="preview-panel">
                    <h4>🔍 Live Pantone & Media Studio</h4>
                    
                    <div class="embedded-player-container" id="player-box">
                        <div class="default-player-placeholder">Click any item or Pantone swatch to inspect in-site</div>
                    </div>

                    <div id="preview-title">Select an item</div>
                    <p id="preview-desc">Color inspiration, pantone codes, and media previews will appear here instantly.</p>
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
            Shaked's Trend Radar &bull; Zine & Collage Aesthetic Edition
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
                playerBox.innerHTML = `<div class="default-player-placeholder" style="background:#111; color:#ff3399; font-family:'Special Elite',monospace; font-size:14px; padding:20px; text-align:center;">✨ Pantone Color Inspiration Loaded Successfully</div>`;
            }
        }
    </script>
</body>
</html>
"""
    
    final_html = html_content.replace("{TODAY_DATE}", today_date)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    print("✨ קובץ ה-index.html עודכן בהצלחה עם סגנון קולאז' עיתונות, סרטי הדבקה וטקסטורות Zine!")

if __name__ == "__main__":
    generate_html()
