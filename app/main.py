from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    task = request.form.get("task")
    job_post = request.form.get("job_post")
    resume = request.form.get("resume")

    if not job_post or not resume:
        return jsonify({"error": "Job posting and resume are required!"})

    if task == "analyze":
        response = analyze_job_post(job_post)
    elif task == "tailor":
        response = tailor_resume(job_post, resume)
    elif task == "interview":
        response = prepare_interview(job_post, resume)
    else:
        response = {"error": "Invalid task selected!"}

    return jsonify(response)

def analyze_job_post(job_post):
    """Analyzes a job posting for key skills and responsibilities."""
    prompt = f"Extract the key skills, qualifications, and responsibilities from this job posting:\n\n{job_post}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return {"analysis": response.choices[0].text.strip()}

def tailor_resume(job_post, resume):
    """Tailors the resume based on the job posting."""
