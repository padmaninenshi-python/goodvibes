import os
import json
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API Key Check
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    print("❌ ERROR: Key Missing! Check .env")

client = Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template('vibes.html')

@app.route('/get-vibes', methods=['POST'])
def get_vibes():
    data = request.json
    user_feeling = data.get('feeling', '')

    try:
        # Prompt for quotes
        prompt = f"""
        User feeling: "{user_feeling}".
        Generate 5 short, powerful uplifting quotes.
        Return strictly JSON with a list under key "quotes".
        Example: {{ "quotes": ["Quote 1", "Quote 2"] }}
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a JSON generator. Output only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )

        result = json.loads(chat_completion.choices[0].message.content)
        return jsonify(result.get('quotes', []))

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)