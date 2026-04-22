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
    q = query.lower().strip()

    # Level 2: Date extraction
    # Match "12 March 2024" or "March 12 2024" or "12/03/2024" etc
    
    # Pattern: day month year (12 March 2024)
    m = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', query, re.IGNORECASE)
    if m:
        day = m.group(1)
        month = m.group(2).capitalize()
        year = m.group(3)
        return jsonify({"output": f"{day} {month} {year}"})

    # Pattern: month day year (March 12 2024)
    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', query, re.IGNORECASE)
    if m:
        month = m.group(1).capitalize()
        day = m.group(2)
        year = m.group(3)
        return jsonify({"output": f"{day} {month} {year}"})

    # Pattern: DD/MM/YYYY or MM/DD/YYYY
    m = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', query)
    if m:
        return jsonify({"output": f"{m.group(1)}/{m.group(2)}/{m.group(3)}"})

    # Level 1: Addition
    m = re.search(r'(\d+)\s*\+\s*(\d+)', q)
    if m:
        result = int(m.group(1)) + int(m.group(2))
        return jsonify({"output": f"The sum is {result}."})

    return jsonify({"output": "I don't know."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
