# Backend qr-code-generator version 2.2
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import qrcode
import io
from PIL import Image
import bleach
import re
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

HEX_COLOR_RE = re.compile(r'^#([A-Fa-f0-9]{6})$')

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

CORS(app)

@app.route("/generate", methods=['POST'])
@limiter.limit("5 per minute")
def generate_qr():
    # 🔥 Added transparent_bg field
    data = request.json.get("data", "").strip()
    fill_color = request.json.get("fill_color", "black")
    back_color = request.json.get("back_color", "white")
    transparent = request.json.get("transparent_bg", False)  # 🔥 matches React checkbox

    # Validate input
    if not data:
        return jsonify({"error": "No text provided"}), 400
    
    if not is_safe_text(data):
        return jsonify({"error": "Insecure content detected"}), 400
    
    if not is_valid_color(fill_color):
        return jsonify({"error": "Invalid fill color format"}), 400

    # 🔥 Only validate background color if transparency is NOT enabled
    if not transparent and not is_valid_color(back_color):
        return jsonify({"error": "Invalid back color format"}), 400

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(data)
    qr.make()

    # 🔥 Create image in RGB mode first, then convert to RGBA for transparency
    img = qr.make_image(
        fill_color=fill_color,
        back_color=(back_color if not transparent else "white")  # white placeholder
    ).convert("RGBA")

    # 🔥 If transparent is requested, replace "almost white" pixels with transparency
    if transparent:
        datas = img.getdata()
        new_data = []
        for item in datas:
            r, g, b, a = item
            # Treat any pixel that is close to white as background
            if r > 250 and g > 250 and b > 250:
                new_data.append((255, 255, 255, 0))  # fully transparent
            else:
                new_data.append(item)  # preserve fill color
        img.putdata(new_data)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return send_file(buf, mimetype="image/png")


def is_safe_text(text):
    cleaned = bleach.clean(text, tags=[], strip=True)
    if cleaned != text:
        return False
    
    if "javascript:" in text.lower():
        return False
    
    return True


def is_valid_color(color):
    return bool(HEX_COLOR_RE.match(color))


if __name__ == "__main__":
    app.run(debug=True)
