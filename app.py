import os
import zipfile
from flask import Flask, render_template_string, send_from_directory, abort

app = Flask(__name__)

# Default media folder
MEDIA_FOLDER = os.path.abspath("./media")

# Allowed extensions
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.ogg', '.mov', '.mkv'}

# HTML & CSS & JS Template - Cloudy Eclipse Theme with Lightbox
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eclipse - August 12, 2026</title>
    
    <!-- FAVICON ECLIPSE (SVG Data URI) -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='42' fill='%23ffffff' filter='drop-shadow(0 0 8px %2338bdf8)'/><circle cx='46' cy='50' r='40' fill='%23090d16'/></svg>">

    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body { 
            font-family: system-ui, -apple-system, sans-serif; 
            background: radial-gradient(circle at 50% 10%, #1e293b 0%, #0f172a 50%, #090d16 100%);
            color: #e2e8f0; 
            min-height: 100vh;
            padding: 30px 20px;
            position: relative;
            overflow-x: hidden;
        }

        /* Ambient Cloud Glow Elements */
        .cloud-bg {
            position: fixed;
            top: -100px;
            left: 50%;
            transform: translateX(-50%);
            width: 800px;
            height: 400px;
            background: radial-gradient(ellipse at center, rgba(148, 163, 184, 0.15) 0%, rgba(15, 23, 42, 0) 70%);
            filter: blur(60px);
            pointer-events: none;
            z-index: 0;
            animation: pulse-glow 8s infinite alternate ease-in-out;
        }

        @keyframes pulse-glow {
            0% { opacity: 0.5; transform: translateX(-50%) scale(0.9); }
            100% { opacity: 1; transform: translateX(-50%) scale(1.1); }
        }

        .header {
            position: relative;
            z-index: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 40px;
            text-align: center;
        }

        /* --- ECLIPSE ANIMATED ICON --- */
        .eclipse-icon {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: #ffffff; /* Le Soleil blanc fixe */
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.8), 0 0 40px rgba(226, 232, 240, 0.4);
            margin-bottom: 8px;
            position: relative;
            overflow: hidden;
        }

        /* La Lune : Disque sombre (#090d16) arrivant par la droite */
        .eclipse-icon::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: #090d16;
            /* Animation unique de 5s se bloquant au centre */
            animation: move-moon-to-center 5s ease-out forwards;
        }

        /* La Couronne Solaire : Apparaît quand l'éclipse devient totale */
        .eclipse-icon::after {
            content: '';
            position: absolute;
            top: -5%;
            left: -5%;
            width: 110%;
            height: 110%;
            border-radius: 50%;
            pointer-events: none;
            box-shadow: 
                0 0 15px 3px rgba(255, 255, 255, 0.9),
                0 0 30px 8px rgba(56, 189, 248, 0.6),
                0 0 50px 15px rgba(148, 163, 184, 0.4);
            opacity: 0;
            animation: corona-appear 5s ease-out forwards;
        }

        @keyframes move-moon-to-center {
            0% {
                transform: translateX(105%) scale(0.98);
            }
            100% {
                transform: translateX(0%) scale(1);
            }
        }

        @keyframes corona-appear {
            0%, 60% {
                opacity: 0;
            }
            100% {
                opacity: 1;
            }
        }

        h1 { 
            color: #f1f5f9; 
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            text-shadow: 0 0 20px rgba(241, 245, 249, 0.3);
        }

        .subtitle {
            color: #94a3b8;
            font-size: 0.95rem;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .btn-zip {
            margin-top: 10px;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
            color: #f8fafc;
            border: 1px solid rgba(226, 232, 240, 0.25);
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), 0 0 15px rgba(148, 163, 184, 0.1);
        }
        .btn-zip:hover { 
            background: linear-gradient(135deg, #475569 0%, #334155 100%);
            border-color: rgba(226, 232, 240, 0.5);
            box-shadow: 0 6px 25px rgba(0, 0, 0, 0.6), 0 0 20px rgba(226, 232, 240, 0.25);
            transform: translateY(-2px); 
        }

        .grid { 
            position: relative;
            z-index: 1;
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
            gap: 24px; 
            max-width: 1400px; 
            margin: 0 auto; 
        }

        .card { 
            background: rgba(30, 41, 59, 0.6); 
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px; 
            overflow: hidden; 
            display: flex; 
            flex-direction: column; 
            border: 1px solid rgba(148, 163, 184, 0.15); 
            transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-4px);
            border-color: rgba(226, 232, 240, 0.35);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 15px rgba(148, 163, 184, 0.1);
        }

        .media-container { 
            width: 100%; 
            height: 220px; 
            background: #090d16; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            position: relative;
        }
        
        .media-container img { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            cursor: pointer;
            transition: opacity 0.2s ease;
        }
        .media-container img:hover {
            opacity: 0.9;
        }

        .media-container video { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
        }

        .info { 
            padding: 16px; 
            display: flex; 
            flex-direction: column; 
            gap: 12px; 
            flex-grow: 1; 
            justify-content: space-between; 
        }

        .filename { 
            font-size: 0.88rem; 
            color: #cbd5e1; 
            word-break: break-all; 
            font-weight: 500;
        }

        .download-btn { 
            display: inline-block; 
            text-align: center; 
            background: rgba(51, 65, 85, 0.8); 
            color: #38bdf8; 
            border: 1px solid rgba(56, 189, 248, 0.3);
            text-decoration: none; 
            padding: 9px 14px; 
            border-radius: 8px; 
            font-weight: 600; 
            font-size: 0.85rem; 
            transition: all 0.2s ease; 
        }

        .download-btn:hover { 
            background: #38bdf8; 
            color: #0f172a;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }

        .empty-msg {
            grid-column: 1 / -1;
            text-align: center;
            color: #64748b;
            font-size: 1.1rem;
            margin-top: 60px;
        }

        /* LIGHTBOX STYLES */
        .lightbox-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(9, 13, 22, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            user-select: none;
        }

        .lightbox-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .lightbox-content {
            position: relative;
            max-width: 90vw;
            max-height: 85vh;
            border-radius: 12px;
            box-shadow: 
                0 20px 50px rgba(0, 0, 0, 0.8),
                0 0 40px rgba(226, 232, 240, 0.2);
            border: 1px solid rgba(226, 232, 240, 0.2);
            background: #000;
            overflow: hidden;
            transform: scale(0.95);
            transition: transform 0.3s ease;
        }

        .lightbox-overlay.active .lightbox-content {
            transform: scale(1);
        }

        .lightbox-img {
            display: block;
            max-width: 90vw;
            max-height: 85vh;
            object-fit: contain;
        }

        .lightbox-close {
            position: absolute;
            top: 20px;
            right: 25px;
            color: #f8fafc;
            font-size: 2rem;
            cursor: pointer;
            z-index: 1010;
            line-height: 1;
            transition: color 0.2s;
            text-shadow: 0 0 10px rgba(0,0,0,0.8);
        }

        .lightbox-close:hover {
            color: #38bdf8;
        }

        .lightbox-btn {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(15, 23, 42, 0.6);
            color: #f8fafc;
            border: 1px solid rgba(226, 232, 240, 0.2);
            font-size: 1.8rem;
            padding: 15px 12px;
            cursor: pointer;
            z-index: 1005;
            border-radius: 8px;
            transition: all 0.2s ease;
            backdrop-filter: blur(4px);
        }

        .lightbox-btn:hover {
            background: rgba(56, 189, 248, 0.8);
            color: #0f172a;
        }

        .lightbox-btn.prev { left: 15px; }
        .lightbox-btn.next { right: 15px; }

        .lightbox-caption {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(15, 23, 42, 0.85);
            color: #cbd5e1;
            padding: 12px 20px;
            font-size: 0.9rem;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
</head>
<body>
    <div class="cloud-bg"></div>

    <div class="header">
        <div class="eclipse-icon"></div>
        <h1>Solar Eclipse - August 12, 2026</h1>
        <p class="subtitle">Edouard LETAILLEUR</p>
        
        {% if has_zip or items %}
        <a href="/download-all" class="btn-zip" download="all.zip">
            📦 Download All Media (ZIP)
        </a>
        {% endif %}
    </div>

    <div class="grid">
        {% for item in items %}
        <div class="card">
            <div class="media-container">
                {% if item.type == 'image' %}
                    <img src="/media/{{ item.name }}" alt="{{ item.name }}" loading="lazy" onclick="openLightbox('{{ item.name }}')">
                {% elif item.type == 'video' %}
                    <video controls preload="metadata">
                        <source src="/media/{{ item.name }}">
                        Your browser does not support video playback.
                    </video>
                {% endif %}
            </div>
            <div class="info">
                <span class="filename">{{ item.name }}</span>
                <a href="/download/{{ item.name }}" class="download-btn" download>Download</a>
            </div>
        </div>
        {% else %}
        <p class="empty-msg">No eclipse media found in the directory.</p>
        {% endfor %}
    </div>

    <!-- LIGHTBOX MODAL -->
    <div class="lightbox-overlay" id="lightbox" onclick="closeLightbox(event)">
        <span class="lightbox-close" onclick="closeLightbox(event)">&times;</span>
        <button class="lightbox-btn prev" onclick="prevImage(event)">&#10094;</button>
        <button class="lightbox-btn next" onclick="nextImage(event)">&#10095;</button>
        <div class="lightbox-content" onclick="event.stopPropagation()">
            <img src="" alt="" class="lightbox-img" id="lightbox-img">
            <div class="lightbox-caption" id="lightbox-caption"></div>
        </div>
    </div>

    <script>
        const imageList = [
            {% for item in items if item.type == 'image' %}
                "{{ item.name }}"{% if not loop.last %},{% endif %}
            {% endfor %}
        ];

        let currentIndex = -1;
        let touchStartX = 0;
        let touchEndX = 0;

        function openLightbox(filename) {
            currentIndex = imageList.indexOf(filename);
            if (currentIndex === -1) return;

            updateLightbox();

            const lightbox = document.getElementById('lightbox');
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function updateLightbox() {
            if (currentIndex < 0 || currentIndex >= imageList.length) return;
            const filename = imageList[currentIndex];
            const img = document.getElementById('lightbox-img');
            const caption = document.getElementById('lightbox-caption');

            img.src = '/media/' + filename;
            caption.textContent = filename;
        }

        function closeLightbox(event) {
            const lightbox = document.getElementById('lightbox');
            lightbox.classList.remove('active');
            document.body.style.overflow = 'auto';
        }

        function prevImage(event) {
            if (event) event.stopPropagation();
            if (imageList.length === 0) return;
            currentIndex = (currentIndex - 1 + imageList.length) % imageList.length;
            updateLightbox();
        }

        function nextImage(event) {
            if (event) event.stopPropagation();
            if (imageList.length === 0) return;
            currentIndex = (currentIndex + 1) % imageList.length;
            updateLightbox();
        }

        document.addEventListener('keydown', function(e) {
            const lightbox = document.getElementById('lightbox');
            if (!lightbox.classList.contains('active')) return;

            if (e.key === 'Escape') closeLightbox();
            else if (e.key === 'ArrowLeft') prevImage();
            else if (e.key === 'ArrowRight') nextImage();
        });

        const lightboxOverlay = document.getElementById('lightbox');

        lightboxOverlay.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        lightboxOverlay.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });

        function handleSwipe() {
            const swipeThreshold = 50;
            if (touchEndX < touchStartX - swipeThreshold) {
                nextImage();
            } else if (touchEndX > touchStartX + swipeThreshold) {
                prevImage();
            }
        }
    </script>
</body>
</html>
"""

def get_media_files():
    """Scans the directory for image and video files."""
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER, exist_ok=True)
        
    media_items = []
    try:
        filenames = sorted(os.listdir(MEDIA_FOLDER))
    except Exception:
        filenames = []

    for filename in filenames:
        ext = os.path.splitext(filename)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            media_items.append({'name': filename, 'type': 'image'})
        elif ext in VIDEO_EXTENSIONS:
            media_items.append({'name': filename, 'type': 'video'})
            
    return media_items

@app.route('/')
def index():
    files = get_media_files()
    zip_path = os.path.join(MEDIA_FOLDER, "all.zip")
    has_zip = os.path.exists(zip_path)
    return render_template_string(HTML_TEMPLATE, items=files, has_zip=has_zip)

@app.route('/media/<path:filename>')
def serve_media(filename):
    """Serves media files for previewing."""
    return send_from_directory(MEDIA_FOLDER, filename)

@app.route('/download/<path:filename>')
def download_media(filename):
    """Forces download for individual files."""
    return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)

@app.route('/download-all')
def download_all():
    """Downloads all.zip if present, or creates it on-the-fly from available media files."""
    zip_path = os.path.join(MEDIA_FOLDER, "all.zip")

    if not os.path.exists(zip_path):
        media_files = get_media_files()
        if not media_files:
            return abort(404, description="No files available to package.")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in media_files:
                file_path = os.path.join(MEDIA_FOLDER, item['name'])
                zipf.write(file_path, arcname=item['name'])

    return send_from_directory(MEDIA_FOLDER, "all.zip", as_attachment=True)

if __name__ == '__main__':
    print(f"Serving media folder: {MEDIA_FOLDER}")
    app.run(debug=True, host='0.0.0.0', port=8080)
