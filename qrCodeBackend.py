#Backend qr-code-generator version 2.0
from flask import Flask, request, send_file, jsonify #for creating web api
from flask_cors import CORS #import library to allow cross-origin requests
import qrcode #generate qr code
import io #handle image data in memory instead of directly saving to disk
from PIL import Image #work with images

import re #regular expressions library - specific patterns in strings - using for XSS check

#Create new Flask app
app = Flask(__name__)
CORS(app) #enable for all routes
#Create URL endpoint that accepts POST requests
@app.route("/generate", methods=['POST'])

#Generate QR code button function
def generate_qr():
    data = request.json.get("data", "").strip() #grabs JSON from frontend
    fill_color = request.json.get("fill_color", "black")
    back_color = request.json.get("back_color", "white")

    if not data:
        return jsonify({"error": "No text provided"}), 400 #check if user forgot to send text, HTTP status 400 error
    
    if not is_safe_text(data):
        return jsonify({"error": "Insecure content detected"}), 400 #bad request for insecure input data
    
    qr = qrcode.QRCode(version=1, box_size=5, border=5)
    qr.add_data(data)
    qr.make() #finalize layout
    img = qr.make_image(fill_color=fill_color, back_color=back_color) #black and white PNG
    buf = io.BytesIO() #in memory file creation
    img.save(buf, format="PNG")
    buf.seek(0)  #rewind memory buffer to beginning so Flask can see it
    
    return send_file(buf, mimetype="image/png") #flask sends image back as a response

def is_safe_text(text):
    #no script tags or javascript URLS
    if re.search(r'<script.*?>', text, re.IGNORECASE):
        return False
    
    if text.lower().startswith('javascript: '):
        return False
    
    return True

if __name__ == "__main__":
    app.run(debug=True) #run flask app only if script is run directly


