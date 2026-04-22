from flask import Flask, request, jsonify
import os
import urllib.request
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running"})

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.json
    query = data.get('query', '')
    
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = json.dumps({
        "contents": [{
            "parts": [{"text": f"Answer this question with only the answer, no explanation, no extra text: {query}"}]
        }]
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        answer_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
    
    return jsonify({"output": answer_text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
