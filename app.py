from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1:free"

# Load resume text from file
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

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            answer = ask_openrouter(question)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
