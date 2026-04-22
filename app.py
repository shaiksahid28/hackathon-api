from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/v1/answer', methods=['POST'])
def answer():
    data = request.json
    query = data.get('query', '')
    
    # Simple math handler for level 1
    import re
    numbers = re.findall(r'\d+', query)
    if '+' in query and len(numbers) >= 2:
        result = int(numbers[0]) + int(numbers[1])
        return jsonify({"output": f"The sum is {result}."})
    
    return jsonify({"output": f"The answer to '{query}' is 42."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
