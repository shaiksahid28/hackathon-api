from flask import Flask, request, jsonify
import os
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running"})

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.json
    query = data.get('query', '')
    
    # Addition - "What is X + Y?"
    add_match = re.search(r'(\d+)\s*\+\s*(\d+)', query)
    if add_match:
        result = int(add_match.group(1)) + int(add_match.group(2))
        return jsonify({"output": f"The sum is {result}."})

    return jsonify({"output": "I don't know."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
