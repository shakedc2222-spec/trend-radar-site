const initialTrends = [
    { type: 'card', class: 'card-landscape tape-olive dog-ear', top: 0, left: 10, rot: -1.5, bg: '#2c3e50', badge: 'TikTok Trend', title: 'Neo-Brutalism & UI Motion Breakdown', sub: 'TikTok 24h Peak Trend', media: 'tiktok', url: 'https://www.tiktok.com/embed/v2/7234567890', icon: '▶' },
    { type: 'card', class: 'card-square tape-terracotta dog-ear', top: 260, left: 10, rot: 1.5, bg: '#111', badge: 'Editorial IG', title: 'Vogue New Era Cover Drop', sub: 'Print & Editorial IG Reel', media: 'instagram', url: 'https://www.instagram.com/p/C000000/embed', icon: 'VOGUE' },
    { type: 'card', class: 'card-landscape tape-olive', top: 280, left: 340, rot: 1, bg: '#8c6d62', badge: 'Runway Stream', title: 'Milan Fashion Week Tailoring', sub: 'Runway & Street Style', media: 'youtube', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ', icon: '🧥' },
    { type: 'torn', top: 580, left: 10, rot: 1, title: 'Print Archive Feature', sub: 'Analog Print Curation' },
    { type: 'card', class: 'card-square tape-terracotta dog-ear', top: 600, left: 460, rot: -1.5, bg: '#4a5d4e', badge: 'Exhibition Video', title: 'Immersive Digital Art Light Installation', sub: 'Global Exhibition Drop', media: 'youtube', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ', icon: '🏛️' },
    { type: 'card', class: 'card-landscape tape-olive dog-ear', top: 900, left: 10, rot: -1, bg: '#556b2f', badge: 'Culinary Reels', title: 'Sculptural Pistachio Tart Art', sub: 'Culinary Social Trend', media: 'youtube', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ', icon: '🥐' },
    { type: 'card', class: 'card-portrait tape-terracotta', top: 920, left: 460, rot: 2, bg: '#7b1fa2', badge: '3D Spotlight', title: 'Surrealist 3D Organic Textures', sub: 'Artist Spotlight', media: 'youtube', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ', icon: '🎨' }
];

let workspaceY = 1250;

function renderCollageBatch(items) {
    const workspace = document.getElementById('collage-workspace');
    items.forEach(item => {
        if (item.type === 'card') {
            const card = document.createElement('div');
            card.className = `collage-card ${item.class}`;
            card.style.top = `${item.top}px`;
            card.style.left = `${item.left}px`;
            card.style.transform = `rotate(${item.rot}deg)`;
            card.onclick = () => playEmbeddedMedia(item.media, item.url, item.title, item.sub);
            
            card.innerHTML = `
                <div class="visual-box ${item.class.includes('landscape') ? 'visual-box-landscape' : item.class.includes('square') ? 'visual-box-square' : ''}" style="background: ${item.bg};">
                    <span class="badge-title">${item.badge}</span>${item.icon}
                </div>
                <div class="card-caption">${item.title}</div>
                <div class="card-sub">${item.sub}</div>
            `;
            workspace.appendChild(card);
        } else if (item.type === 'torn') {
            const torn = document.createElement('div');
            torn.className = 'torn-paper-art-frame';
            torn.style.top = `${item.top}px`;
            torn.style.left = `${item.left}px`;
            torn.style.transform = `rotate(${item.rot}deg)`;
            torn.onclick = () => playEmbeddedMedia('info', '', item.title, item.sub);

            torn.innerHTML = `
                <div style="height: 140px; display: flex; flex-direction: column; justify-content: center; font-family: 'Raleway', sans-serif; font-weight: 800; font-size: 20px; color: var(--stroke-dark); text-align: center;">
                    ${item.title}
                    <span style="font-size: 11px; font-weight: normal; font-family: 'Special Elite', monospace; color: #666; margin-top: 6px;">${item.sub}</span>
                </div>
                <div class="card-caption" style="margin-top: 10px;">Ripped Paper Print Asset</div>
                <div class="card-sub">High Vertical Layout</div>
            `;
            workspace.appendChild(torn);
        }
    });
}

// טעינה ראשונית
document.addEventListener("DOMContentLoaded", () => {
    renderCollageBatch(initialTrends);
    document.getElementById('live-date').innerText = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
});

// אינסופר גלילה דינמי - מוסיף עוד ועוד תכנים אוטומטית כשגוללים למטה!
window.addEventListener('scroll', () => {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1200) {
        const nextBatch = [
            { type: 'card', class: 'card-square tape-terracotta dog-ear', top: workspaceY, left: 10, rot: 1.5, bg: '#004d40', badge: 'Branding', title: 'Tactile Eco-Packaging', sub: 'Behance Branding Trend', media: 'youtube', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ', icon: '🧴' },
            { type: 'card', class: 'card-landscape tape-olive', top: workspaceY + 20, left: 340, rot: -1, bg: '#311b92', badge: 'Spatial UX', title: 'Spatial Computing & Bezi 3D', sub: 'Immersive Technology', media: 'youtube', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ', icon: '🥽' },
            { type: 'torn', top: workspaceY + 320, left: 10, rot: -1, title: 'Zine & Press Cutout', sub: 'Alternative Press Curation' },
            { type: 'card', class: 'card-square tape-terracotta', top: workspaceY + 340, left: 460, rot: 2, bg: '#b71c1c', badge: 'Music Culture', title: 'Analog Album Art & Grainy Swiss Design', sub: 'Music & Visual Culture', media: 'youtube', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ', icon: '🎵' }
        ];
        renderCollageBatch(nextBatch);
        workspaceY += 650;
    }
});

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