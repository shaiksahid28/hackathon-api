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

    # Level 3: Odd/Even - all variations
    # "Is 9 an odd number?" / "Is 9 odd?" / "9 is odd?" / "Check if 9 is odd"
    m = re.search(r'(\d+)\s+(?:is\s+)?an?\s+(odd|even)(?:\s+number)?', ql)
    if not m:
        m = re.search(r'is\s+(\d+)\s+(?:an?\s+)?(odd|even)', ql)
    if not m:
        m = re.search(r'(?:check|tell|find).*?(\d+).*?(odd|even)', ql)
    if m:
        try:
            num = int(m.group(1))
            asked = m.group(2)
        except:
            num = int(m.group(2)) if m.group(2).isdigit() else int(m.group(1))
            asked = m.group(2) if not m.group(2).isdigit() else m.group(1)
        if asked == 'odd':
            return jsonify({"output": "YES" if num % 2 != 0 else "NO"})
        else:
            return jsonify({"output": "YES" if num % 2 == 0 else "NO"})

    # General odd/even with number found anywhere
    if 'odd' in ql or 'even' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            num = int(nums[0])
            if 'odd' in ql:
                return jsonify({"output": "YES" if num % 2 != 0 else "NO"})
            else:
                return jsonify({"output": "YES" if num % 2 == 0 else "NO"})

    # Level 2: Date extraction
    m = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', q, re.IGNORECASE)
    if m:
        return jsonify({"output": f"{m.group(1)} {m.group(2).capitalize()} {m.group(3)}"})

    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', q, re.IGNORECASE)
    if m:
        re
