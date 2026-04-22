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
    
    numbers = re.findall(r'\d+', query)
    if '+' in query and len(numbers) >= 2:
        result = int(numbers[0]) + int(numbers[1])
        return jsonify({"output": f"The sum is {result}."})
    
    return jsonify({"output": f"The answer is: {query}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
