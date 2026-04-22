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
    
    # Handle addition: "What is 10 + 15?"
    add_match = re.search(r'(\d+)\s*\+\s*(\d+)', query)
    if add_match:
        result = int(add_match.group(1)) + int(add_match.group(2))
        return jsonify({"output": f"The sum is {result}."})
    
    # Handle subtraction
    sub_match = re.search(r'(\d+)\s*-\s*(\d+)', query)
    if sub_match:
        result = int(sub_match.group(1)) - int(sub_match.group(2))
        return jsonify({"output": f"The difference is {result}."})
    
    # Handle multiplication
    mul_match = re.search(r'(\d+)\s*[\*x×]\s*(\d+)', query)
    if mul_match:
        result = int(mul_match.group(1)) * int(mul_match.group(2))
        return jsonify({"output": f"The product is {result}."})
    
    # Handle division
    div_match = re.search(r'(\d+)\s*/\s*(\d+)', query)
    if div_match:
        result = int(div_match.group(1)) / int(div_match.group(2))
        return jsonify({"output": f"The result is {result}."})
    
    return jsonify({"output": f"The answer is {query}."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
