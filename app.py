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
    ql = query.lower().strip()

    # Level 3: Odd/Even
    if 'odd' in ql or 'even' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            num = int(nums[0])
            is_odd = num % 2 != 0
            is_even = num % 2 == 0

            if 'odd' in ql:
                return jsonify({"output": "YES" if is_odd else "NO"})
            if 'even' in ql:
                return jsonify({"output": "YES" if is_even else "NO"})

    # Level 2: Date extraction
    m = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', query, re.IGNORECASE)
    if m:
        return jsonify({"output": f"{m.group(1)} {m.group(2).capitalize()} {m.group(3)}"})

    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', query, re.IGNORECASE)
    if m:
        return jsonify({"output": f"{m.group(2)} {m.group(1).capitalize()} {m.group(3)}"})

    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', query)
    if m:
        try:
            dt = datetime.strptime(f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "%Y-%m-%d")
            return jsonify({"output": dt.strftime("%-d %B %Y")})
        except:
            pass

    # Level 1: Addition
    m = re.search(r'(\d+)\s*\+\s*(\d+)', query)
    if m:
        result = int(m.group(1)) + int(m.group(2))
        return jsonify({"output": f"The sum is {result}."})

    return jsonify({"output": "I don't know."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
