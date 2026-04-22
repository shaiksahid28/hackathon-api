from flask import Flask, request, jsonify
import os
import re
import math

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running"})

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.json
    query = data.get('query', '')
    q = query.lower().strip()

    # Addition
    m = re.search(r'(\d+)\s*\+\s*(\d+)', q)
    if m:
        result = int(m.group(1)) + int(m.group(2))
        return jsonify({"output": f"The sum is {result}."})

    # Subtraction
    m = re.search(r'(\d+)\s*-\s*(\d+)', q)
    if m:
        result = int(m.group(1)) - int(m.group(2))
        return jsonify({"output": f"The difference is {result}."})

    # Multiplication
    m = re.search(r'(\d+)\s*[\*×x]\s*(\d+)', q)
    if m:
        result = int(m.group(1)) * int(m.group(2))
        return jsonify({"output": f"The product is {result}."})

    # Division
    m = re.search(r'(\d+)\s*/\s*(\d+)', q)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        result = a // b if a % b == 0 else round(a/b, 2)
        return jsonify({"output": f"The result is {result}."})

    # Square root
    m = re.search(r'square root of (\d+)', q)
    if m:
        result = math.isqrt(int(m.group(1)))
        return jsonify({"output": f"The square root is {result}."})

    # Square / power
    m = re.search(r'(\d+)\s*squared', q)
    if m:
        result = int(m.group(1)) ** 2
        return jsonify({"output": f"The result is {result}."})

    m = re.search(r'(\d+)\s*\^\s*(\d+)', q)
    if m:
        result = int(m.group(1)) ** int(m.group(2))
        return jsonify({"output": f"The result is {result}."})

    # Percentage
    m = re.search(r'(\d+)%\s*of\s*(\d+)', q)
    if m:
        result = (int(m.group(1)) / 100) * int(m.group(2))
        return jsonify({"output": f"The result is {result}."})

    return jsonify({"output": "I don't know."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
