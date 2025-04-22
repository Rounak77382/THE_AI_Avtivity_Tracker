from flask import Flask, jsonify, send_from_directory
from core.afkdetector2 import afkDetector

app = Flask(__name__, static_folder='./web')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/detect_afk', methods=['GET'])
def detect_afk():
    result = afkDetector()  
    return jsonify(result=result)

if __name__ == "__main__":
    app.run(debug=True, port=3000)