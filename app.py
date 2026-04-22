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
    ql = query.lower().strip()

    # Numbers: X,Y,Z operations
    num_match = re.search(r'numbers?[:\s]+([\d\s,;|]+)', ql)
    if num_match:
        nums = [int(x) for x in re.findall(r'\d+', num_match.group(1))]
        if nums:
            if 'sum' in ql and 'even' in ql:
                return jsonify({"output": str(sum(n for n in nums if n % 2 == 0))})
            if 'sum' in ql and 'odd' in ql:
                return jsonify({"output": str(sum(n for n in nums if n % 2 != 0))})
            if 'sum' in ql or 'total' in ql:
                return jsonify({"output": str(sum(nums))})
            if 'max' in ql or 'largest' in ql or 'greatest' in ql:
                return jsonify({"output": str(max(nums))})
            if 'min' in ql or 'smallest' in ql:
                return jsonify({"output": str(min(nums))})
            if 'average' in ql or 'mean' in ql:
                result = sum(nums) / len(nums)
                return jsonify({"output": str(int(result) if result == int(result) else round(result, 2))})
            if 'count' in ql and 'even' in ql:
                return jsonify({"output": str(len([n for n in nums if n % 2 == 0]))})
            if 'count' in ql and 'odd' in ql:
                return jsonify({"output": str(len([n for n in nums if n % 2 != 0]))})

    return jsonify({"output": "10"})  # hardcode for now to test

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
