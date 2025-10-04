from flask import Flask, render_template, request, jsonify
import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Set OpenAI API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("Warning: OPENAI_API_KEY is not set! Your chatbot won't work until you add it in .env.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a valid question."})

    if not openai.api_key:
        return jsonify({"answer": "Error: OpenAI API key is missing. Please set it in your .env file."})

    try:
        # OpenAI v0.28 syntax
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=300,
            temperature=0.3
        )

        # Extract the AI response
        answer = response.choices[0].message["content"].strip()
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

