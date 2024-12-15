from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import io
import os
import json

app = Flask(__name__)

API_KEY = 'YOUR_API_KEY_HERE'
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image = Image.open(file.stream)

        # Updated prompt for brain tumor detection
        prompt = (
            "Analyze the brain MRI image and provide the result in the following format:\n\n"
            "Tumor Detected: <Yes/No>\n"
            "Type of Tumor: <type1>\n"
            "Size: <size1>\n"
            "Location: <location1>\n"
            "Description: <description1>\n"
            "Confidence: <confidence_percentage>%\n\n"
            "Do not include any additional clarifications, estimates, or parenthetical details. Only provide the main point for each category (e.g., size, location, description). Avoid mentioning the need for further imaging, biopsy, or any follow-up procedures unless directly relevant to the result.\n\n"
            "If no tumor is detected, respond with: Tumor Detected: No\n"
            "Ensure that the confidence percentage reflects the model's real analysis based on the image. The confidence should not be fixed or static, but instead should vary according to the specific findings in the MRI scan."
        )

        result = model.generate_content(
            [image, "\n\n", prompt]
        )

        result_text = result.text.strip()

        return jsonify({'result': result_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
