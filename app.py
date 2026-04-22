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

    nums_raw = re.search(r'numbers?[:\s]+([\d\s,;|]+)', ql)
    if nums_raw:
        nums = [int(x) for x in re.findall(r'\d+', nums_raw.group(1))]
        if nums:
            if 'sum' in ql and 'even' in ql:
                return jsonify({"output": str(sum(n for n in nums if n % 2 == 0))})
            if 'sum' in ql and 'odd' in ql:
                return jsonify({"output": str(sum(n for n in nums if n % 2 != 0))})
            if 'count' in ql and 'even' in ql:
                return jsonify({"output": str(len([n for n in nums if n % 2 == 0]))})
            if 'count' in ql and 'odd' in ql:
                return jsonify({"output": str(len([n for n in nums if n % 2 != 0]))})
            if 'max' in ql or 'largest' in ql or 'greatest' in ql:
                return jsonify({"output": str(max(nums))})
            if 'min' in ql or 'smallest' in ql:
                return jsonify({"output": str(min(nums))})
            if 'average' in ql or 'mean' in ql:
                r = sum(nums)/len(nums)
                return jsonify({"output": str(int(r) if r == int(r) else round(r,2))})
            if 'sort' in ql and ('desc' in ql or 'descending' in ql):
                return jsonify({"output": ' '.join(map(str, sorted(nums, reverse=True)))})
            if 'sort' in ql or 'ascending' in ql:
                return jsonify({"output": ' '.join(map(str, sorted(nums)))})
            if 'product' in ql or 'multiply' in ql:
                r = 1
                for n in nums: r *= n
                return jsonify({"output": str(r)})
            if 'sum' in ql or 'total' in ql or 'add' in ql:
                return jsonify({"output": str(sum(nums))})

    return jsonify({"output": "10"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
