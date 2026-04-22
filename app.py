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

    # Level 4: Sum even/odd numbers from list
    # "Numbers: 2,5,8,11. Sum even numbers."
    m = re.search(r'numbers?[:\s]+([\d,\s]+)', ql)
    if m:
        nums = [int(x.strip()) for x in re.findall(r'\d+', m.group(1))]
        
        if 'sum even' in ql:
            result = sum(n for n in nums if n % 2 == 0)
            return jsonify({"output": str(result)})
        
        if 'sum odd' in ql:
            result = sum(n for n in nums if n % 2 != 0)
            return jsonify({"output": str(result)})
        
        if 'count even' in ql:
            result = len([n for n in nums if n % 2 == 0])
            return jsonify({"output": str(result)})
        
        if 'count odd' in ql:
            result = len([n for n in nums if n % 2 != 0])
            return jsonify({"output": str(result)})
        
        if 'largest' in ql or 'maximum' in ql or 'max' in ql:
            return jsonify({"output": str(max(nums))})
        
        if 'smallest' in ql or 'minimum' in ql or 'min' in ql:
            return jsonify({"output": str(min(nums))})
        
        if 'sum' in ql:
            return jsonify({"output": str(sum(nums))})
        
        if 'average' in ql or 'mean' in ql:
            result = sum(nums) / len(nums)
            return jsonify({"output": str(int(result) if result == int(result) else round(result, 2))})
        
        if 'sort' in ql and 'desc' in ql:
            return jsonify({"output": ', '.join(map(str, sorted(nums, reverse=True)))})
        
        if 'sort' in ql:
            return jsonify({"output": ', '.join(map(str, sorted(nums)))})

    # Level 3: Odd/Even check
    if 'odd' in ql or 'even' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            num = int(nums[0])
            is_odd = num % 2 != 0
            if 'odd' in ql and 'even' in ql:
                return jsonify({"output": "Odd" if is_odd else "Even"})
            if 'odd' in ql:
                return jsonify({"output": "YES" if is_odd else "NO"})
            if 'even' in ql:
                return jsonify({"output": "YES" if not is_odd else "NO"})

    # Level 3: Prime
    if 'prime' in ql:
        nums = re.findall(r'\d+', ql)
        if nums:
            num = int(nums[0])
            is_prime = num > 1 and all(num % i != 0 for i in range(2, int(num**0.5)+1))
            return jsonify({"output": "YES" if is_prime else "NO"})

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
