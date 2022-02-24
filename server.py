from flask import Flask, jsonify, request
import logging
import Script

app = Flask(__name__)

@app.route('/word-cloud/generate', methods=['POST'])
def generate_word_cloud():
    return Script.converter_pdf_json_count(request.json["path"], file_name="")

if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, host='localhost', port=8080)