from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1:free"

with open("resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

def ask_openrouter(question):
    prompt = f"""
You are James Cheriyan. Respond based entirely on your resume.

Resume:
\"\"\"
{resume_text}
\"\"\"

Question: {question}
"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    )
    return response.json()["choices"][0]["message"]["content"]

@app.route("/")
def index():
    # Example questions to show on UI
    starter_questions = [
        "What are your technical skills?",
        "Describe your experience at Natterbox.",
        "What is your educational background?",
        "Summarize your work history.",
        "What certifications or degrees do you have?",
        "Where have you worked before?",
        "What experience do you have in telecom or VoIP?",
        "How do you handle system monitoring in a 24x7 environment?"
    ]
    return render_template("chat.html", starter_questions=starter_questions)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = ask_openrouter(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
