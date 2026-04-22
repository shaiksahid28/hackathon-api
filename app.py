from flask import Flask, request, jsonify
import os
import re
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running"})

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.json
    query = data.get('query', '')
    q = query.strip()
    ql = q.lower()

    # Level 3: Odd/Even check
    m = re.search(r'is\s+(\d+)\s+an?\s+(odd|even)\s+number', ql)
    if m:
        num = int(m.group(1))
        asked = m.group(2)
        if asked == 'odd':
            return jsonify({"output": "YES" if num % 2 != 0 else "NO"})
        else:
            return jsonify({"output": "YES" if num % 2 == 0 else "NO"})

    # Also handle: "Is 9 odd?" or "Is 9 even?"
    m = re.search(r'is\s+(\d+)\s+(odd|even)', ql)
    if m:
        num = int(m.group(1))
        asked = m.group(2)
        if asked == 'odd':
            return jsonify({"output": "YES" if num % 2 != 0 else "NO"})
        else:
            return jsonify({"output": "YES" if num % 2 == 0 else "NO"})

    # Level 2: Date extraction
    m = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', q, re.IGNORECASE)
    if m:
        return jsonify({"output": f"{m.group(1)} {m.group(2).capitalize()} {m.group(3)}"})

    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', q, re.IGNORECASE)
    if m:
        return jsonify({"output": f"{m.group(2)} {m.group(1).capitalize()} {m.group(3)}"})

    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', q)
    if m:
        try:
            dt = datetime.strptime(f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "%Y-%m-%d")
            return jsonify({"output": dt.strftime("%-d %B %Y")})
        except:
            pass

    # Level 1: Addition
    m = re.search(r'(\d+)\s*\+\s*(\d+)', q)
    if m:
        result = int(m.group(1)) + int(m.group(2))
        return jsonify({"output": f"The sum is {result}."})

    return jsonify({"output": "I don't know."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
