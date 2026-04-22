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

    # Level 3: Odd/Even - ALL possible variations
    if 'odd' in ql or 'even' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            num = int(nums[0])
            is_odd = num % 2 != 0

            # "odd or even" type question
            if 'odd' in ql and 'even' in ql:
                return jsonify({"output": "Odd" if is_odd else "Even"})

            # "is X odd?" / "is X an odd number?"
            if 'odd' in ql:
                return jsonify({"output": "YES" if is_odd else "NO"})

            # "is X even?" / "is X an even number?"
            if 'even' in ql:
                return jsonify({"output": "YES" if not is_odd else "NO"})

    # Level 3: Prime number check
    if 'prime' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            num = int(nums[0])
            if num < 2:
                is_prime = False
            else:
                is_prime = all(num % i != 0 for i in range(2, int(num**0.5)+1))
            return jsonify({"output": "YES" if is_prime else "NO"})

    # Level 3: Positive/Negative check
    if 'positive' in ql or 'negative' in ql:
        nums = re.findall(r'-?\d+', ql)
        if nums:
            num = int(nums[0])
            if 'positive' in ql:
                return jsonify({"output": "YES" if num > 0 else "NO"})
            if 'negative' in ql:
                return jsonify({"output": "YES" if num < 0 else "NO"})

    # Level 3: Greater/Less than
    m = re.search(r'is\s+(-?\d+)\s+greater\s+than\s+(-?\d+)', ql)
    if m:
        return jsonify({"output": "YES" if int(m.group(1)) > int(m.group(2)) else "NO"})

    m = re.search(r'is\s+(-?\d+)\s+less\s+than\s+(-?\d+)', ql)
    if m:
        return jsonify({"output": "YES" if int(m.group(1)) < int(m.group(2)) else "NO"})

    # Level 3: Equal check
    m = re.search(r'is\s+(-?\d+)\s+equal\s+to\s+(-?\d+)', ql)
    if m:
        return jsonify({"output": "YES" if int(m.group(1)) == int(m.group(2)) else "NO"})

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
