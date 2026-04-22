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

    # Pattern 1: "12 March 2024"
    m = re.search(r'(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', q, re.IGNORECASE)
    if m:
        day = m.group(1)
        month = m.group(2).capitalize()
        year = m.group(3)
        return jsonify({"output": f"{day} {month} {year}"})

    # Pattern 2: "March 12, 2024" or "March 12 2024"
    m = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', q, re.IGNORECASE)
    if m:
        month = m.group(1).capitalize()
        day = m.group(2)
        year = m.group(3)
        return jsonify({"output": f"{day} {month} {year}"})

    # Pattern 3: "2024-03-12" (ISO format)
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', q)
    if m:
        try:
            dt = datetime.strptime(f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "%Y-%m-%d")
            return jsonify({"output": dt.strftime("%-d %B %Y")})
        except:
            pass

    # Pattern 4: "12/03/2024" or "03/12/2024"
    m = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', q)
    if m:
        try:
            dt = datetime.strptime(f"{m.group(1)}/{m.group(2)}/{m.group(3)}", "%d/%m/%Y")
            return jsonify({"output": dt.strftime("%-d %B %Y")})
        except:
            pass

    # Pattern 5: "12th March 2024" or "1st January 2020"
    m = re.search(r'(\d{1,2})(?:st|nd|rd|th)\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})', q, re.IGNORECASE)
    if m:
        day = m.group(1)
        month = m.group(2).capitalize()
        year = m.group(3)
        return jsonify({"output": f"{day} {month} {year}"})

    # Level 1: Addition
    m = re
