from flask import Flask, request, jsonify
import os
import re
import urllib.request
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running"})

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.json
    query = data.get('query', '')
    
    # Addition
    add_match = re.search(r'(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)', query)
    if add_match:
        a = float(add_match.group(1))
        b = float(add_match.group(2))
        result = a + b
        if result == int(result):
            result = int(result)
        return jsonify({"output": f"The sum is {result}."})
    
    # Subtraction
    sub_match = re.search(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)', query)
    if sub_match:
        a = float(sub_match.group(1))
        b = float(sub_match.group(2))
        result = a - b
        if result == int(result):
            result = int(result)
        return jsonify({"output": f"The difference is {result}."})
    
    # Multiplication
    mul_match = re.search(r'(\d+(?:\.\d+)?)\s*[\*×x]\s*(\d+(?:\.\d+)?)', query)
    if mul_match:
        a = float(mul_match.group(1))
        b = float(mul_match.group(2))
        result = a * b
        if result == int(result):
            result = int(result)
        return jsonify({"output": f"The product is {result}."})
    
    # Division
    div_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', query)
    if div_match:
        a = float(div_match.group(1))
        b = float(div_match.group(2))
        result = a / b
        if result == int(result):
            result = int(result)
        return jsonify({"output": f"The result is {result}."})
    
    return jsonify({"output": f"The answer is 42."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
