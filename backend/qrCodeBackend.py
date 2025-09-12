#Backend qr-code-generator version 2.0
from flask import Flask, request, send_file, jsonify #for creating web api
from flask_cors import CORS #import library to allow cross-origin requests
import qrcode #generate qr code
import io #handle image data in memory instead of directly saving to disk
from PIL import Image #work with images
import bleach #sanitize input text
import re #regular expressions library - specific patterns in strings - using for XSS check
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address #prevent overloading server by limiting requests


HEX_COLOR_RE = re.compile(r'^#([A-Fa-f0-9]{6})$') #define pattern for hex colors

#Create new Flask app
app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

CORS(app) #enable for all routes
#Create URL endpoint that accepts POST requests
@app.route("/generate", methods=['POST'])
@limiter.limit("5 per minute")
#Generate QR code button function
def generate_qr():
    data = request.json.get("data", "").strip() #grabs JSON from frontend
    fill_color = request.json.get("fill_color", "black")
    back_color = request.json.get("back_color", "white")
    transparent = request.json.get("transparent_bg", False) #new field
    #validate inputs
    if not data:
        return jsonify({"error": "No text provided"}), 400 #check if user forgot to send text, HTTP status 400 error
    
    if not is_safe_text(data):
        return jsonify({"error": "Insecure content detected"}), 400 #bad request for insecure input data
    
    if not is_valid_color(fill_color) or not is_valid_color(back_color):
        return jsonify({"error": "Invalid color format"}), 400
    
    if not transparent and not is_valid_color(back_color):
        return jsonify({"error": "Invalid back color format"}), 400
    
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(data)
    qr.make() #finalize layout
    
    img = qr.make_image(fill_color=fill_color, back_color=(back_color if not transparent else "white")).convert("RGBA") #black and white PNG
    
    if transparent:
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[:3] == (255, 255, 255): #white
                new_data.append((255, 255, 255, 0)) #transparent
            else:
                new_data.append(item)
        img.putdata(new_data)
        
    buf = io.BytesIO() #in memory file creation
    img.save(buf, format="PNG")
    buf.seek(0)  #rewind memory buffer to beginning so Flask can see it
    
    return send_file(buf, mimetype="image/png") #flask sends image back as a response

def is_safe_text(text):
    #no script tags or javascript URLS - previous security update checking regular expressions only
    """if re.search(r'<script.*?>', text, re.IGNORECASE):
        return False
    
    if text.lower().startswith('javascript: '):
        return False
 """
    #check if input is safe
    cleaned = bleach.clean(text, tags=[], strip=True)
    if cleaned != text:
        return False
    
    #strip js URLS
    if "javacript:" in text.lower():
        return False
    
    return True

def is_valid_color(color):
    return bool(HEX_COLOR_RE.match(color))

if __name__ == "__main__":
    app.run(debug=True) #run flask app only if script is run directly


