import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 1. Setup Gemini API 
# (Add GEMINI_API_KEY to your Railway Variables)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running"})

@app.route('/v1/answer', methods=['POST'])
def answer():
    try:
        # Accept the POST request data
        data = request.get_json()
        query = data.get('query', '')
        
        # Initialize Gemini 1.5 Flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # This prompt ensures you get ONLY the result (e.g., "10" instead of "The sum is 10")
        # This is the secret to getting 100% on the Jaccard/Cosine scores.
        prompt = (
            "Solve the following query precisely. "
            "Return ONLY the final answer. No words, no sentences, no explanations. "
            f"Query: {query}"
        )
        
        response = model.generate_content(prompt)
        ai_output = response.text.strip()
        
        # Return the exact JSON structure required by the challenge
        return jsonify({"output": ai_output})

    except Exception as e:
        return jsonify({"output": "Error"}), 500

if __name__ == '__main__':
    # Railway binding
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
